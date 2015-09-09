# This CMakeLists.txt file is not usable on it's own, but should be included in another
# main CMakeLists.txt. It provides tests for the Python binding as CTest targets, and
# install the Python module

find_package(PythonLibsNew REQUIRED)

set(CHRP_PYTHONPATH ${CMAKE_CURRENT_SOURCE_DIR}:${CMAKE_CURRENT_SOURCE_DIR}/examples:${CMAKE_BINARY_DIR})

function(chrp_python_test _file_)
    get_filename_component(_name_ ${_file_} NAME_WE)
    add_test(NAME python-${_name_} COMMAND ${PYTHON_EXECUTABLE} ${_file_})
    set_tests_properties(python-${_name_}
    PROPERTIES ENVIRONMENT "PYTHONPATH=${CHRP_PYTHONPATH}")
endfunction()

function(chrp_python_import_test _file_)
    get_filename_component(_name_ ${_file_} NAME_WE)
    add_test(NAME python-example-${_name_} COMMAND ${PYTHON_EXECUTABLE} -c "import ${_name_}")
    set_tests_properties(python-example-${_name_}
    PROPERTIES ENVIRONMENT "PYTHONPATH=${CHRP_PYTHONPATH}")
endfunction()

if(BUILD_TESTS)
    file(GLOB python_test_files ${CMAKE_CURRENT_SOURCE_DIR}/tests/*.py)
    list(REMOVE_ITEM python_test_files ${CMAKE_CURRENT_SOURCE_DIR}/tests/__init__.py)

    foreach(test_file IN LISTS python_test_files)
        chrp_python_test(${test_file})
    endforeach(test_file)

    file(GLOB python_example_files ${CMAKE_CURRENT_SOURCE_DIR}/examples/*.py)

    foreach(test_file IN LISTS python_example_files)
        chrp_python_import_test(${test_file})
    endforeach(test_file)
endif()
