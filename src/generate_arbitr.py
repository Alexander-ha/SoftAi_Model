from diffusers import AutoPipelineForText2Image
import torch
import sys
import os

def generator_func(prompt, path_to_save, seed=37):
    try:
        print("Loading model...")
        
        hf_token = None
        token_files = [
            os.path.join(os.path.dirname(__file__), '..', 'venv', 'hf_token.txt'),
            os.path.join(os.path.dirname(__file__), '.huggingface', 'token'),
            os.path.expanduser('~/.huggingface/token')
        ]
        
        for token_file in token_files:
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    hf_token = f.read().strip()
                print("Using Hugging Face token from file")
                break
        
        if not hf_token and 'HUGGINGFACE_HUB_TOKEN' in os.environ:
            hf_token = os.environ['HUGGINGFACE_HUB_TOKEN']
            print("Using Hugging Face token from environment")
        
        if torch.cuda.is_available():
            device = "cuda"
            torch_dtype = torch.float16
            print("Using CUDA")
        else:
            device = "cpu" 
            torch_dtype = torch.float32
            print("Using CPU")
        
        print("Downloading model...")
        
        if hf_token:
            pipe = AutoPipelineForText2Image.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch_dtype,
                use_safetensors=True,
                use_auth_token=hf_token
            )
        else:
            pipe = AutoPipelineForText2Image.from_pretrained(
                "runwayml/stable-diffusion-v1-5", 
                torch_dtype=torch_dtype,
                use_safetensors=True
            )
        
        pipe = pipe.to(device)
        print("Model loaded successfully")

        print("Generating image...")
        generator = torch.Generator(device=device).manual_seed(seed)
        
        image = pipe(
            prompt=prompt,
            generator=generator,
            num_inference_steps=20,
            height=512,
            width=512
        ).images[0]
        
        print(f"Saving image to {path_to_save}")
        image.save(path_to_save)
        print("Image saved successfully")
        
    except torch.cuda.OutOfMemoryError:
        print("CUDA out of memory! Trying with smaller image...")
        try:
            image = pipe(
                prompt=prompt,
                generator=generator,
                num_inference_steps=15,
                height=256,
                width=256
            ).images[0]
            image.save(path_to_save)
            print("Image generated with smaller size")
        except Exception as e2:
            print(f"Generation failed: {e2}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def test_imports():
    try:
        import torch
        import diffusers
        print("All imports successful")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()