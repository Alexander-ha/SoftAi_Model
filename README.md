# SoftAI Model

A comprehensive AI image generation platform that provides flexible access to state-of-the-art Diffusion models through both command-line interface and web application.

## 🌟 Features

- **Text-to-Image Generation**: Create stunning images from text prompts using Stable Diffusion
- **Web Interface**: User-friendly Flask web application with real-time generation
- **Multiple Generation Modes**: Pre-configured scripts for cakes, cats, dogs, and arbitrary prompts
- **Cross-Platform Executables**: Build standalone applications for Windows and Linux
- **CI/CD Pipeline**: Automated testing with GitHub Actions
- **CUDA Support**: GPU acceleration for faster generation (with fallback to CPU)
- **Hugging Face Integration**: Secure token-based model access

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- CMake 3.28+
- Git

### Installation

#### Automatic Build (Recommended)
**Windows:**
```bash
build.bat [your_huggingface_token]
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh [your_huggingface_token]
```

#### Manual Installation
```bash
# Clone repository
git clone https://github.com/your-username/SoftAI_model.git
cd SoftAI_model

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Web Interface (Recommended)
```bash
python main.py --port 8001
```
Then open http://localhost:8001 in your browser.

### Command Line Generation
```bash
# Generate from text prompt
python main.py --prompt "beautiful sunset over mountains" --output_path output.png

# Force CPU usage
python main.py --prompt "cute puppy" --output_path dog.png --cpu

# Custom seed
python main.py --prompt "abstract art" --output_path art.png --seed 123
```

### Pre-configured Scripts
```bash
# Generate specific categories
python src/generate_cake.py
python src/generate_cat.py  
python src/generate_dog.py
python src/generate_arbitr.py
```

## 🔧 Advanced Build Options

### Building Executables
The project supports building standalone executables:

```bash
# Build all executables
cmake --build build --target build_src_exe

# Build specific executable
cmake --build build --target build_generate_cake
```

### Available Build Targets:
- `build_generate_cake` - Cake image generator
- `build_generate_cat` - Cat image generator  
- `build_generate_dog` - Dog image generator
- `build_generate_arbitr` - Arbitrary prompt generator
- `build_full` - Complete build with all components

## 🐳 Docker Support

### Building Docker Image
```bash
docker build -t ai-image-generator .
```

### Running with Docker
```bash
docker run -p 8001:8001 -e HUGGINGFACE_HUB_TOKEN=your_token_here ai-image-generator

docker run -it -p 8001:8001 -e HUGGINGFACE_HUB_TOKEN=your_token_here ai-image-generator /bin/bash

docker run -p 8001:8001 \
  -e HUGGINGFACE_HUB_TOKEN=your_token_here \
  -v $(pwd)/static/generated:/app/static/generated \
  -v $(pwd)/static/uploads:/app/static/uploads \
  ai-image-generator```

```

### Token File
Place your token in one of these locations:
- `venv/hf_token.txt`
- `.huggingface/token`
- `~/.huggingface/token`

## 🧪 Testing

### Run Test Suite
```bash
# Run all tests
python -m unittest discover -v

# Or use CMake test targets
cmake --build build --target test_src_scripts
```

### GitHub Actions
Tests automatically run on push and pull requests via:
```yaml
name: Run Unit Tests
on: [push, pull_request]
```

## 📁 Project Structure

```
SoftAI_Model/
├── src/                    # Core generation scripts
│   ├── generate_cake.py
│   ├── generate_cat.py
│   ├── generate_dog.py
│   └── generate_arbitr.py # Main generation module
├── web/                   # Web interface
│   ├── base.html
│   └── templates/
├── tests/                 # Test suite
│   ├── test_pipeline_txt_to_img.py
│   └── test_pipeline_txt_to_img.py
├── main.py               # Main application entry point
├── CMakeLists.txt        # Build configuration
├── build.bat            # Windows build script
├── build.sh             # Linux build script
└── requirements.txt     # Python dependencies
```

## 🛠️ Technical Details

### Supported Models
- **Primary**: `runwayml/stable-diffusion-v1-5`
- **Alternative**: `dreamlike-art/dreamlike-photoreal-2.0`

### Hardware Requirements
- **Minimum**: 8GB RAM, CPU-only
- **Recommended**: 16GB RAM, NVIDIA GPU with 8GB+ VRAM

### Performance Notes
- GPU generation: ~10-30 seconds per image
- CPU generation: ~2-5 minutes per image
- Image resolution: 512x512 (default), adjustable in code

## 🐛 Troubleshooting

### Common Issues

**CUDA Out of Memory:**
- Use `--cpu` flag for CPU-only mode
- Reduce image dimensions in `generate_arbitr.py`

**Model Download Errors:**
- Verify Hugging Face token
- Check internet connection
- Ensure sufficient disk space (~4GB for models)

**Build Failures:**
- Ensure CMake 3.28+ is installed
- Check Python version compatibility
- Verify all dependencies in `requirements.txt`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project uses the Stable Diffusion v1.5 model. Please ensure compliance with the model's license terms when using this software.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed description

## 🔄 Version Information

- **Current Version**: 1.0.0
- **Python**: 3.10+
- **PyTorch**: 2.1.2
- **Diffusers**: 0.26.0

---

**Happy Generating! 🎨**

