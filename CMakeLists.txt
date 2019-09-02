cmake_minimum_required(VERSION 2.8.12)

# Prevent CMake from looking for a C and a C++ compilers, as we might not
# need them. They will be search for if using the internal chemfiles
project(chemfiles-python NONE)

option(CHFL_PY_INTERNAL_CHEMFILES "Use the internal version of chemfiles" OFF)

if(NOT ${CHFL_PY_INTERNAL_CHEMFILES})
    find_package(chemfiles CONFIG QUIET 0.9)
endif()

file(REMOVE ${CMAKE_BINARY_DIR}/external.py)
file(REMOVE ${CMAKE_BINARY_DIR}/external.pyc)

if(${chemfiles_FOUND})
    set(CHEMFILES_VERSION "${chemfiles_VERSION}")
    get_target_property(CHEMFILES_TYPE chemfiles TYPE)
    get_target_property(CHEMFILES_LOCATION chemfiles LOCATION)
    if ("${CHEMFILES_TYPE}" STREQUAL "SHARED_LIBRARY")
        message(STATUS "Using external chemfiles ${CHEMFILES_VERSION} at ${CHEMFILES_LOCATION}")
    elseif ("${CHEMFILES_TYPE}" STREQUAL "STATIC_LIBRARY")
        message(FATAL_ERROR
            "Can not use the static version of external chemfiles at at ${CHEMFILES_LOCATION}\n"
            "Define CHFL_PY_INTERNAL_CHEMFILES=ON to use use the internal chemfiles."
        )
    endif()
    file(WRITE ${CMAKE_BINARY_DIR}/external.py
        "EXTERNAL_CHEMFILES = \"${CHEMFILES_LOCATION}\"\n"
    )
    install(FILES ${CMAKE_BINARY_DIR}/external.py DESTINATION ".")
else()
    # Use the git submodule
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/lib/CMakeLists.txt")
        message(FATAL_ERROR
            "The git submodule for chemfiles is not initalized.\n"
            "Please run `git submodule update --init`"
        )
    endif()

    message(STATUS "Using internal chemfiles from ${CMAKE_CURRENT_SOURCE_DIR}/lib")
    set(BUILD_SHARED_LIBS ON CACHE BOOL "Build shared libraries instead of static ones" FORCE)
    add_subdirectory(lib)
    file(READ lib/VERSION CHEMFILES_VERSION)
    string(STRIP ${CHEMFILES_VERSION} CHEMFILES_VERSION)
endif()
