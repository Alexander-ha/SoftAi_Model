# specify minimu CMake version
cmake_minimum_required(VERSION 3.28)
project(SoftAi_Model)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
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
    execute_process(
        COMMAND ${venv_dir}/bin/pip install -r ${requirements_path}
        RESULT_VARIABLE pip_install_ret_code
    )

    if(pip_install_ret_code)
        message(FATAL_ERROR "Failed to install dependencies from ${requirements_path}!")
    endif()
    message(STATUS "Virtual environment setup done at ${venv_dir} with dependencies from ${requirements_path}")
endfunction()
add_subdirectory(src)
add_test (NAME python-tests
  COMMAND ${PYTHON_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/
)

