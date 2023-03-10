# =============================================================================
# Copyright (c) 2022, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
# =============================================================================

cmake_minimum_required(VERSION 3.23.1 FATAL_ERROR)

set(cuspatial_version 23.02.00)

file(DOWNLOAD https://raw.githubusercontent.com/rapidsai/rapids-cmake/branch-23.02/RAPIDS.cmake
     ${CMAKE_BINARY_DIR}/RAPIDS.cmake)
include(${CMAKE_BINARY_DIR}/RAPIDS.cmake)

project(
  cuspatial-python
  VERSION ${cuspatial_version}
  LANGUAGES # TODO: Building Python extension modules via the python_extension_module requires the C
            # language to be enabled here. The test project that is built in scikit-build to verify
            # various linking options for the python library is hardcoded to build with C, so until
            # that is fixed we need to keep C.
            C CXX)

option(FIND_CUSPATIAL_CPP "Search for existing cuspatial C++ installations before defaulting to local files"
       OFF)

# If the user requested it we attempt to find cuspatial.
if(FIND_CUSPATIAL_CPP)
  find_package(cuspatial ${cuspatial_version})
else()
  set(cuspatial_FOUND OFF)
endif()

if(NOT cuspatial_FOUND)
  # TODO: This will not be necessary once we upgrade to CMake 3.22, which will
  # pull in the required languages for the C++ project even if this project
  # does not require those languges.
  include(rapids-cuda)
  rapids_cuda_init_architectures(cuspatial)
  enable_language(CUDA)
  # Since cuspatial only enables CUDA optionally we need to manually include the file that
  # rapids_cuda_init_architectures relies on `project` including.
  include("${CMAKE_PROJECT_cuspatial_INCLUDE}")

  add_subdirectory(../../cpp cuspatial-cpp)

  install(TARGETS cuspatial DESTINATION cuspatial/_lib)
endif()

include(rapids-cython)
rapids_cython_init()

add_subdirectory(cuspatial/_lib)
