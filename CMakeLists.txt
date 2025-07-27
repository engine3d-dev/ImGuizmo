cmake_minimum_required(VERSION 3.27)

project(imguizmo LANGUAGES CXX)

set(
    all_src
    GraphEditor.cpp
    ImCurveEdit.cpp
    ImGradient.cpp
    ImGuizmo.cpp
    ImSequencer.cpp
)

add_library(${PROJECT_NAME} ${all_src})

target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_LIST_DIR})

find_package(imguidocking REQUIRED)
target_link_libraries(${PROJECT_NAME} PUBLIC imguidocking::imguidocking)

install(TARGETS ${PROJECT_NAME})