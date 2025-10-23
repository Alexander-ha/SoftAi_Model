@echo off
echo 🔧 Building AI Image Generator...

mkdir build 2>nul

cmake -B build -DWITH_HF_TOKEN=ON -DHF_TOKEN=%1
cmake --build build --target build_full

echo ✅ Build completed!
echo 📁 Executables are in: build\dist\ and build\src_dist\