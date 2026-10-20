---
title: 'TorchNeuron: running HF models on AWS Trainium is easier than ever'
title_original: 'TorchNeuron: running HF models on AWS Trainium is easier than ever'
date: '2026-10-19'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hf-torchneuron
author: ''
summary: '[翻译失败，原文如下]


  # TorchNeuron: running HF models on AWS Trainium is easier than ever


  TorchNeuron provides a new native backend for PyTorch on AWS Traini...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:15.261226'
---

[翻译失败，原文如下]

# TorchNeuron: running HF models on AWS Trainium is easier than ever

TorchNeuron provides a new native backend for PyTorch on AWS Trainium. Transformers, Diffusers and Kernels natively support it, making it easier than ever to run models on Trainium and to share them on the HF hub.

## TorchNeuron

TorchNeuronis a PyTorch plugin that brings a new backend for Trainium enabling support for eager mode,torch.compileand native distributed APIs like FSDP and TP.
Read the Pytorchblogto learn more about TorchNeuron.

Starting Oct. 20, 2026, TorchNeuron will be available as a public beta. Researchers and developers will be able to install it withpip install torch-neuronx.

## New backend, native interface in HF libraries

To date, the Hugging Face experience on AWS Trainium and Inferentia — AI chips designed respectively for cost-effective training and inference at scale — has been delivered throughoptimum-neuron. This library relies on the torch-neuronx package, which is based on PyTorch XLA. It was the natural choice at the time, but it meant thinking like a compiler: lazy tensors instead of eager execution, static shapes only, a recompilation for every graph break. Optimum Neuron existed to hide that complexity, and maintained custom code (modeling classes, trainers, etc) to do so.

TorchNeuron changes this. It integrates directly into PyTorch and exposesneuronas a native device, with eager execution, PyTorch's own distributed primitives (DTensor, FSDP2) andtorch.compile.

For the Hugging Face libraries, Trainium becomes a device like any other: Transformers, Diffusers, Accelerate, PEFT and TRL run on it directly, with the same classes and scripts you would use on any other accelerator. From now on, we recommend that Neuron users use these libraries directly instead of going through Optimum Neuron.

### Transformers

#### Inference

Text generation is now natively supported in Transformers for a wide range of models. With TorchNeuron, 89% of the top 100 most-used text-generation model architectures are supported out of the box, compared to 46% with Optimum Neuron v0.4.5. You just need to pass thedevice_map=neuronargument in your code and your model will be moved to the Neuron devices.

The following is an example of text-generation with tensor parallelism, which will enable to fully benefit from your Neuron instance. Note that it uses a static cache for generation as this is strongly recommended with Neuron to prevent frequent recompilations.

```py
import os

import torch
import torch.distributed as dist
import torch_neuronx  
from torch.distributed import DeviceMesh
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from transformers.distributed import DistributedConfig
from transformers.generation.configuration_utils import CompileConfig

MODEL_ID = "Qwen/Qwen3.8-27B"
MAX_SEQ_LEN = 1024
PREFILL_CHUNK_SIZE = 512

dist.init_process_group(backend="neuron")
world_size = dist.get_world_size()

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
    distributed_config=DistributedConfig(tp_size=world_size),
    device_mesh=DeviceMesh("neuron", list(range(world_size))),
).eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "left"

inputs = tokenizer.apply_chat_template(
    [{"role": "user", "content": "The future of AI is"}],
    add_generation_prompt=True,
    padding=True,
    tokenizer_kwargs={"pad_to_multiple_of": PREFILL_CHUNK_SIZE},
    return_tensors="pt",
)

generation_config = GenerationConfig(
    max_new_tokens=128,
    do_sample=False,
    use_cache=True,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id,
    cache_implementation="static",
    max_cache_len=MAX_SEQ_LEN,
    prefill_chunk_size=PREFILL_CHUNK_SIZE,
    compile_config=CompileConfig(backend="neuron", fullgraph=False, dynamic=False),
)

with torch.no_grad():
    output_ids = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        generation_config=generation_config,
    )

if dist.get_rank() == 0:
    prompt_len = inputs["input_ids"].shape[1]
    print(tokenizer.decode(output_ids[0, prompt_len:], skip_special_tokens=True))

```

#### Training

Now that Neuron is a native PyTorch device, training on Trainium uses the same Hugging Face libraries as any other accelerator: Transformers, Accelerate, PEFT and TRL. You no longer need a dedicated trainer or a Neuron-specific fork of the model code. A standard TRL fine-tuning script runs on a Trainium instance with only a few Neuron-specific settings.

Here is a supervised fine-tuning script built on TRL'sSFTTrainer. If you have fine-tuned a model with TRL on GPUs before, it should look familiar.

```py
import os

import torch
from datasets import load_dataset
from transformers.distributed import DistributedConfig

from trl import ModelConfig, ScriptArguments, SFTConfig, SFTTrainer, TrlParser


def main(script_args, training_args, model_args):
    
    torch._dynamo.config.automatic_dynamic_shapes = False

    training_args.model_init_kwargs = {
        "revision": model_args.model_revision,
        "trust_remote_code": training_args.trust_remote_code,
        "attn_implementation": model_args.attn_implementation,
        "dtype": model_args.dtype,
        "device_map": None,
    }
    if int(os.environ.get("WORLD_SIZE", "1")) > 1:
        
        training_args.model_init_kwargs["distributed_config"] = DistributedConfig(
            tp_size=int(os.environ.get("TP_SIZE", "1")),
            fsdp_size=int(os.environ.get("FSDP_SIZE", "1")),
        )

    
    train_dataset = load_dataset(
        script_args.dataset_name,
        name=script_args.dataset_config,
        split=script_args.dataset_train_split,
    )
    
    train_dataset = train_dataset.select_columns(["messages"])

    
    trainer = SFTTrainer(
        model=model_args.model_name_or_path,
        args=training_args,
        train_dataset=train_dataset,
    )

    trainer.train()
    trainer.save_model(training_args.output_dir)
    trainer.end()


if __name__ == "__main__":
    parser = TrlParser((ScriptArguments, SFTConfig, ModelConfig))
    script_args, training_args, model_args = parser.parse_args_and_config()
    main(script_args, training_args, model_args)

```

Parallelism is handled natively by Transformers. You put aDistributedConfigwith the tensor-parallel (TP) and FSDP sizes inmodel_init_kwargs,SFTTrainerpasses it tofrom_pretrained, and the model is sharded as its weights are loaded. The Trainer sees that the model is already distributed and does not wrap it again. You don't need an--fsdpflag or an Accelerate FSDP config.

Nothing in the script is tied to Trainium: the same code runs on any hardware. A few things are worth knowing when you run it on Trainium:

- Static shapes.The script disables automatic dynamic shapes intorch.compileand uses wrapped packing to produce sequences of up to 2048 tokens. With TRL ≥ 1.16, batches on Neuron are padded to a multiple of 128 tokens, limiting the number of input shapes. Compiled graphs are reused for subsequent steps with the same shapes.
- torch.compileon.Passing--torch_compile trueis all it takes: on a Trainium instance,torch.compiledetects the device and picks the Neuron backend automatically, with nothing else to configure.
- Async weight loading off.The built-in asynchronous weight loading in Transformers is not supported on Neuron, so for now we disable it withHF_DEACTIVATE_ASYNC_LOAD=1.

[翻译失败，原文如下]

The command below launches training withtorchrun, which starts one process per NeuronCore.TP_SIZEandFSDP_SIZEset the parallelism layout, and their product is the number of processes: here 4 x 8 = 32, matching--nproc_per_node. The 32 processes form a 4 x 8 grid. Tensor parallelism splits each layer across the 4 cores of a TP group, and FSDP shards the parameters, gradients and optimizer state across the 8 TP groups.

```sh
TP_SIZE=4 FSDP_SIZE=8 HF_DEACTIVATE_ASYNC_LOAD=1 uv run torchrun --nproc_per_node=32 sft_neuron_example.py \
    --model_name_or_path Qwen/Qwen3-8B \
    --dataset_name HuggingFaceH4/ultrachat_200k \
    --dataset_train_split train_sft \
    --output_dir Qwen3-8B-sft-tp4-fsdp8 \
    --dtype bfloat16 \
    --max_length 2048 \
    --packing true \
    --packing_strategy wrapped \
    --learning_rate 2e-5 \
    --warmup_steps 0.03 \
    --num_train_epochs 1 \
    --logging_steps 2 \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --save_only_model true \
    --torch_compile true

```

We ran it on 8 Trainium2 chips (32 NeuronCores), which is half atrn2.48xlargeinstance.

Training runs to completion, andtrainer.save_modelwrites a standard Transformers checkpoint. Nothing in it is tied to Neuron: you can push it to the Hugging Face Hub as is and load it on any other hardware.

### Diffusers

Many pipelines from the Diffusers library are compatible with TorchNeuron in eager and compiled mode. FLUX.1-dev, FLUX.2, Qwen-Image, Qwen-Image-2.1 and H3 are also compatible with tensor parallelism to make the most of your Neuron devices. The following is an example showing how you can use TP:

```py
import torch, torch.distributed as dist, torch_neuronx 
from torch.distributed.device_mesh import DeviceMesh 
from diffusers import QwenImage21Pipeline, QwenImage21Transformer2DModel, TensorParallelConfig


dist.init_process_group(backend="neuron") 
dev = torch.neuron.current_device()
mesh = DeviceMesh("neuron", list(range(8))) 


model = "Qwen/Qwen-Image-2.1"
transformer = QwenImage21Transformer2DModel.from_pretrained(
    model,
    subfolder="transformer",
    torch_dtype=torch.bfloat16,
    parallel_config=TensorParallelConfig(mesh=mesh), 
)
pipe = QwenImage21Pipeline.from_pretrained(
    model,
    transformer=transformer,
    torch_dtype=torch.bfloat16,
)
pipe.vae.to(dev)
pipe.transformer.compile_repeated_blocks(backend="neuron", fullgraph=True, dynamic=False)


emb, mask, _ = pipe.encode_prompt(prompt="A capybara wearing a wizard hat, oil painting", device="cpu")  
image = pipe(
    prompt_embeds=emb.to(dev),
    prompt_embeds_mask=mask.to(dev) if mask is not None else None,
    height=1024,
    width=1024,
    num_inference_steps=40,
    generator=torch.Generator("cpu").manual_seed(0), 
).images[0]
if dist.get_rank() == 0:
    image.save("out.png")

```

You can run this piece of code with:NEURON_LOGICAL_NC_CONFIG=2 torchrun --nproc_per_node=8 run.py.

More and more pipleines will be compatible with TP. If a pipeline you like is not, you can also add support for it followingthis guide.

### Kernels

Make sure to check out thekernels from the Neuron teamas more and more Neuron kernels will become available on the Hub to speed up your models.
Neuron kernels can be written using theNeuron Kernel Interface(NKI), which gives lower control to optimize operations. This way, users can run their own custom operations and share them on the hub.

You can use for examplethis kernelto speed up your vision transformers with up to a x2.4 speedup on Trainium!

![](/images/posts/54177f53909a.png)

## Acknowledgments

Special thanks to the AWS team for their work on TorchNeuron and for their reactivity to our feedback to make the HF integration as good as possible.

---

> 本文由AI自动翻译，原文链接：[TorchNeuron: running HF models on AWS Trainium is easier than ever](https://huggingface.co/blog/hf-torchneuron)
> 
> 翻译时间：2026-10-20 07:22
