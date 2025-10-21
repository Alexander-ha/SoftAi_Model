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

# Создаем директорию для выходных файлов
add_custom_target(create_src_dirs
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/src_dist
    COMMENT "Creating src output directories"
)

# Функция для создания EXE (исправленная)
function(create_src_exe python_script exe_name)
    add_custom_target(build_${exe_name}
        COMMAND ${PYINSTALLER_CMD} 
                --onedir
                --console
                --name ${exe_name}
                --distpath ${CMAKE_BINARY_DIR}/src_dist
                ${CMAKE_CURRENT_SOURCE_DIR}/${python_script}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        DEPENDS create_src_dirs
        COMMENT "Building ${exe_name} from ${python_script}"
    )
endfunction()

# Создаем EXE для скриптов в src
create_src_exe(generate_cake.py generate_cake)
create_src_exe(generate_cat.py generate_cat)
create_src_exe(generate_dog.py generate_dog)
create_src_exe(generate_arbitr.py generate_arbitr)

# Мета-цель для всех src exe
add_custom_target(build_src_exe
    DEPENDS build_generate_cake build_generate_cat build_generate_dog build_generate_arbitr
    COMMENT "Building all src executables"
)

# Простой тест что скрипты работают
add_custom_target(test_src_scripts
    COMMAND ${PYTHON_PATH} -c "
import sys
sys.path.append('${CMAKE_CURRENT_SOURCE_DIR}')
try:
    print('Testing imports...')
    from generate_arbitr import generator_func
    print('✅ generate_arbitr imports OK')
    print('✅ All src scripts are ready')
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"
    COMMENT "Testing src script imports"
)