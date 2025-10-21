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

    if(WIN32)
        set(PIP_PATH "${venv_dir}/Scripts/pip.exe")
    else()
        set(PIP_PATH "${venv_dir}/bin/pip")
    endif()

    execute_process(
        COMMAND ${PIP_PATH} install -r ${requirements_path}
        RESULT_VARIABLE pip_install_ret_code
    )

    if(pip_install_ret_code)
        message(FATAL_ERROR "Failed to install dependencies from ${requirements_path}!")
    endif()
    
    message(STATUS "Virtual environment setup done at ${venv_dir}")
endfunction()

set(SRC_VENV ${CMAKE_BINARY_DIR}/venv)
create_venv(${SRC_VENV} ${CMAKE_SOURCE_DIR}/src/requirements.txt)

set(VENV_DIR ${SRC_VENV} CACHE INTERNAL "VENV directory")

add_subdirectory(src)

add_test(NAME python-tests
    COMMAND ${VENV_PYTHON} -m pytest ${CMAKE_SOURCE_DIR}/tests
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)