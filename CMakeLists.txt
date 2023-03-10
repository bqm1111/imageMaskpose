cmake_minimum_required(VERSION 3.15 FATAL_ERROR)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CUDA_COMPILER /usr/local/cuda-11.5/bin/nvcc)

project(test LANGUAGES CXX CUDA)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -pthread")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -fno-omit-frame-pointer -g -pthread -fsanitize=leak")

set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
find_package(spdlog REQUIRED)

file(GLOB SOURCES ${PROJECT_SOURCE_DIR}/*.cpp
                    )
                    
add_executable(${PROJECT_NAME} ${SOURCES})
pkg_check_modules(Uuid REQUIRED IMPORTED_TARGET uuid)
include_directories(${Uuid_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${Uuid_LIBRARIES})

# cuda
find_package(CUDA REQUIRED)
set(CMAKE_CUDA_ARCHITECTURES 52 60 61 75 CACHE STRING "CUDA architectures")
set_target_properties(${PROJECT_NAME} PROPERTIES CUDA_STANDARD 17)
# set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -O3 --compiler-options -fno-strict-aliasing --ptxas-options=-v --generate-line-info")
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} --compiler-options -fno-strict-aliasing --ptxas-options=-v --generate-line-info")
include_directories(${CUDA_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${CUDA_LIBRARIES})

# gstreamer
find_package(PkgConfig REQUIRED)
pkg_check_modules(GST_PKG REQUIRED IMPORTED_TARGET gstreamer-app-1.0)
target_include_directories(${PROJECT_NAME} PUBLIC ${GST_PKG_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PkgConfig::GST_PKG)
target_compile_options(${PROJECT_NAME} PUBLIC ${GST_PKG_CFLAGS_OTHER})

# deepstream
target_include_directories(${PROJECT_NAME} PUBLIC /opt/nvidia/deepstream/deepstream/sources/includes)
target_link_directories(${PROJECT_NAME} PUBLIC /opt/nvidia/deepstream/deepstream/lib)
target_link_libraries(${PROJECT_NAME} -lnvbufsurface -lnvbufsurftransform -lnvdsgst_helper -lnvds_batch_jpegenc 
                                        -lnvdsgst_meta -lnvds_meta -lnvinfer -lnvinfer_plugin -lnvds_inferutils 
                                        -lnvds_utils -lm -lnvds_infercustomparser)
# OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} -lstdc++fs)

# Json-glib
pkg_check_modules(JSON-GLIB REQUIRED json-glib-1.0)
include_directories(${JSON-GLIB_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} ${JSON-GLIB_LIBRARIES})

# Eigen 
find_package(Eigen3 3.3 REQUIRED)
target_include_directories(${PROJECT_NAME} PUBLIC ${EIGEN3_INCLUDE_DIR})

# librdkafka
pkg_check_modules(KAFKACPP REQUIRED IMPORTED_TARGET rdkafka++>=1.9.0 rdkafka>=1.9.0)
target_include_directories(${PROJECT_NAME} PUBLIC ${KAFKACPP_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PkgConfig::KAFKACPP)
target_compile_options(${PROJECT_NAME} PUBLIC ${KAFKACPP_CFLAGS_OTHER})

