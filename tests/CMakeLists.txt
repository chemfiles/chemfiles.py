if(${CHFL_PY_CODE_COVERAGE})
    set(TEST_COMMAND "coverage;run;--append")
else()
    set(TEST_COMMAND ${PYTHON_EXECUTABLE})
endif()

set(TEST_RUNNER_PY "${CMAKE_CURRENT_BINARY_DIR}/test-runner.py")
file(WRITE ${TEST_RUNNER_PY}
"import os
import sys
sys.path.insert(1, '${PROJECT_BINARY_DIR}/src')

path = sys.argv[1]

# we need to remove sys.argv; as unittest main try to parse it and fails
del sys.argv[1]

with open(path) as fd:
    name = os.path.basename(path)
    code = compile(fd.read(), name, 'exec')
    exec(code)
")

function(python_test _file_)
    get_filename_component(_name_ ${_file_} NAME_WE)
    add_test(
        NAME ${_name_}
        COMMAND ${TEST_COMMAND} ${TEST_RUNNER_PY} ${_file_}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
endfunction()

file(GLOB all_test_files
    ${CMAKE_CURRENT_SOURCE_DIR}/*.py
)

foreach(test_file IN LISTS all_test_files)
    python_test(${test_file})
endforeach(test_file)
