cmake_minimum_required(VERSION 3.30)
project(day11 C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED True)

add_executable(day11 day_11.c)

find_package(PkgConfig REQUIRED)
pkg_check_modules(glib2 REQUIRED IMPORTED_TARGET glib-2.0)

target_link_libraries(${PROJECT_NAME} PRIVATE PkgConfig::glib2 m)