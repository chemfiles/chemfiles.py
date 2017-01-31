if(${CHFL_PY_CODE_COVERAGE})
    set(TEST_COMMAND "coverage;run")
else()
    set(TEST_COMMAND ${PYTHON_EXECUTABLE})
endif()

function(python_test _file_)
    get_filename_component(_name_ ${_file_} NAME_WE)
    add_test(
        NAME ${_name_}
        COMMAND ${TEST_COMMAND} ${_file_}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    set_tests_properties(
        ${_name_} PROPERTIES ENVIRONMENT
        "PYTHONPATH=${PROJECT_BINARY_DIR}/src"
    )
endfunction()

file(GLOB all_test_files
    ${CMAKE_CURRENT_SOURCE_DIR}/*.py
)

foreach(test_file IN LISTS all_test_files)
    python_test(${test_file})
endforeach(test_file)
