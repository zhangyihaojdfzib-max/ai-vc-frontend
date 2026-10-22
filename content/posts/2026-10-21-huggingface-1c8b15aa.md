---
title: 'Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium.'
title_original: 'Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium.'
date: '2026-10-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/amazon/profiling-torchneuron-part-1
author: ''
summary: '[翻译失败，原文如下]


  # Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium.


  Many ML practitioners have some intuition about how to make mo...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:55:44.096921'
---

[翻译失败，原文如下]

# Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium.

Many ML practitioners have some intuition about how to make models run fast, but fewer know how to analyze why a model is slow. In Part 1 of this series, you will learn how to systematically analyze inference performance and identify where the time is spent.

This post starts from scratch and assumes no prior profiling experience. The walkthrough uses AWS Trainium, a purpose-built AI chip for deep learning training and inference workloads, andTorchNeuron, its open source native PyTorch backend. TorchNeuron supports standard PyTorch workflows on Trainium, including eager execution,torch.compile, and standard PyTorch APIs, with minimal code changes. Additionally, TorchNeuron integrates withNeuron Kernel Interface (NKI)to enable custom operators and performance optimization for Trainium hardware. By the end, you should know:

- How to configuretorch.profilerwith the Neuron backend and capture a clean trace.
- How to read thekey_averages()table to identify which operations consume Neuron device time and compare their Self CPU time.
- How to follow one operation through Neuron Explorer, from framework dispatch through runtime scheduling to hardware execution on a NeuronCore.
- How these signals change across three implementations of the same operation.

## Neuron as a PyTorch Backend

Before you profile a workload, it helps to understand howNeuronintegrates with PyTorch.

The Neuron backend uses PyTorch'sPrivateUse1extension point. This mechanism lets an accelerator integrate with the framework without adding a dedicated dispatch key such ascuda. Thetorch_neuronxpackage works with upstream PyTorch to register Neuron as a native backend for PyTorch code. For details about this extension mechanism, seeFacilitating New Backend Integration by PrivateUse1.

## Set Up the Profiler

You use two objects to profile a Neuron workload:

- NeuronConfigcontrols which Neuron data streams and NeuronCores to capture and where to write the output. You pass it totorch.profiler.profileasexperimental_config.
- NeuronProfilertakes aNeuronConfigand provides anexport_tracecallback. The callback writes the framework trace,trace.json, alongside the Neuron system traces.

```python
nc = NeuronConfig(
    modes=[ProfileMode.DEVICE, ProfileMode.RUNTIME],
    profile_output_dir=OUTPUT_DIR,
    capture_enabled_for_nc='0',
    correlate_device_time=True,
)
exporter = NeuronProfiler(nc)

```

Themodesparameter selects the data streams to capture, such as device instructions and runtime traces. Thecapture_enabled_for_ncparameter selects the NeuronCores to trace. Settingcorrelate_device_time=Truepropagates device time from the trace into thekey_averages()table, where you can compare CPU and Neuron device time. For the complete parameter reference and availableProfileModevalues, see the NeuronConfigProfile Modes documentation.

## Tooling: Neuron Explorer

Neuron Explorer is a browser-based viewer for the system trace, device timeline, and per-engine breakdown. You can access it through an SSH tunnel or the Visual Studio Code extension. In this post, you use Explorer to confirm whatkey_averages()reports numerically and inspect what happens between dispatches.

After profiling, the output directory contains the system trace and, when you capture device data, matched.neffand.ntfffiles. The Neuron Executable File Format (NEFF) contains the compiled Neuron executable, while the matching NTFF contains its hardware instruction trace. The files share a numeric hash that identifies them as a pair. To open the profile in Neuron Explorer, upload the complete output directory for a system or combined profile. For a device-only profile, upload the matching.neffand.ntfffiles individually. SeeStep 5: Upload your profilefor the UI and command-line instructions.

## Profile RMSNorm

For this first analysis, you profile RMSNorm, a small operation with a clear sequence of arithmetic and reduction operations.

You profile three implementations of the same operation:

1. Naive RMSNorm with individual PyTorch operations: multiply, mean, add, reciprocal square root, and multiply.
2. torch.rms_norm(), the PyTorch built-in lowered to a single fused Neuron kernel.
3. Naive RMSNorm withtorch.compile, using the same operations as the first implementation.

The scripts use the same inputs, profiler configuration, and schedule so the results are directly comparable.

All scripts to reproduce this work are available in thetorch-neuronxexamples directory.

## Profile 1: Naive PyTorch Operations

Start by writing RMSNorm with individual PyTorch operations. Each line maps to one or more ATen operations and can create intermediate tensors.

```python
device = torch.device('neuron')

x = torch.randn(4, 512, dtype=torch.bfloat16, device=device)
weight = torch.ones(512, dtype=torch.bfloat16, device=device)

def rms_norm_fn(t):
    x_sq = t * t                                    
    mean_sq = x_sq.mean(dim=-1, keepdim=True)       
    rms = torch.rsqrt(mean_sq + 1e-6)               
    return t * rms * weight                         

```

Call the profiler with two arguments required for the Neuron backend:

1. IncludeProfilerActivity.PrivateUse1to collect activity from the Neuron device.
2. PassNeuronConfigasexperimental_configto enable the Neuron-specific Kineto features.

The schedule useswait=2,warmup=1, andactive=1across fourprof.step()calls. This records one warm iteration without including initial setup overhead.

Calltorch.neuron.synchronize()inside the profiler loop. Without this synchronization, the profiler can export before the device finishes and leave the Neuron time column empty.

```python
with torch.profiler.profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.PrivateUse1],
    experimental_config=nc,
    record_shapes=False,
    on_trace_ready=exporter.export_trace,
    schedule=torch.profiler.schedule(wait=2, warmup=1, active=1),
) as prof:
    for step in range(4):
        with torch.no_grad():
            _ = rms_norm_fn(x)
        torch.neuron.synchronize()
        prof.step()

```

After profiling finishes, inspect thekey_averages()table. Sort byself_privateuse1_time_totalto place the operations with the highest device cost first. The table shown here is filtered to the RMSNorm operations that report Neuron device time. The fullkey_averages()output also includes CPU-side events such as allocations and host-to-device transfers.

```python
print(prof.key_averages().table(sort_by="self_privateuse1_time_total", row_limit=4))

```

The key averages table shows that three aten::mul calls account for the largest share of Neuron device time.

The table shows which ATen operations ran, how often they ran, and how much time they spent on the CPU and Neuron device.aten::mulhas the highest total device time because the function performs three multiplications.

Self NEURON total: 2.355 ms

Each row maps directly to the function.aten::mulruns forx * x,x * rms, and the final multiplication byweight.aten::meanreduces the last dimension.aten::addadds the epsilon value and triggers a host-to-device copy because the scalar starts on the CPU.aten::rsqrtcomputes the reciprocal square root.

![Neuron Explorer follows an aten::mul operation from framework dispatch through runtime scheduling to execution on the Neuron hardware lanes.](/images/posts/c610c56d4453.png)

Neuron Explorer follows an aten::mul operation from framework dispatch through runtime scheduling to execution on the Neuron hardware lanes.

### Read the Trace in Explorer

In Explorer, time flows from left to right and the event lifecycle flows from top to bottom. Each ATen operation follows the same pattern: creation in the framework lane, scheduling in the runtime lane asnrta_execute_schedule, and device execution in the hardware lane asnc_exec_running.

[翻译失败，原文如下]

The system trace view organizes events into lanes. In the Default grouping mode, labels follow the pattern instance/PID/subsystem/identifier:

In eager mode, each operation runs independently. Use the dependency chain viewer to followaten::mul.Tensorfrom the framework layer through runtime scheduling to device execution.

![The dependency chain viewer highlights the lifecycle of one operation across the framework, runtime, and hardware lanes.](/images/posts/eef340544bee.gif)

The dependency chain viewer highlights the lifecycle of one operation across the framework, runtime, and hardware lanes.

## Profile 2: torch.rms_norm

Replace the individual operations with PyTorch's built-inrms_normfunction. Neuron lowers the operation to one fused kernel:

```python
def rms_norm_fn(t):
    return torch.rms_norm(t, [512], weight)

```

![The fused RMSNorm appears as one device operation in the key averages table.](/images/posts/5b058c104679.png)

The fused RMSNorm appears as one device operation in the key averages table.

Self NEURON total: 403.3 μs

![The fused RMSNorm follows one framework-to-hardware path instead of dispatching each arithmetic operation separately.](/images/posts/644616538609.png)

The fused RMSNorm follows one framework-to-hardware path instead of dispatching each arithmetic operation separately.

### Compare the Lowering Path

In the naive implementation, each operation crosses the dispatch boundary independently and follows its own framework-to-runtime-to-hardware path. In the fused implementation, one Python call covers the complete computation. The trace contains one dispatch and one hardware event, with no gaps between component operations.

## Profile 3: Naive PyTorch with torch.compile

For the final example, compile the original naive RMSNorm function withtorch.compile.

With@torch.compile(backend="neuron"), TorchDynamo captures the Python bytecode as an FX graph and AOTAutograd lowers it to ATen operations. The Neuron backend receives the complete graph instead of dispatching each operation separately. It fuses the operations, optimizes memory access, and compiles the graph into a single NEFF artifact. The artifact runs as one hardware dispatch.

```python
@torch.compile(backend='neuron', fullgraph=True)
def naive_compiled(t):
    x_sq = t * t
    mean_sq = x_sq.mean(dim=-1, keepdim=True)
    rms = torch.rsqrt(mean_sq + 1e-6)
    return t * rms * weight

```

![The compiled function appears as one Torch-Compiled Region in the key averages table.](/images/posts/8bc276a18c86.png)

The compiled function appears as one Torch-Compiled Region in the key averages table.

Self NEURON total: 375.5 μs

![The compiled graph follows one path through runtime scheduling and hardware execution.](/images/posts/82eff3e27e2e.png)

The compiled graph follows one path through runtime scheduling and hardware execution.

The table shows one device execution, as in Profile 2, but the code takes a different path. Instead of calling a purpose-built fused operation, the compiler discovers the fusion from the original Python function. In this run, the Neuron time is comparable totorch.rms_norm, at 375 μs compared with 403 μs.

## Side-by-Side Summary

Bothtorch.rms_normandtorch.compilefuse RMSNorm into one kernel dispatch. In these runs, either approach takes about one-sixth of the naive implementation's device time. Fusion removes the gaps between hardware executions and avoids materializing intermediate values such asx_sqandmean_sqbetween separately dispatched operations.

## Conclusion

key_averages()shows which operations consume device time, while its full output also reveals CPU-side setup and transfers. Explorer provides the corresponding visual trace. You can follow one operation from framework dispatch through runtime scheduling to hardware execution and see the gaps that fusion removes.

You can use the same workflow on larger models: find a hotspot in the table, verify it in the trace, and then determine whether a fused operation ortorch.compilecan reduce its cost.

In Part 2, we will move into the device-level profile. You open the NEFF, inspect the TensorEngine, VectorEngine, and direct memory access (DMA) breakdown, and place the kernel on the roofline to determine whether it is compute-bound or memory-bound.

Special thanks to Aritra Roy Gosthipaty for the inspiration to begin this series, and to my peers Pinak Panigrahi, Samir Araujo, Akhil Azhikodan, Esha Lakhotia and the rest for reviewing!

---

> 本文由AI自动翻译，原文链接：[Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium.](https://huggingface.co/blog/amazon/profiling-torchneuron-part-1)
> 
> 翻译时间：2026-10-22 06:55
