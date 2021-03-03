cmake_minimum_required(VERSION 3.5)
project(smartreply)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
# Update submodules as needed
    option(GIT_SUBMODULE "Check submodules during build" ON)
    if(GIT_SUBMODULE)
        message(STATUS "Submodule update")
        execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                        RESULT_VARIABLE GIT_SUBMOD_RESULT)
        if(NOT GIT_SUBMOD_RESULT EQUAL "0")
            message(FATAL_ERROR "git submodule update --init failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
        endif()
    endif()
endif()

add_subdirectory(
    "dependencies/tensorflow/tensorflow/lite"
)

add_subdirectory(
    "dependencies/pybind11"
)

add_subdirectory(
    "dependencies/re2"
)

pybind11_add_module(
    smartreply
    MODULE
    "src/py_inference.cc"
    "src/predictor.cc"
    "src/op_extract_feature.cc"
    "src/op_normalize.cc"
    "src/op_predict.cc"
)
target_link_libraries(smartreply PRIVATE tensorflow-lite)
target_link_libraries(smartreply PRIVATE ${CMAKE_DL_LIBS})
target_link_libraries(smartreply PRIVATE re2)

install(TARGETS smartreply DESTINATION .)
