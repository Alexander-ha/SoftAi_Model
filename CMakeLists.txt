cmake_minimum_required(VERSION 3.28)
project(AISoft_Model VERSION 1.0.0 LANGUAGES)

option(WITH_HF_TOKEN "Enable Hugging Face token support" OFF)
set(HF_TOKEN "" CACHE STRING "Hugging Face API token")

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

if(CMAKE_CXX_COMPILER)
    enable_language(CUDA)
    find_package(CUDAToolkit)
    if(CUDAToolkit_FOUND)
        message(STATUS "CUDA found: ${CUDAToolkit_VERSION}")
    else()
        message(WARNING "CUDA not found! PyTorch will use CPU only.")
    endif()
else()
    message(WARNING "C++ compiler not found - skipping CUDA detection")
endif()

# Функция создания совместимого окружения
function(create_venv venv_dir)
    if(EXISTS ${venv_dir})
        message(STATUS "Virtual environment already exists in ${venv_dir}")
        return()
    endif()
    
    message(STATUS "Creating Python virtual environment...")
    execute_process(
        COMMAND ${Python3_EXECUTABLE} -m venv ${venv_dir}
        RESULT_VARIABLE venv_creation_ret_code
    )
    
    if(NOT venv_creation_ret_code EQUAL 0)
        message(FATAL_ERROR "Failed to create virtual environment!")
    endif()

    # Определяем пути
    if(WIN32)
        set(PIP_PATH "${venv_dir}/Scripts/pip.exe")
        set(PYTHON_PATH "${venv_dir}/Scripts/python.exe")
    else()
        set(PIP_PATH "${venv_dir}/bin/pip")
        set(PYTHON_PATH "${venv_dir}/bin/python")
    endif()

    # Ждем создания виртуального окружения
    execute_process(COMMAND ${CMAKE_COMMAND} -E sleep 2)

    # Обновляем pip
    message(STATUS "Upgrading pip...")
    execute_process(
        COMMAND ${PIP_PATH} install --upgrade pip
        RESULT_VARIABLE pip_upgrade_ret_code
        OUTPUT_QUIET
        ERROR_QUIET
    )

    # Устанавливаем совместимые версии поэтапно
    message(STATUS "Step 1: Installing compatible NumPy...")
    execute_process(
        COMMAND ${PIP_PATH} install "numpy<2"
        RESULT_VARIABLE numpy_install_ret_code
        TIMEOUT 120
    )
    
    if(NOT numpy_install_ret_code EQUAL 0)
        message(FATAL_ERROR "Failed to install NumPy")
    endif()
    message(STATUS "NumPy installed")

    message(STATUS "Step 2: Installing PyTorch with compatible versions...")
    execute_process(
        COMMAND ${PIP_PATH} install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu
        RESULT_VARIABLE torch_install_ret_code
        TIMEOUT 300
    )
    
    if(NOT torch_install_ret_code EQUAL 0)
        message(FATAL_ERROR "Failed to install PyTorch")
    endif()
    message(STATUS "PyTorch installed")

    message(STATUS "Step 3: Installing compatible Hugging Face ecosystem...")
    execute_process(
        COMMAND ${PIP_PATH} install "huggingface-hub==0.19.4" "diffusers==0.24.0" "transformers==4.35.2"
        RESULT_VARIABLE hf_install_ret_code
        TIMEOUT 300
    )
    
    if(NOT hf_install_ret_code EQUAL 0)
        message(FATAL_ERROR "Failed to install Hugging Face packages")
    endif()
    message(STATUS "Hugging Face packages installed")

    message(STATUS "Step 4: Installing web dependencies...")
    execute_process(
        COMMAND ${PIP_PATH} install flask==2.3.3 werkzeug==2.3.7 pillow==9.5.0
        RESULT_VARIABLE web_install_ret_code
        TIMEOUT 180
    )
    
    if(NOT web_install_ret_code EQUAL 0)
        message(FATAL_ERROR "Failed to install web dependencies")
    endif()
    message(STATUS "Web dependencies installed")

    message(STATUS "Step 5: Installing additional dependencies...")
    execute_process(
        COMMAND ${PIP_PATH} install "accelerate==0.24.1" "safetensors==0.4.1" "pyinstaller==5.13.2"
        RESULT_VARIABLE additional_install_ret_code
        TIMEOUT 180
    )
    
    if(NOT additional_install_ret_code EQUAL 0)
        message(FATAL_ERROR "Failed to install additional dependencies")
    endif()
    message(STATUS "Additional dependencies installed")

    # Создаем файл для финальной проверки
    file(WRITE ${CMAKE_BINARY_DIR}/final_check.py "
try:
    import torch
    print('SUCCESS: PyTorch', torch.__version__)
    
    import diffusers
    print('SUCCESS: Diffusers', diffusers.__version__)
    
    import transformers
    print('SUCCESS: Transformers', transformers.__version__)
    
    import flask
    print('SUCCESS: Flask')
    
    print('SUCCESS: All packages installed!')
    exit(0)
except Exception as e:
    print('ERROR:', str(e))
    exit(1)
")

    # Финальная проверка через файл
    execute_process(
        COMMAND ${PYTHON_PATH} ${CMAKE_BINARY_DIR}/final_check.py
        RESULT_VARIABLE final_check
        OUTPUT_VARIABLE final_output
    )
    
    message(STATUS "${final_output}")
    
    if(NOT final_check EQUAL 0)
        message(FATAL_ERROR "Final package check failed")
    endif()
    
    message(STATUS "Virtual environment setup completed at ${venv_dir}")
endfunction()

function(setup_huggingface_token)
    if(WITH_HF_TOKEN AND HF_TOKEN)
        message(STATUS "Using Hugging Face token from CMake configuration")
        file(WRITE ${VENV_DIR}/hf_token.txt ${HF_TOKEN})
    elseif(DEFINED ENV{HUGGINGFACE_HUB_TOKEN})
        message(STATUS "Using Hugging Face token from environment")
        file(WRITE ${VENV_DIR}/hf_token.txt $ENV{HUGGINGFACE_HUB_TOKEN})
    else()
        message(WARNING "No Hugging Face token provided")
        message(STATUS "Some models may require authentication")
    endif()
endfunction()

set(VENV_DIR ${CMAKE_BINARY_DIR}/venv)
create_venv(${VENV_DIR})
setup_huggingface_token()

if(WIN32)
    set(PYTHON_PATH ${VENV_DIR}/Scripts/python.exe)
    set(PYINSTALLER_CMD ${VENV_DIR}/Scripts/pyinstaller.exe)
    set(EXE_EXT ".exe")
else()
    set(PYTHON_PATH ${VENV_DIR}/bin/python)
    set(PYINSTALLER_CMD ${VENV_DIR}/bin/pyinstaller)
    set(EXE_EXT "")
endif()

# Создаем файл для проверки пакетов
file(WRITE ${CMAKE_BINARY_DIR}/check_packages.py "
import sys
print('Python version:', sys.version)

try:
    import torch
    print('PyTorch:', torch.__version__)
    print('CUDA available:', torch.cuda.is_available())
    
    import diffusers
    print('Diffusers:', diffusers.__version__)
    
    import transformers
    print('Transformers:', transformers.__version__)
    
    import flask
    print('Flask: OK')
    
    print('SUCCESS: All packages are properly installed!')
    sys.exit(0)
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
")

add_custom_target(check_packages
    COMMAND ${PYTHON_PATH} ${CMAKE_BINARY_DIR}/check_packages.py
    COMMENT "Checking package installation"
)

add_custom_target(create_dist_dirs
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/dist
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/src_dist
    COMMENT "Creating output directories"
)

# Простой тест через файл
file(WRITE ${CMAKE_BINARY_DIR}/test_basic.py "
import sys
print('Basic functionality test...')

try:
    import torch
    print('PyTorch OK')
    
    from diffusers import AutoPipelineForText2Image
    print('Diffusers OK')
    
    import flask
    print('Flask OK')
    
    print('All basic functionality: SUCCESS')
    sys.exit(0)
    
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
")

add_custom_target(test_basic
    COMMAND ${PYTHON_PATH} ${CMAKE_BINARY_DIR}/test_basic.py
    COMMENT "Basic functionality test"
)

add_subdirectory(src)

# Сборка основного приложения
add_custom_target(build_main_exe
    COMMAND ${PYINSTALLER_CMD} 
            --onedir
            --console
            --name ai_image_generator
            --add-data "templates;templates"
            --add-data "static;static"
            --hidden-import=generate_arbitr
            --hidden-import=flask
            --hidden-import=torch
            --hidden-import=diffusers
            --hidden-import=transformers
            --hidden-import=PIL
            --hidden-import=accelerate
            --distpath ${CMAKE_BINARY_DIR}/dist
            ${CMAKE_SOURCE_DIR}/main.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    DEPENDS create_dist_dirs
    COMMENT "Building main Flask application"
)

# Цели сборки
add_custom_target(build_all
    COMMAND ${CMAKE_COMMAND} --build . --target build_main_exe  
    COMMAND ${CMAKE_COMMAND} --build . --target build_src_exe
    COMMENT "Building all executables"
)

add_custom_target(build_with_checks
    COMMAND ${CMAKE_COMMAND} --build . --target check_packages
    COMMAND ${CMAKE_COMMAND} --build . --target test_basic
    COMMAND ${CMAKE_COMMAND} --build . --target build_all
    COMMENT "Building with package checks"
)

add_custom_target(build_quick
    COMMAND ${CMAKE_COMMAND} --build . --target build_all
    COMMENT "Quick build without checks"
)

add_custom_target(build_info
    COMMAND ${CMAKE_COMMAND} -E echo "=== Build Information ==="
    COMMAND ${CMAKE_COMMAND} -E echo "Platform: ${CMAKE_SYSTEM_NAME}"
    COMMAND ${CMAKE_COMMAND} -E echo "Python: ${Python3_EXECUTABLE}"
    COMMAND ${CMAKE_COMMAND} -E echo "VENV: ${VENV_DIR}"
    COMMAND ${CMAKE_COMMAND} -E echo "Output: ${CMAKE_BINARY_DIR}/dist/"
    COMMAND ${CMAKE_COMMAND} -E echo "HF Token: ${WITH_HF_TOKEN}"
    COMMENT "Displaying build information"
)

message(STATUS "")
message(STATUS "Build targets:")
message(STATUS "   build_quick       - Quick build without checks")
message(STATUS "   build_with_checks - Build with package checks") 
message(STATUS "   build_all         - Build all executables")
message(STATUS "   check_packages    - Check package installation")
message(STATUS "   build_info        - Show build information")
message(STATUS "")
message(STATUS "Configure with HF token:")
message(STATUS "   cmake -B build -DWITH_HF_TOKEN=ON -DHF_TOKEN=your_token")
message(STATUS "")