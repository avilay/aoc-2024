cmake_minimum_required(VERSION 3.30)
project(day_12 C)

set(CMAKE_C_STANDARD 17)

add_executable(${PROJECT_NAME} main.c)

file(COPY ${CMAKE_SOURCE_DIR}/inputs DESTINATION ${CMAKE_BINARY_DIR})

find_package(PkgConfig REQUIRED)
pkg_check_modules(glib2 REQUIRED IMPORTED_TARGET glib-2.0)

target_link_libraries(${PROJECT_NAME} PRIVATE PkgConfig::glib2 m)

