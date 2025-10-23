cmake_minimum_required(VERSION 3.28)
project(SoftAi_Src)

get_directory_property(VENV_DIR PARENT_DIRECTORY VENV_DIR)

if(WIN32)
    set(PYTHON_PATH ${VENV_DIR}/Scripts/python.exe)
    set(PYINSTALLER_CMD ${VENV_DIR}/Scripts/pyinstaller.exe)
else()
    set(PYTHON_PATH ${VENV_DIR}/bin/python)
    set(PYINSTALLER_CMD ${VENV_DIR}/bin/pyinstaller)
endif()

# Создаем тестовый файл для generate_arbitr
file(WRITE ${CMAKE_BINARY_DIR}/test_generate_arbitr.py "
import sys
import os
sys.path.append('${CMAKE_CURRENT_SOURCE_DIR}')

try:
    from generate_arbitr import test_imports
    result = test_imports()
    if result:
        print('SUCCESS: generate_arbitr imports work')
        sys.exit(0)
    else:
        print('ERROR: generate_arbitr imports failed')
        sys.exit(1)
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
")

# Простая функция для создания exe
function(create_src_exe python_script exe_name)
    if(WIN32)
        set(EXE_EXT ".exe")
        set(PLATFORM_SPECIFIC --console --onefile)
    else()
        set(EXE_EXT "")
        set(PLATFORM_SPECIFIC --onefile)
    endif()
    
    add_custom_target(build_${exe_name}
        COMMAND ${PYINSTALLER_CMD} 
                ${PLATFORM_SPECIFIC}
                --name ${exe_name}
                --hidden-import=torch
                --hidden-import=diffusers
                --hidden-import=transformers
                --hidden-import=PIL
                --hidden-import=flask
                --distpath ${CMAKE_BINARY_DIR}/src_dist
                ${CMAKE_CURRENT_SOURCE_DIR}/${python_script}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Building ${exe_name}${EXE_EXT}"
    )
endfunction()

create_src_exe(generate_cake.py generate_cake)
create_src_exe(generate_cat.py generate_cat)
create_src_exe(generate_dog.py generate_dog)
create_src_exe(generate_arbitr.py generate_arbitr)

add_custom_target(build_src_exe
    DEPENDS build_generate_cake build_generate_cat build_generate_dog build_generate_arbitr
    COMMENT "Building all src executables"
)

# Простой тест для generate_arbitr через файл
add_custom_target(test_generate_arbitr
    COMMAND ${PYTHON_PATH} ${CMAKE_BINARY_DIR}/test_generate_arbitr.py
    COMMENT "Testing generate_arbitr imports"
)

add_custom_target(test_src_scripts
    DEPENDS test_generate_arbitr
    COMMENT "Testing src scripts"
)