# SoftAI Model

A flexible repository designed for simple access to Diffusion AI models. This project provides an easy-to-use framework for generating high-quality images using state-of-the-art text-to-image diffusion models.

## Features

- **Text-to-Image Generation**: Generate photorealistic images from text prompts
- **Multiple Generation Targets**: Pre-configured examples for cakes, cats, and dogs
- **Testing Suite**: Comprehensive unit tests to ensure model reliability
- **Cross-Platform**: Supports both native execution and Docker containerization
- **Automatic Dependency Management**: CMake-based virtual environment setup

## Installation Requirements

The project automatically handles dependency installation through CMake. Required packages include:
- PyTorch
- Diffusers
- Transformers
- Pillow
- And other AI/ML dependencies

## Compile and Run

### Prerequisites
- CMake 3.28 or higher
- Python 3.x
- CUDA-capable GPU (recommended) or CPU

### Building the Project

```bash
# Create build directory
mkdir build && cd build

# Configure with CMake
cmake ..

# Build the project
cmake --build .
```

### Running Generation Scripts

The project provides three main generation targets:

```bash
# Generate cake images
cmake --build . --target run_generate_cake

# Generate cat images
cmake --build . --target run_generate_cat

# Generate dog images
cmake --build . --target run_generate_dog
```

### Custom Generation

You can modify the prompt in any of the generation scripts (`generate_cake.py`, `generate_cat.py`, `generate_dog.py`) to create custom images:

```python
prompt = "your custom prompt here, professional, 4k, highly detailed"
```

## Run by Docker

### Building the Docker Image

```bash
docker build -t softai-model .
```

### Running with Docker

```bash
# Run with GPU support (recommended)
docker run --gpus all -it softai-model

# Run with CPU only
docker run -it softai-model
```

## Model Information

This project uses the **dreamlike-art/dreamlike-photoreal-2.0** model from Hugging Face, which is optimized for generating photorealistic images from text prompts.

## Testing

Run the test suite to verify the installation:

```bash
# Run all tests
ctest

# Or run Python tests directly
python -m pytest tests/
```

The test suite includes:
- Pipeline functionality verification
- Image generation consistency checks
- Prompt variation testing

## Project Structure

```
SoftAI_Model/
├── src/
│   ├── CMakeLists.txt        # Build configuration
│   ├── generate_cake.py      # Cake image generation
│   ├── generate_cat.py       # Cat image generation
│   ├── generate_dog.py       # Dog image generation
│   └── requirements.txt      # Python dependencies
├── tests/
│   └── test_pipeline.py      # Unit tests
└── CMakeLists.txt           # Build configuration
```

## Examples

The repository includes pre-configured examples for:
- **Cake Generation**: "3 tier black forest cake, professional, 4k, highly detailed"
- **Cat Generation**: "cute cat lying on the couch, professional, 4k, highly detailed"  
- **Dog Generation**: "cute dog playing with a ball in the yard, professional, 4k, highly detailed"

## License

This project is built upon the dreamlike-art/dreamlike-photoreal-2.0 model. Please check the respective model licenses for usage restrictions.

## Support

For issues and questions, please open an issue on the GitHub repository.
