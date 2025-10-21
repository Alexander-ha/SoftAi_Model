cmake_minimum_required(VERSION 3.28)
project(SoftAi_Model)

# Поиск Python
find_package(Python3 REQUIRED COMPONENTS Interpreter)

# Поиск CUDA
find_package(CUDAToolkit)
if(CUDAToolkit_FOUND)
    message(STATUS "CUDA found: ${CUDAToolkit_VERSION}")
else()
    message(WARNING "CUDA not found! PyTorch will use CPU only.")
endif()

# Функция для создания venv
function(create_venv venv_dir requirements_path)
    if(EXISTS ${venv_dir})
        message(STATUS "Virtual environment already exists in ${venv_dir}, skipping creation.")
        return()
    endif()
    
    if(NOT EXISTS ${requirements_path})
        message(FATAL_ERROR "Requirements file not found: ${requirements_path}")
    endif()

    execute_process(
        COMMAND ${Python3_EXECUTABLE} -m venv ${venv_dir}
        RESULT_VARIABLE venv_creation_ret_code
    )
    
    if(venv_creation_ret_code)
        message(FATAL_ERROR "Failed to create virtual environment at ${venv_dir}!")
    endif()

    if(WIN32)
        set(PIP_PATH "${venv_dir}/Scripts/pip.exe")
    else()
        set(PIP_PATH "${venv_dir}/bin/pip")
    endif()

    # Устанавливаем зависимости
    execute_process(
        COMMAND ${PIP_PATH} install -r ${requirements_path} pyinstaller
        RESULT_VARIABLE pip_install_ret_code
    )

    if(pip_install_ret_code)
        message(FATAL_ERROR "Failed to install dependencies from ${requirements_path}!")
    endif()
    
    message(STATUS "Virtual environment setup done at ${venv_dir}")
endfunction()

# Создаем venv
set(VENV_DIR ${CMAKE_BINARY_DIR}/venv)
create_venv(${VENV_DIR} ${CMAKE_SOURCE_DIR}/src/requirements.txt)

# Передаем переменные в дочерний CMakeLists
set(VENV_DIR ${VENV_DIR} CACHE INTERNAL "VENV directory")

# Добавляем поддиректорию src
add_subdirectory(src)

# Создаем цели для main.py в корне
if(WIN32)
    set(PYTHON_PATH ${VENV_DIR}/Scripts/python.exe)
    set(VENV_PYTHON ${VENV_DIR}/Scripts/python.exe)
    set(PYINSTALLER_CMD ${VENV_DIR}/Scripts/pyinstaller.exe)
else()
    set(PYTHON_PATH ${VENV_DIR}/bin/python)
    set(VENV_PYTHON ${VENV_DIR}/bin/python)
    set(PYINSTALLER_CMD ${VENV_DIR}/bin/pyinstaller)
endif()

# EXE цель для main.py (исправленная)
add_custom_target(build_main_exe
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/dist
    COMMAND ${PYINSTALLER_CMD} 
            --onedir
            --console
            --name ai_image_generator
            --distpath ${CMAKE_BINARY_DIR}/dist
            ${CMAKE_SOURCE_DIR}/main.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Building main.py as executable"
)

# Тест CUDA
add_custom_target(test_cuda
    COMMAND ${PYTHON_PATH} -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU device: {torch.cuda.get_device_name(0)}')
else:
    print('CUDA not available - using CPU')
"
    COMMENT "Testing CUDA availability"
)

add_custom_target(run_tests
    COMMAND ${VENV_PYTHON} -m pytest ${CMAKE_SOURCE_DIR}/tests -v
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running Python tests"
)

add_custom_target(build_all
    DEPENDS build_main_exe build_src_exe
    COMMENT "Building all executables"
)

add_custom_target(test_all
    DEPENDS test_cuda run_tests
    COMMENT "Running all tests"
)