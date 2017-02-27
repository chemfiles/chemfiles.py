cmake_minimum_required(VERSION 2.8.11)
project(chemfiles.py)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
cmake_policy(VERSION 2.8.11)
if (${CMAKE_VERSION} VERSION_GREATER 2.8.12)
    cmake_policy(SET CMP0026 OLD)
endif()

option(CHFL_PY_CODE_COVERAGE "Enable python code coverage" OFF)
option(CHFL_PY_BUILD_DOCUMENTATION "Build the python documentation" OFF)
option(CHFL_PY_INTERNAL_CHEMFILES "Use the internal version of chemfiles" OFF)

if(NOT ${CHFL_PY_INTERNAL_CHEMFILES})
    find_package(chemfiles CONFIG QUIET 0.7)
endif()

if(${chemfiles_FOUND})
    set(CHEMFILES_VERSION "${chemfiles_VERSION}")
    get_target_property(CHEMFILES_LOCATION chemfiles LOCATION)
    get_target_property(CHEMFILES_TYPE chemfiles TYPE)
    if ("${CHEMFILES_TYPE}" STREQUAL "SHARED_LIBRARY")
        message(STATUS "Using chemfiles (version ${CHEMFILES_VERSION}) at ${CHEMFILES_LOCATION}")
    elseif ("${CHEMFILES_TYPE}" STREQUAL "STATIC_LIBRARY")
        message(FATAL_ERROR
            "Can not use the static version of chemfiles at ${CHEMFILES_LOCATION}\n"
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
    get_target_property(CHEMFILES_LOCATION chemfiles LOCATION)
endif()

configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in"
  "${CMAKE_CURRENT_BINARY_DIR}/setup.py"
)

# We configure the same file twice: the one in `build/lib` will be the one
# installed, and the one in `src/chemfiles` will be used for testing.
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/src/chemfiles/clib.py.in"
  "${CMAKE_CURRENT_BINARY_DIR}/src/chemfiles/clib.py"
)

set(CHEMFILES_LOCATION "chemfiles")
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/src/chemfiles/clib.py.in"
  "${CMAKE_CURRENT_BINARY_DIR}/build/lib/chemfiles/clib.py"
)

find_package(PythonInterp REQUIRED)
set(SETUP_PY "${CMAKE_CURRENT_BINARY_DIR}/setup.py")

file(GLOB_RECURSE PYTHON_SRC src/chemfiles/**.py)
set(SETUP_PY_BUILD_OUTPUT "")
foreach(_file_ ${PYTHON_SRC})
    file(RELATIVE_PATH _path_ ${CMAKE_CURRENT_SOURCE_DIR} ${_file_})
    list(APPEND SETUP_PY_BUILD_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${_path_})

    file(RELATIVE_PATH _path_ ${CMAKE_CURRENT_SOURCE_DIR}/src/chemfiles ${_file_})
    list(APPEND SETUP_PY_BUILD_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/build/lib/${_path_})
endforeach()
list(APPEND SETUP_PY_BUILD_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/src/chemfiles/clib.py)
list(APPEND SETUP_PY_BUILD_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/build/lib/clib.py)

add_custom_command(
    OUTPUT ${SETUP_PY_BUILD_OUTPUT}
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/src/ ${CMAKE_CURRENT_BINARY_DIR}/src/
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_CURRENT_BINARY_DIR}/src/chemfiles/clib.py.in
    COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} build
    COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_CURRENT_BINARY_DIR}/build/lib/chemfiles/clib.py
    DEPENDS ${PYTHON_SRC}
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
