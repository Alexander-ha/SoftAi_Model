cmake_minimum_required(VERSION 3.28)
project(SoftAi_Src)

get_directory_property(VENV_DIR PARENT_DIRECTORY VENV_DIR)

if(WIN32)
    set(PYTHON_PATH ${VENV_DIR}/Scripts/python.exe)
    set(NUITKA_CMD ${VENV_DIR}/Scripts/nuitka)
    set(EXE_EXT ".exe")
else()
    set(PYTHON_PATH ${VENV_DIR}/bin/python)
    set(NUITKA_CMD ${VENV_DIR}/bin/nuitka)
    set(EXE_EXT "")
endif()

# Функция для создания exe с Nuitka
function(create_src_exe python_script exe_name)
    add_custom_target(build_${exe_name}
        COMMAND ${NUITKA_CMD} 
                --standalone
                --onefile
                --windows-console-mode=attach
                --output-dir=${CMAKE_BINARY_DIR}/src_dist
                --output-filename=${exe_name}${EXE_EXT}
                --include-package=torch
                --include-package=diffusers
                --include-package=transformers
                --include-package=PIL
                --plugin-enable=pylint-warnings
                --assume-yes-for-downloads
                ${CMAKE_CURRENT_SOURCE_DIR}/${python_script}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Building ${exe_name}${EXE_EXT} with Nuitka"
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