#!/bin/bash
echo "🔧 Building AI Image Generator..."

mkdir -p build

cmake -B build -DWITH_HF_TOKEN=ON -DHF_TOKEN=$1

cmake --build build --target build_full

echo "✅ Build completed!"
echo "📁 Executables are in: build/dist/ and build/src_dist/"