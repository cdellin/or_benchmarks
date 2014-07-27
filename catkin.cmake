cmake_minimum_required(VERSION 2.8.3)

find_package(catkin REQUIRED)
catkin_package()

find_package(OpenRAVE REQUIRED)

include(FindPkgConfig)
pkg_check_modules(YamlCpp REQUIRED yaml-cpp)

include_directories(
    "include/"
    ${OpenRAVE_INCLUDE_DIRS}
    ${YamlCpp_INCLUDE_DIRS}
)
link_directories(
    ${OpenRAVE_LIBRARY_DIRS}
    ${YamlCpp_LIBRARY_DIRS}
)

# OpenRAVE plugin.
add_library("${PROJECT_NAME}_plugin" SHARED
    src/CollisionCheckingBenchmark.cpp
    src/CollisionCheckingModule.cpp
)
target_link_libraries("${PROJECT_NAME}_plugin"
    ${OpenRAVE_LIBRARIES}
    ${YamlCpp_LIBRARIES}
)
set_target_properties("${PROJECT_NAME}_plugin" PROPERTIES
    PREFIX ""
    COMPILE_FLAGS "${OpenRAVE_CXX_FLAGS}"
    LINK_FLAGS "${OpenRAVE_LINK_FLAGS}"
    LIBRARY_OUTPUT_DIRECTORY "${CATKIN_DEVEL_PREFIX}/${CATKIN_GLOBAL_LIB_DESTINATION}/openrave-${OpenRAVE_LIBRARY_SUFFIX}"
)

install(TARGETS "${PROJECT_NAME}_plugin"
    LIBRARY DESTINATION "${CATKIN_PACKAGE_LIB_DESTINATION}/openrave-${OpenRAVE_LIBRARY_SUFFIX}"
)
install(PROGRAMS "scripts/run_benchmark.py"
     DESTINATION "${CATKIN_PACKAGE_BIN_DESTINATION}"
)
