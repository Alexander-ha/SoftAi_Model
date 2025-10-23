import argparse
import sys
import os
import torch
import uuid
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from generate_arbitr import generator_func

def check_cuda():
    cuda_available = torch.cuda.is_available()
    if cuda_available:
        print(f"✅ CUDA is available: {torch.cuda.get_device_name(0)}")
        print(f"✅ CUDA version: {torch.version.cuda}")
    else:
        print("⚠️  CUDA is not available - using CPU (slow!)")
    return cuda_available

app = Flask(__name__)
 
upload_folder = os.path.join('static', 'uploads')
generated_folder = os.path.join('static', 'generated')
app.config['UPLOAD'] = upload_folder
app.config['GENERATED'] = generated_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

os.makedirs(upload_folder, exist_ok=True)
os.makedirs(generated_folder, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image = None
    prompt = ""
    
    if request.method == 'POST':
        if 'prompt' in request.form:
            prompt = request.form['prompt']
            seed = int(request.form.get('seed', 37))
            
            filename = f"generated_{uuid.uuid4().hex[:8]}.png"
            output_path = os.path.join(app.config['GENERATED'], filename)
            
            try:
                print(f"🎨 Generating image for prompt: {prompt}")
                generator_func(prompt, output_path, seed=seed)
                generated_image = filename
                print(f"✅ Image generated: {filename}")
            except Exception as e:
                print(f"❌ Error generating image: {e}")
                return render_template('index.html', 
                                     error=f"Error generating image: {str(e)}",
                                     prompt=prompt)
        
        elif 'img' in request.files:
            file = request.files['img']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD'], filename))
                return render_template('index.html', 
                                     uploaded_image=filename,
                                     prompt=prompt)
    
    return render_template('index.html', 
                         generated_image=generated_image,
                         prompt=prompt)

@app.route('/generate', methods=['POST'])
def generate_image():
    """API endpoint for image generation"""
    prompt = request.form['prompt']
    seed = int(request.form.get('seed', 37))
    
    filename = f"generated_{uuid.uuid4().hex[:8]}.png"
    output_path = os.path.join(app.config['GENERATED'], filename)
    
    try:
        generator_func(prompt, output_path, seed=seed)
        return {'success': True, 'image_url': f"/static/generated/{filename}"}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    parser = argparse.ArgumentParser(description='AI Image Generator with CUDA support')
    parser.add_argument('--prompt', type=str, help='Text prompt for image generation')
    parser.add_argument('--output_path', type=str, help='Path to save generated image')
    parser.add_argument('--seed', type=int, default=37, help='Random seed (default: 37)')
    parser.add_argument('--cpu', action='store_true', help='Force CPU usage (ignore CUDA)')
    parser.add_argument('--port', type=int, default=8001, help='Port to run Flask app on')
    
    args = parser.parse_args()
    
    if args.prompt and args.output_path:
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
            generator_func(args.prompt, args.output_path, seed=args.seed)
            print(f"✅ Image successfully saved to: {args.output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        print("🌐 Starting Flask web interface...")
        check_cuda()
        app.run(debug=True, port=args.port, host='0.0.0.0')

if __name__ == "__main__":
    main()