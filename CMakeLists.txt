cmake_minimum_required(VERSION 2.8.11)
project(chemfiles.py)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
cmake_policy(VERSION 2.8.11)

option(CHFL_PY_CODE_COVERAGE "Enable python code coverage" OFF)
option(CHFL_PY_BUILD_DOCUMENTATION "Build the python documentation" OFF)
option(CHFL_PY_INTERNAL_CHEMFILES "Use the internal version of chemfiles" OFF)

if(NOT ${CHFL_PY_INTERNAL_CHEMFILES})
    find_package(chemfiles CONFIG QUIET 0.7)
endif()

if(${chemfiles_FOUND})
    set(CHEMFILES_VERSION "${chemfiles_VERSION}")
    get_target_property(CHEMFILES_TYPE chemfiles TYPE)
    if ("${CHEMFILES_TYPE}" STREQUAL "SHARED_LIBRARY")
        message(STATUS "Using external chemfiles (version ${CHEMFILES_VERSION})")
    elseif ("${CHEMFILES_TYPE}" STREQUAL "STATIC_LIBRARY")
        message(FATAL_ERROR
            "Can not use the static version of external chemfiles\n"
            "Define CHFL_PY_INTERNAL_CHEMFILES=ON to use use the internal chemfiles."
        )
    endif()
else()
    # Use the git submodule
    message(STATUS "Using internal chemfiles from ${CMAKE_CURRENT_SOURCE_DIR}/chemfiles")
    set(BUILD_SHARED_LIBS ON CACHE BOOL "Build shared libraries instead of static ones" FORCE)
    add_subdirectory(chemfiles)
    file(READ chemfiles/VERSION CHEMFILES_VERSION)
    string(STRIP ${CHEMFILES_VERSION} CHEMFILES_VERSION)
endif()

configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in"
  "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
)

find_package(PythonInterp REQUIRED)
set(SETUP_PY "${CMAKE_CURRENT_BINARY_DIR}/setup.py")

file(GLOB_RECURSE PYTHON_SRC src/chemfiles/**.py)
set(SETUP_PY_BUILD_OUTPUT "")
set(COPY_SRC_OUTPUT "")
foreach(_file_ ${PYTHON_SRC})
    file(RELATIVE_PATH _path_ ${CMAKE_CURRENT_SOURCE_DIR} ${_file_})
    list(APPEND COPY_SRC_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_path_})

    file(RELATIVE_PATH _path_ ${CMAKE_CURRENT_SOURCE_DIR}/src/chemfiles ${_file_})
    list(APPEND SETUP_PY_BUILD_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/build/lib/${_path_})
endforeach()

add_custom_command(
    OUTPUT ${COPY_SRC_OUTPUT}
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_BINARY_DIR}/src/
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/src/ ${CMAKE_CURRENT_BINARY_DIR}/src/
    DEPENDS ${PYTHON_SRC}
    COMMENT "Copying python sources"
)

# We configure the same file twice: the one in `build/lib` will be the one
# installed, and the one in `src/chemfiles` will be used for testing.
add_custom_command(
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/src/chemfiles/location.py"
    COMMAND ${CMAKE_COMMAND}
            -DLOCATION_PY_PATH=${CMAKE_CURRENT_BINARY_DIR}/src/
            -DCHEMFILES_LOCATION=$<TARGET_FILE:chemfiles>
            -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/generate_location.cmake
    COMMENT "Generating test location.py"
)

add_custom_command(
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/build/lib/chemfiles/location.py"
    COMMAND ${CMAKE_COMMAND}
            -DLOCATION_PY_PATH=${CMAKE_CURRENT_BINARY_DIR}/build/lib
            -DCHEMFILES_LOCATION=${CMAKE_INSTALL_PREFIX}/lib${LIB_SUFFIX}/$<TARGET_FILE_NAME:chemfiles>
            -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/generate_location.cmake
    COMMENT "Generating install location.py"
)

add_custom_target(location.py ALL
    DEPENDS ${COPY_SRC_OUTPUT}
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/src/chemfiles/location.py
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/build/lib/chemfiles/location.py
)

add_custom_command(
    OUTPUT ${SETUP_PY_BUILD_OUTPUT}
    COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} build
    DEPENDS location.py
    COMMENT "Running python setup.py build"
)

set(ADDITIONAL_CLEANUP "${CMAKE_CURRENT_BINARY_DIR}/build/")
if(NOT "${CMAKE_CURRENT_BINARY_DIR}" STREQUAL "${CMAKE_CURRENT_SOURCE_DIR}")
    set(ADDITIONAL_CLEANUP "${ADDITIONAL_CLEANUP};${CMAKE_CURRENT_BINARY_DIR}/src/")
endif()
set_property(DIRECTORY PROPERTY ADDITIONAL_MAKE_CLEAN_FILES ${ADDITIONAL_CLEANUP})

add_custom_target(chemfiles.py ALL DEPENDS ${SETUP_PY_BUILD_OUTPUT})
add_dependencies(chemfiles.py chemfiles)

install(CODE "execute_process(COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install --prefix=${CMAKE_INSTALL_PREFIX})")

enable_testing()
add_subdirectory(tests)

if(${CHFL_PY_BUILD_DOCUMENTATION})
    add_subdirectory(doc)
endif()
