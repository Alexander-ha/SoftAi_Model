from diffusers import AutoPipelineForText2Image
import torch
import sys

def generator_func(prompt, path_to_save, seed=37):
    try:
        print("📥 Loading model...")
        
        if torch.cuda.is_available():
            device = "cuda"
            torch_dtype = torch.float16
            print("🔥 Using CUDA (fast)")
        else:
            device = "cpu" 
            torch_dtype = torch.float32
            print("🐌 Using CPU (slow)")
        
        pipe_txt2img = AutoPipelineForText2Image.from_pretrained(
            "dreamlike-art/dreamlike-photoreal-2.0", 
            torch_dtype=torch_dtype,
            use_safetensors=True
        ).to(device)

        print("🎨 Generating image...")
        generator = torch.Generator(device=device).manual_seed(seed)
        
        image = pipe_txt2img(
            prompt, 
            generator=generator,
            num_inference_steps=20
        ).images[0]
        
        print(f"💾 Saving image to {path_to_save}")
        image.save(path_to_save)
        
    except torch.cuda.OutOfMemoryError:
        print("❌ CUDA out of memory! Try with --cpu flag or reduce image size")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Generation error: {e}")
        sys.exit(1)