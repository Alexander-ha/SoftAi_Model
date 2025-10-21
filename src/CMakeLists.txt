cmake_minimum_required(VERSION 3.28)

set(SRC_VENV ${VENV_DIR})

if(WIN32)
    set(VENV_PYTHON ${SRC_VENV}/Scripts/python.exe)
else()
    set(VENV_PYTHON ${SRC_VENV}/bin/python)
endif()

set(VENV_PYTHON ${VENV_PYTHON} PARENT_SCOPE)

add_custom_target(run_generate_cake
    COMMAND ${VENV_PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/generate_cake.py
    DEPENDS ${SRC_VENV}
    COMMENT "Running generate_cake.py"
)

add_custom_target(run_generate_cat
    COMMAND ${VENV_PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/generate_cat.py
    DEPENDS ${SRC_VENV}
    COMMENT "Running generate_cat.py"
)

add_custom_target(run_generate_dog
    COMMAND ${VENV_PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/generate_dog.py
    DEPENDS ${SRC_VENV}
    COMMENT "Running generate_dog.py"
)