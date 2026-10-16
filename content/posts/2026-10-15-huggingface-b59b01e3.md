---
title: Welcome FLUX.3 Image Klein in Diffusers
title_original: Welcome FLUX.3 Image Klein in Diffusers
date: '2026-10-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/flux-3
author: ''
summary: '[翻译失败，原文如下]


  # Welcome FLUX.3 Image Klein in Diffusers: The latest open image generation model
  from Black Forest Labs


  Black Forest LabsFLUX.3 Image K...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:40:46.691825'
---

[翻译失败，原文如下]

# Welcome FLUX.3 Image Klein in Diffusers: The latest open image generation model from Black Forest Labs

Black Forest LabsFLUX.3 Image Klein is here, and it runs in Diffusers from day one. One model does text-to-image and multi-reference image-to-image, and it adds something new, thelayout control. You write bounding boxes into the prompt to say where each part of the image should go, or which parts of a reference image to move.

Both open checkpoints are in theFLUX.3 Image Klein collection:

![a red fox in a snowy forest (text-to-image), the same fox re-rendered from that image (image-to-image), a black stippled running silhouette on a chartreuse background, drawn inside its labeled bounding box, and a knitted knight moved from a "from" box to a "to" box next to a knitted dragon (layout editing)](/images/posts/25df1984a8e4.png)

You can head on to theHugging Face spaceand generate some images right now!

## TL;DR

- One model for text-to-image, multi-reference image-to-image, and bounding-box layout control.
- The distilled checkpoint makes a 1024 × 1024 image in about2 secondson an H100.
- NVFP4 and FP8 weights load withfrom_single_file, for smaller GPUs.
- LoRA training scripts for both text-to-image and image editing.
- Ships as aModular Diffuserspipeline, so you can pop blocks out or add your own.

## Contents

- Getting started
- What FLUX.3 can do
- Base model and quantized variants
- LoRA finetuning
- What it costs to run
- The architecture
- Modular Diffusers
- Try it

## Getting started

Install the latestdiffusersandtransformers(for the Qwen3-VL text encoder):

```bash
pip install -U diffusers transformers

```

Load the distilled checkpoint and generate an image:

```python
import torch
from diffusers import ModularPipeline

pipe = ModularPipeline.from_pretrained("black-forest-labs/flux-3-image-klein")
pipe.load_components(dtype=torch.bfloat16)
pipe.to("cuda")

pipe(prompt="a red fox", output="images")[0].save("fox.png")

```

## What FLUX.3 can do

### Text-to-image

FLUX.3 responds best to a full scene description with the subject, the setting, the light, the composition, and the style. Theofficial prompting guidefrom Black Forest Labs has more tips. The distilled checkpoint generates a1024 × 1024image in16steps by default. Passheight,width, ornum_inference_stepsto change them.

```python
prompt = (
    "A wide-angle wildlife photograph of a red fox standing alert in a snow-covered forest clearing at golden hour. "
    "The fox is centered in the frame, its thick orange winter coat contrasting with the fresh white snow, breath "
    "visible in the cold air. Snow-laden pine trees fill the softly blurred background, and low warm sunlight rakes "
    "across the scene from the left, casting long blue shadows."
)

fox = pipe(
    prompt=prompt,
    generator=torch.Generator().manual_seed(0),
    output="images"
)[0]
fox.save("fox.png")

```

![A red fox standing alert in a snow-covered forest clearing, lit by low golden sunlight from the left](/images/posts/2350bdd0feb8.png)

### Image-to-image

Pass a reference image (or more) with theimageargument. Write the prompt as a caption of the image youwant, with the change included.

```python
prompt = (
    "The same red fox in the same snow-covered forest clearing, now at night under a full moon: cool blue "
    "moonlight, deep shadows, stars visible through the pine branches, the fox's eyes catching the light."
)
night = pipe(
    prompt=prompt,
    image=fox, 
    generator=torch.Generator().manual_seed(0),
    output="images",
)[0]
night.save("night.png")

```

![The fox from the previous image, relit in cold blue light](/images/posts/e440595ccaf8.png)

With several references, refer to them in the prompt as<ref_image_0>,<ref_image_1>, ... in the order they are passed toimage:

```python
red_fox = pipe(prompt="a red fox", generator=torch.Generator().manual_seed(0), output="images")[0]
bench = pipe(prompt="a wooden bench", generator=torch.Generator().manual_seed(0), output="images")[0]

combined = pipe(
    prompt="The fox from <ref_image_0> sitting on the wooden bench from <ref_image_1> in a snowy setting.",
    image=[red_fox, bench],
    output="images",
)[0]

combined.save("combined.png")

```

![A red fox sitting on dry grass](/images/posts/6aab69c75adb.png)

![A slatted wooden bench against a plain grey wall](/images/posts/879da59e5f3e.png)

![The same fox sitting on the same bench, with snow on the ground](/images/posts/f70da0331d09.png)

### Layout control

Add a JSON list of regions after the caption. Each region has anid, abbox, and adesc, and the caption mentions it as<id>.

Boxes are written as[y_min, x_min, y_max, x_max],y first, on a 0–1000 scale. Because the scale is normalized, the same box works at any image size.

#### Placing regions in a new image

```python
layout_prompt = (
    "Minimalist graphic illustration featuring a black silhouette of a person <silhouette_1> centered against a "
    "solid, vibrant chartreuse background <background_1>. The figure is captured in a dynamic, mid-stride running "
    "pose, facing toward the left side of the frame. "
    '[{"id": "background_1", "bbox": [0, 0, 1000, 1000], "desc": "A flat field of neon yellow-green with a subtle '
    'paper texture and fine, organic grain."}, {"id": "silhouette_1", "bbox": [150, 150, 850, 850], "desc": "A '
    "black silhouette of a person in motion, made of dense stippled ink. The leading edges are solid; the trailing "
    'arm and leg dissolve into coarse square pixels and scattered dots."}]'
)

runner = pipe(prompt=layout_prompt, generator=torch.Generator().manual_seed(0), output="images")[0]

```

![Diagram: the caption and the two region descriptions on the left, the two boxes on a 0–1000 grid in the middle, and the generated image on the right, where a black stippled runner fills the silhouette box on a chartreuse background](/images/posts/f8294d64fe26.png)

#### Moving regions within a reference image

For edits, each region says where its content comesfrom(src_bboxin the reference) and where it goes (tgt_bboxin the output). A region with the same two boxes stays where it is.

This example moves the knitted knight up and to the left, and pins the backdrop, the cliff, the needle, the dragon, and the fire:

```python
from diffusers.utils import load_image

knight_image = load_image("knight_orig.png")
edit_prompt = (
    "In <ref_image_0>, move the miniature grey amigurumi knight figure <knight_1> upwards and to the left along the "
    "yarn cliff <cliff_1>. Keep the rest of the image completely unchanged, preserving the blurred yarn backdrop "
    "<backdrop_1>, the large knitted dragon <dragon_1>, and the fiery orange thread <fire_1>. "
    '[{"id": "knight_1", "from": "ref_image_0", "src_bbox": [500, 150, 850, 350], "tgt_bbox": [194, 55, 544, 255], '
    '"desc": "A miniature amigurumi knight crocheted from thick grey woolen yarn."}, '
    '{"id": "backdrop_1", "from": "ref_image_0", "src_bbox": [0, 0, 1000, 1000], "tgt_bbox": [0, 0, 1000, 1000], '
    '"desc": "A soft, out-of-focus backdrop of cream and indigo knitted yarn."}, '
    '{"id": "cliff_1", "from": "ref_image_0", "src_bbox": [300, 0, 1000, 450], "tgt_bbox": [300, 0, 1000, 450], '
    '"desc": "A steep cliff of stacked yarn skeins in mustard, terracotta, and indigo."}, '
    '{"id": "needle_1", "from": "ref_image_0", "src_bbox": [420, 250, 550, 450], "tgt_bbox": [420, 250, 550, 450], '
    '"desc": "An oversized polished steel tapestry needle."}, '
    '{"id": "dragon_1", "from": "ref_image_0", "src_bbox": [100, 600, 950, 1000], "tgt_bbox": [100, 600, 950, 1000], '
    '"desc": "A large, fluffy knitted dragon in terracotta and mustard yarn."}, '
    '{"id": "fire_1", "from": "ref_image_0", "src_bbox": [350, 400, 650, 650], "tgt_bbox": [350, 400, 650, 650], '
    '"desc": "Curled puffs of fiery orange angora thread suspended in mid-air."}]'
)

[翻译失败，原文如下]

moved = pipe(prompt=edit_prompt, image=knight_image, generator=torch.Generator().manual_seed(0), output="images")[0]

```

## Base model and quantized variants

### Base model

Everything above uses the distilled checkpoint. The base checkpoint runs 50 steps with classifier-free guidance, and it's the one to fine-tune (seeLoRA finetuning).

```python
pipe = ModularPipeline.from_pretrained("black-forest-labs/flux-3-image-klein-base")
pipe.load_components(dtype={"vae": torch.float32, "default": torch.bfloat16})
pipe.to("cuda")

pipe.guider = pipe.guider.new(guidance_scale=5.0)  
image = pipe(prompt=prompt, output="images")[0]

```

### Single-file format checkpoints

Black Forest Labs also ships the transformer as a single file, inbf16and in two quantized formats:fp8r(rowwise FP8) andnvfp4. Load any of them withfrom_single_file, then load the other components by name so the bf16 transformer isn't downloaded too.

```python
from diffusers import BFLQuantizationConfig, Flux3Transformer2DModel, ModularPipeline

model_id = "black-forest-labs/flux-3-image-klein-base"
variant = "fp8r"  

transformer = Flux3Transformer2DModel.from_single_file(
    f"https://huggingface.co/{model_id}/blob/main/variants/{variant}/model.safetensors",
    config=model_id,
    subfolder="transformer",
    quantization_config=BFLQuantizationConfig(compute_dtype=torch.bfloat16),
    dtype=torch.bfloat16,
)

pipe = ModularPipeline.from_pretrained(model_id)
pipe.load_components(dtype=torch.bfloat16)
pipe.update_components(transformer=transformer)
pipe.to("cuda")

```

For the unquantized single file, usehttps://huggingface.co/{model_id}/blob/main/model.safetensorsand dropquantization_config.

## LoRA finetuning

FLUX.3 works for both text-to-image and image-to-image, which makes it a great base for custom LoRAs.diffusersships DreamBooth LoRA training scripts for both tasks (you can also train withOstris' AI Toolkit).

Here is a text-to-image example that learns a tarot-card style from themultimodalart/1920-raider-waite-tarot-public-domaindataset, triggered withtrtcrd:

```bash
accelerate launch train_dreambooth_lora_flux3_klein.py \
  --pretrained_model_name_or_path="black-forest-labs/flux-3-image-klein-base" \
  --dataset_name="multimodalart/1920-raider-waite-tarot-public-domain" \
  --caption_column="caption" \
  --instance_prompt="trtcrd" \
  --output_dir="trained-flux3-tarot-lora" \
  --mixed_precision="bf16" \
  --resolution=1024 \
  --use_aspect_ratio_buckets \
  --train_batch_size=1 \
  --rank=16 \
  --lora_alpha=16 \
  --learning_rate=1e-4 \
  --lr_scheduler="constant" \
  --max_train_steps=1500 \
  --validation_prompt="a trtcrd of a cat, tarot style" \
  --validation_epochs=25 \
  --seed=0 \
  --push_to_hub

```

To reduce memory usage, add a few optimization flags:

```bash
  --gradient_checkpointing \
  --cache_latents \
  --use_8bit_adam

```

--gradient_checkpointingrecomputes activations in the backward pass (lower VRAM, slightly slower),--cache_latentspre-encodes the images and frees the VAE, and--use_8bit_adamkeeps the optimizer states in 8-bit.

A couple of knobs are worth experimenting with. The grid below trains the same tarot style with different LoRA ranks and optimizers; the adapters are on the Hub atdiffusers-modular/flux3-tarot-lora. More training features and configurations are documented in theDreamBooth FLUX.3 README.

![FLUX.3 tarot-style LoRA across ranks and optimizers: the base model with no LoRA, then rank 16, rank 8 and rank 32 (AdamW, lr 1e-4) and a Prodigy run, on two held-out prompts](/images/posts/6cde44f6232d.png)

For instruction-based editing, the image-to-image script (train_dreambooth_lora_flux3_klein_img2img.py) trains on (reference image, target image, instruction) triplets, where the reference is addressed in the prompt as<ref_image_0>.

See theDreamBooth FLUX.3 READMEfor all options and the full image-to-image example.

## What it costs to run

In this section, we will talk about the memory consumption and the speed of generation of the models.

### Memory

If you have less memory:

- Load aquantized transformer.
- Run the text encoder separately and free it. It only runs once per image, before denoising (seeEncode once, generate many).
- Turn on automatic CPU offloading, which moves each component to the GPU only while it runs (we didn't benchmark this)

```python
from diffusers import ComponentsManager, ModularPipeline

manager = ComponentsManager()
manager.enable_auto_cpu_offload(device="cuda")

pipe = ModularPipeline.from_pretrained("black-forest-labs/flux-3-image-klein", components_manager=manager)
pipe.load_components(dtype={"vae": torch.float32, "default": torch.bfloat16})


```

### Speed

End-to-end timings for the distilled checkpoint (16 steps), averaged over three runs after a warmup:

Single NVIDIA H100 80GB, no offloading, default attention backend.

A reference image roughly doubles the time. Reference tokens join the same sequence as the text and the image being generated, so a 1024 × 1024 reference adds 4,096 tokens to every transformer call

![Stacked bars of tokens per transformer call: text-to-image 4,256 tokens; image-to-image 8,272; layout text-to-image 4,336; layout image-to-image 8,800](/images/posts/f3c006c5b23c.png)

## The architecture

Let's open the model up, one piece at a time. The model takes three kinds of tokens:

1. text
2. thenoisy imagebeing generated
3. and optionalreference images

### From pixels to tokens

FLUX.3 is a latent-space flow model for image generation. This means that the denoiser takes latents as inputs and produces latents as outputs. We use a VAE to decode the latents back to pixels. FLUX.3 uses the same VAE architecture as Flux.2.

The FLUX.2 VAE compresses an image 8× in each direction into 32 channels, and then every 2 × 2 patch of that latent is packed into a single token with 128 channels.

Soone token covers a 16 × 16 pixel patch, and a 1024 × 1024 image becomes a 64 × 64 grid of 4,096 tokens. The noisy image starts as random noise of exactly that shape. A reference image goes through the same VAE encoder and packing, and keeps its own size.

### From prompt to tokens

The text encoder is Qwen3-VL, a vision-language model. FLUX.3 doesn't just take its last layer. It reads the hidden states ofeightof its 36 layers (layers 4, 8, …, 32) and stacks them, so each text token becomes a 8 × 2560 = 20,480-dimensional vector before a linear layer projects it to the transformer's width of 3072.

This gives the transformer features from several depths of the language model, not just its final layer. The prompt is padded to a multiple of 80 tokens, and the transformer attends to the padding too, which is why the pipeline takes one prompt per call.

### Two stages

The transformer processes the tokens in two stages:

1. Stage 1: per-mode blocks.Each stream goes through 5 blocks with its own weights. Text has its own blocks, the noisy image has its own, and the reference images have their own.
2. Stage 2: joint blocks.The streams are concatenated into one sequence,[text | image | reference], which goes through 28 blocks that share one set of weights.

The two stages differ inwho can attend to whom.

In stage 1, each stream only attends to itself, so each kind of token gets refined on its own terms first. In stage 2, everything attends to everything, where the image learns from the text and from the references. For comparison, FLUX.2's double-stream blocks also give text and image separate weights, but let them attend to each other from the start. FLUX.3 keeps the streams fully apart first, then merges them.

At the end, the text and reference tokens are simply dropped. Only the image tokens go through the output layers, which predict how to move them one step toward a clean image.

### Inside one block

Every block, in either stage, has the same shape. Attention and the MLP runin parallelon the same normalized input, and their sum is added back to the residual stream.

[翻译失败，原文如下]

Each block starts with a LayerNorm that has no learned scale or shift of its own. The scale, shift, and gate come from a timestep embedding instead (this is calledmodulation). Inside the attention, the queries and keys are RMS-normalized and get rotary position embeddings (RoPE), which we look at below.

In a joint block, all tokens share the same weights, but text, image, and reference tokens each get their own scale, shift, and gate.

```python
def block(x, shift, scale, gate):      
    h = layer_norm(x)                  
    h = (1 + scale) * h + shift
    q, k, v = to_q(h), to_k(h), to_v(h)
    q, k = rope(rms_norm(q)), rope(rms_norm(k))
    out = attention(q, k, v) + mlp(h)  
    return x + gate * out

```

### Every token gets its own timestep

In FLUX.1 and FLUX.2, one timestep embedding modulates every token. In FLUX.3, the modulation depends on the kind of token.

The noisy image tokens are modulated by the current timestept. The text and reference tokens are always modulated by timestep0, which means "clean, nothing to denoise here". So even a reference that looks almost the same as the output is marked as given context, not as something to generate.

The distilled checkpoint is aflow map. It is also told the timestep each step jumps to. That second timestep gets its own embedding, which is added to every token's modulation, so each of its 16 steps can make a larger jump.

### Positions in four dimensions

Attention on its own doesn't know where a token is (this phenomenon is called permutation equivariance). RoPE fixes that by rotating each query and key by an amount that depends on the token's position. FLUX.3 uses four position axes,(t, h, w, l)(timestep, height, width, length of sequence), and gives each one a quarter (32 dimensions) of every 128-dimensional attention head:

Text tokens line up alongl, like words in a sentence. The image and the references are 2D grids in(h, w), separated from each other alongl. Because a reference uses the same(h, w)coordinates as the output, "the same spot in the reference" has a precise meaning to the model, which is what thesrc_bbox/tgt_bboxediting relies on.

### The denoising loop

FLUX.3 is a flow-matching model. Generation starts from pure noise, and at each of the 50 steps the transformer predicts avelocity. This is the direction from noise toward a clean image. The scheduler takes one step along it.

At every step you can also read off the model's current guess of the final image. Decoding that guess at a few steps shows how the image takes shape:

![step01](/images/posts/673f702c0981.png)

![step05](/images/posts/d0046967efdc.png)

![step10](/images/posts/99f4c781ad0b.png)

![step15](/images/posts/f9b7765ca6cd.png)

![step25](/images/posts/e98fd020c6fe.png)

![step50](/images/posts/bfc5c9ffdba3.png)

The fox, its pose, and the light are already in place by step 10, while the noise level is still 0.97. The snow-laden branches and the texture of the fur only appear in the last few steps. FLUX.3's scheduler uses a large time shift (6.93), which keeps the noise level high for most of the run: 44 of the 50 steps happen above σ = 0.5. We built this figure by adding one small block to the pipeline, which brings us to Modular Diffusers.

If you are new to flow matching, we have a beginnerfriendly tutorialand avideofor you to understand how it works.

## Modular Diffusers

FLUX.3 ships as aModular Diffuserspipeline.

### See the workflows

You can list the workflows and print the exact blocks of each one, without loading any weights.

```python
from diffusers import Flux3AutoBlocks

blocks = Flux3AutoBlocks()
print(blocks.available_workflows)


print(list(blocks.get_workflow("text2image").sub_blocks))



```

get_workflow()resolves the auto branches and gives you the plain sequence of steps that will run.print(blocks.get_workflow("image_conditioned").doc)prints the components, inputs, defaults, and outputs of that workflow.

### Encode once, generate many

Pop the text encoder out, encode the prompt once, free it, and generate from the cached embeddings.

```python
import torch
from diffusers import ModularPipeline

model_id = "black-forest-labs/flux-3-image-klein-base"

blocks = ModularPipeline.from_pretrained(model_id).blocks
text_blocks = blocks.sub_blocks.pop("text_encoder")  

text_pipe = text_blocks.init_pipeline(model_id)
text_pipe.load_components(dtype=torch.bfloat16)
text_pipe.to("cuda")

state = text_pipe(prompt=prompt, negative_prompt="")  

prompt_embeds = state.get("prompt_embeds")
negative_prompt_embeds = state.get("negative_prompt_embeds")

del text_pipe
torch.cuda.empty_cache()

image_pipe = blocks.init_pipeline(model_id)  
image_pipe.load_components(dtype={"vae": torch.float32, "default": torch.bfloat16})
image_pipe.to("cuda")

for seed in range(3):
    image = image_pipe(
        prompt_embeds=prompt_embeds,
        negative_prompt_embeds=negative_prompt_embeds,
        generator=torch.Generator().manual_seed(seed),
        output="images",
    )[0]
    image.save(f"{seed}.png")

```

### Add a step inside the loop

The denoising figure above came from one extra block that records the model's guess of the clean image at every step:

```python
from diffusers.modular_pipelines import Flux3AutoBlocks, InputParam, ModularPipelineBlocks, OutputParam


class Flux3PreviewStep(ModularPipelineBlocks):
    model_name = "flux3"

    @property
    def inputs(self):
        return [InputParam("latents"), InputParam("noise_pred")]

    @property
    def intermediate_outputs(self):
        return [OutputParam("x0_previews", type_hint=list)]

    @torch.no_grad()
    def __call__(self, components, block_state, i, t):
        if i == 0:
            block_state.x0_previews = []
        sigma = t / 1000  
        block_state.x0_previews.append(block_state.latents - sigma * block_state.noise_pred)  
        return components, block_state


blocks = Flux3AutoBlocks()
denoise_loop = blocks.sub_blocks["denoise"].sub_blocks["text2image"].sub_blocks["denoise"]
denoise_loop.sub_blocks.insert("preview", Flux3PreviewStep(), 1)  

pipe = blocks.init_pipeline(model_id)
pipe.load_components(dtype={"vae": torch.float32, "default": torch.bfloat16})
pipe.to("cuda")

out = pipe(prompt=prompt, generator=torch.Generator().manual_seed(0), output=["x0_previews", "images"])

```

## Try it

- Models:FLUX.3 Image Klein collection
- Docs:FLUX.3 in Diffusers
- Fine-tune:DreamBooth LoRA scripts
- Prompting:Black Forest Labs prompting guide

Built something with FLUX.3? Share your LoRAs and pipelines on the Hub. We'd love to see them! 😎

---

> 本文由AI自动翻译，原文链接：[Welcome FLUX.3 Image Klein in Diffusers](https://huggingface.co/blog/flux-3)
> 
> 翻译时间：2026-10-16 06:40
