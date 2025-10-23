cmake_minimum_required(VERSION 3.28)
project(AISoft_Model VERSION 1.0.0 LANGUAGES)

option(WITH_HF_TOKEN "Enable Hugging Face token support" OFF)
set(HF_TOKEN "" CACHE STRING "Hugging Face API token")

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

# Функция создания виртуального окружения и установки пакетов
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

    # Устанавливаем зависимости из requirements.txt
    if(EXISTS ${CMAKE_SOURCE_DIR}/requirements.txt)
        message(STATUS "Installing dependencies from requirements.txt...")
        execute_process(
            COMMAND ${PIP_PATH} install -r ${CMAKE_SOURCE_DIR}/requirements.txt
            RESULT_VARIABLE requirements_install_ret_code
            TIMEOUT 300
        )
        
        if(NOT requirements_install_ret_code EQUAL 0)
            message(WARNING "Failed to install from requirements.txt, trying compatible versions...")
        endif()
    endif()

    # Устанавливаем совместимые версии поэтапно
    message(STATUS "Installing compatible packages...")
    
    message(STATUS "Step 1: Installing compatible NumPy...")
    execute_process(
        COMMAND ${PIP_PATH} install "numpy<2"
        RESULT_VARIABLE numpy_install_ret_code
        TIMEOUT 120
    )
    
    if(NOT numpy_install_ret_code EQUAL 0)
        message(WARNING "Failed to install NumPy")
    endif()

    message(STATUS "Step 2: Installing PyTorch...")
    if(CMAKE_CXX_COMPILER AND CUDAToolkit_FOUND)
        execute_process(
            COMMAND ${PIP_PATH} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
            RESULT_VARIABLE torch_install_ret_code
            TIMEOUT 300
        )
    else()
        execute_process(
            COMMAND ${PIP_PATH} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
            RESULT_VARIABLE torch_install_ret_code
            TIMEOUT 300
        )
    endif()
    
    if(NOT torch_install_ret_code EQUAL 0)
        message(WARNING "Failed to install PyTorch")
    endif()

    message(STATUS "Step 3: Installing compatible Hugging Face ecosystem...")
    execute_process(
        COMMAND ${PIP_PATH} install 
            "huggingface-hub==0.19.4"
            "diffusers==0.21.4" 
            "transformers==4.35.2" 
            "accelerate==0.24.1"
            "safetensors>=0.3.1"
        RESULT_VARIABLE hf_install_ret_code
        TIMEOUT 300
    )
        
    if(NOT hf_install_ret_code EQUAL 0)
        message(WARNING "Failed to install Hugging Face packages")
    endif()

    message(STATUS "Step 4: Installing web dependencies...")
    execute_process(
        COMMAND ${PIP_PATH} install flask werkzeug pillow
        RESULT_VARIABLE web_install_ret_code
        TIMEOUT 180
    )
    
    if(NOT web_install_ret_code EQUAL 0)
        message(WARNING "Failed to install web dependencies")
    endif()

    # ДОБАВЛЕНО: Установка тестовых зависимостей
    message(STATUS "Step 5: Installing test dependencies...")
    execute_process(
        COMMAND ${PIP_PATH} install pytest
        RESULT_VARIABLE pytest_install_ret_code
        TIMEOUT 120
    )
    
    if(NOT pytest_install_ret_code EQUAL 0)
        message(WARNING "Failed to install pytest")
    endif()

    # Финальная проверка
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
    
    import pytest
    print('SUCCESS: pytest')
    
    print('SUCCESS: All packages installed!')
    exit(0)
except Exception as e:
    print('ERROR:', str(e))
    exit(1)
")

    execute_process(
        COMMAND ${PYTHON_PATH} ${CMAKE_BINARY_DIR}/final_check.py
        RESULT_VARIABLE final_check
        OUTPUT_VARIABLE final_output
    )
    
    message(STATUS "${final_output}")
    
    if(NOT final_check EQUAL 0)
        message(WARNING "Some packages might not be installed correctly")
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
        message(STATUS "No Hugging Face token provided - some models may require authentication")
    endif()
endfunction()

# Создаем необходимые файлы и директории
function(setup_project_structure)
    # Создаем базовую структуру static
    execute_process(
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_SOURCE_DIR}/static/uploads
    )
    execute_process(
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_SOURCE_DIR}/static/generated
    )
    
    # Создаем placeholder файлы для static
    file(WRITE ${CMAKE_SOURCE_DIR}/static/.gitkeep "")
    file(WRITE ${CMAKE_SOURCE_DIR}/static/uploads/.gitkeep "")
    file(WRITE ${CMAKE_SOURCE_DIR}/static/generated/.gitkeep "")
    
    # Создаем __init__.py в src чтобы сделать его пакетом
    file(WRITE ${CMAKE_SOURCE_DIR}/src/__init__.py "# AI Model Package")
endfunction()

setup_project_structure()

set(VENV_DIR ${CMAKE_BINARY_DIR}/.venv)
create_venv(${VENV_DIR})
setup_huggingface_token()

if(WIN32)
    set(PYTHON_PATH ${VENV_DIR}/Scripts/python.exe)
else()
    set(PYTHON_PATH ${VENV_DIR}/bin/python)
endif()

# Цели для запуска приложения
add_custom_target(run_web
    COMMAND ${PYTHON_PATH} ${CMAKE_SOURCE_DIR}/main.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running web interface"
)

add_custom_target(run_web_dev
    COMMAND ${PYTHON_PATH} ${CMAKE_SOURCE_DIR}/main.py --port 8001
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running web interface on port 8001"
)

# Цели для тестирования
add_custom_target(run_tests
    COMMAND ${PYTHON_PATH} -m pytest ${CMAKE_SOURCE_DIR}/tests -v
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running all tests with pytest"
)


add_custom_target(venv_shell
    COMMENT "Virtual environment is ready at ${VENV_DIR}. Activate with:"
)

if(WIN32)
    add_custom_target(venv_activate
        COMMAND cmd.exe /c "echo Activate virtual environment: && echo ${VENV_DIR}\\Scripts\\activate"
        COMMENT "Windows activation command printed above"
    )
else()
    add_custom_target(venv_activate
        COMMAND bash -c "echo 'Activate virtual environment:' && echo 'source ${VENV_DIR}/bin/activate'"
        COMMENT "Linux activation command printed above"
    )
endif()

message(STATUS "")
message(STATUS "=== AI Image Generator Setup Complete ===")
message(STATUS "Virtual environment: ${VENV_DIR}")
message(STATUS "")
message(STATUS "Available targets:")
message(STATUS "   run_web        - Run the web interface")
message(STATUS "   run_web_dev    - Run web interface on port 8001")
message(STATUS "   run_tests      - Run all tests with pytest")
message(STATUS "   test_pipeline  - Run pipeline tests only")
message(STATUS "   venv_activate  - Show virtual environment activation command")
message(STATUS "")
message(STATUS "To set Hugging Face token:")
message(STATUS "   cmake -B build -DWITH_HF_TOKEN=ON -DHF_TOKEN=your_token_here")
message(STATUS "   OR set HUGGINGFACE_HUB_TOKEN environment variable")
message(STATUS "")
message(STATUS "To run manually from venv:")
if(WIN32)
    message(STATUS "   ${VENV_DIR}\\Scripts\\activate")
    message(STATUS "   python main.py")
else()
    message(STATUS "   source ${VENV_DIR}/bin/activate")
    message(STATUS "   python main.py")
endif()
message(STATUS "")