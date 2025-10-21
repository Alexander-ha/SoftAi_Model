
set(SRC_VENV ${CMAKE_BINARY_DIR}/src) #Setting source directory and venv 

create_venv(${SRC_VENV} ${CMAKE_SOURCE_DIR}/src/requirements.txt) #Creating venv according to our imports

add_custom_target(run_generate_cake
    COMMAND ${SRC_VENV}/bin/python ${CMAKE_SOURCE_DIR}/src/generate_cake.py
    DEPENDS ${SRC_VENV}
) ## Add target to exec img to img 

add_custom_target(run_generate_cat
    COMMAND ${SRC_VENV}/bin/python ${CMAKE_SOURCE_DIR}/src/generate_cat.py
    DEPENDS ${SRC_VENV}
) ## Add target to exec txt to img 

add_custom_target(run_generate_dog
    COMMAND ${SRC_VENV}/bin/python ${CMAKE_SOURCE_DIR}/src/generate_dog.py
    DEPENDS ${SRC_VENV}
)  ## Add target to exec inpainting
