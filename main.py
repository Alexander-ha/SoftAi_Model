import argparse
import sys
import os
import torch

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from generate_arbitr import generator_func

def check_cuda():
    """Проверяет доступность CUDA"""
    cuda_available = torch.cuda.is_available()
    if cuda_available:
        print(f"✅ CUDA is available: {torch.cuda.get_device_name(0)}")
        print(f"✅ CUDA version: {torch.version.cuda}")
    else:
        print("⚠️  CUDA is not available - using CPU (slow!)")
    return cuda_available

def main():
    parser = argparse.ArgumentParser(description='AI Image Generator with CUDA support')
    parser.add_argument('prompt', type=str, help='Text prompt for image generation')
    parser.add_argument('output_path', type=str, help='Path to save generated image')
    parser.add_argument('--seed', type=int, default=37, help='Random seed (default: 37)')
    parser.add_argument('--cpu', action='store_true', help='Force CPU usage (ignore CUDA)')
    
    args = parser.parse_args()
    
    print("🤖 AI Image Generator Starting...")
    print("=" * 50)
    
    if not args.cpu:
        cuda_available = check_cuda()
    else:
        print("🔧 CPU mode forced by user")
        cuda_available = False
    
    print(f"🎨 Prompt: {args.prompt}")
    print(f"💾 Output: {args.output_path}")
    print(f"🎲 Seed: {args.seed}")
    print("=" * 50)
    
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    
    try:
        print("🚀 Generating image...")
        generator_func(args.prompt, args.output_path)
        print(f"✅ Image successfully saved to: {args.output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()