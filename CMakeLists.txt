cmake_minimum_required(VERSION 3.25)

project(ImGuizmo VERSION 1.0 LANGUAGES C CXX)

set(
    ALL_SRC
    GraphEditor.cpp
    ImCurveEdit.cpp
    ImGradient.cpp
    ImGuizmo.cpp
    ImSequencer.cpp

    GraphEditor.h
    ImCurveEdit.h
    ImGradient.h
    ImGuizmo.h
    ImSequencer.h
   ImZoomSlider.h
)


find_package(glfw3 REQUIRED)
find_package(Vulkan REQUIRED)
find_package(imguidocking REQUIRED)

if(LINUX)
    find_package(VulkanLoader REQUIRED CONFIG)
endif(LINUX)

add_library(${PROJECT_NAME} ${ALL_SRC})

target_include_directories(${PROJECT_NAME} PUBLIC ./)

target_link_libraries(${PROJECT_NAME} glfw Vulkan::Vulkan imguidocking::imguidocking)

if(LINUX)
target_link_libraries(${PROJECT_NAME} glfw Vulkan::Loader)
endif(LINUX)
install(TARGETS ${PROJECT_NAME})
