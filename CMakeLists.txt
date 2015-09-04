cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

project(chemharp_python CXX)
set(CMAKE_CXX_STANDARD 11)
set(CXX_STANDARD_REQUIRED ON)

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'release' as none was specified.")
  set(CMAKE_BUILD_TYPE "release" CACHE STRING "Choose the type of build." FORCE)
endif()

if(${CMAKE_CURRENT_SOURCE_DIR} STREQUAL ${CMAKE_SOURCE_DIR})
    # This is the top-level CMakeLists.txt
    set(TOP_LEVEL true)
else()
    set(TOP_LEVEL false)
endif()

if(TOP_LEVEL)
    find_package(Chemharp)
    if(NOT ${CHEMHARP_FOUND})
        message(FATAL_ERROR "Could not find Chemharp. Please set CHEMHARP_INCLUDEDIR \
                            and CHEMHARP_LIBDIR to the location of the library.")
    endif()
    include_directories(${CHEMHARP_INCLUDE_DIRS})
endif()

if(TOP_LEVEL)
    # uninstall target
    configure_file(
        "${CMAKE_SOURCE_DIR}/cmake/uninstall.in.cmake"
        "${CMAKE_BINARY_DIR}/uninstall.cmake"
        IMMEDIATE @ONLY)

    add_custom_target(uninstall
        COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/uninstall.cmake)
endif()

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/external/boost/CMakeLists.txt")
    message(STATUS "Unpacking Boost sources")
    execute_process(
        COMMAND ${CMAKE_COMMAND} -E tar xf ${CMAKE_CURRENT_SOURCE_DIR}/external/boost.tar.gz
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/external
    )
endif()
add_subdirectory(external)
include_directories(BEFORE SYSTEM ${CMAKE_CURRENT_SOURCE_DIR}/external/boost)

find_package(PythonLibsNew REQUIRED)

include_directories(SYSTEM ${PYTHON_INCLUDE_DIRS})

file(GLOB python_sources src/*.cpp)

PYTHON_ADD_MODULE(chemharp_python ${python_sources})
target_link_libraries(chemharp_python boost_numpy boost_python)

if(TOP_LEVEL)
    target_link_libraries(chemharp_python ${CHEMHARP_LIBRARIES})
else()
    target_link_libraries(chemharp_python chemharp)
endif()

add_custom_command(TARGET chemharp_python POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy
                       $<TARGET_FILE:chemharp_python>
                       chemharp.so
                   COMMENT "Copying Python binding to 'chemharp.so'")

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/chemharp.so
        DESTINATION ${PYTHON_SITE_PACKAGES})

function(chrp_python_test _file_)
    get_filename_component(_name_ ${_file_} NAME_WE)
    add_test(NAME python-${_name_} COMMAND ${PYTHON_EXECUTABLE} ${_file_})
    set_tests_properties(python-${_name_}
        PROPERTIES ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}")
endfunction()

function(chrp_python_import_test _file_)
    get_filename_component(_name_ ${_file_} NAME_WE)
    add_test(NAME python-example-${_name_} COMMAND ${PYTHON_EXECUTABLE} -c "import ${_name_}")
    set_tests_properties(python-example-${_name_}
    PROPERTIES ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}:${CMAKE_CURRENT_SOURCE_DIR}/examples")
endfunction()

if(BUILD_TESTS)
    file(GLOB python_test_files ${CMAKE_CURRENT_SOURCE_DIR}/tests/*.py)

    foreach(test_file IN LISTS python_test_files)
        chrp_python_test(${test_file})
    endforeach(test_file)

    file(GLOB python_example_files ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.py)

    foreach(test_file IN LISTS python_example_files)
        chrp_python_import_test(${test_file})
    endforeach(test_file)
endif()
