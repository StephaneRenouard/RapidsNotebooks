# Copyright (c) 2019-2020, NVIDIA CORPORATION.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cupy as cp

from ..utils._caches import _cupy_kernel_cache
from ..utils.helper_tools import _get_function, _get_tpb_bpg, _print_atts

_SUPPORTED_TYPES = [
    "int8",
    "uint8",
    "int16",
    "uint16",
    "int32",
    "uint32",
    "float32",
    "float64",
    "complex64",
    "complex128",
]


class _cupy_pack_wrapper(object):
    def __init__(self, grid, block, kernel):
        if isinstance(grid, int):
            grid = (grid,)
        if isinstance(block, int):
            block = (block,)

        self.grid = grid
        self.block = block
        self.kernel = kernel

    def __call__(self, out_size, binary, out):

        kernel_args = (out_size, binary, out)

        self.kernel(self.grid, self.block, kernel_args)


def _populate_kernel_cache(np_type, k_type):

    if np_type not in _SUPPORTED_TYPES:
        raise ValueError("Datatype {} not found for '{}'".format(np_type, k_type))

    if (str(np_type), k_type) in _cupy_kernel_cache:
        return

    _cupy_kernel_cache[(str(np_type), k_type)] = _get_function(
        "/io/_writer.fatbin",
        "_cupy_pack_" + str(np_type),
    )


def _get_backend_kernel(
    dtype,
    grid,
    block,
    k_type,
):

    kernel = _cupy_kernel_cache[(str(dtype), k_type)]
    if kernel:
        return _cupy_pack_wrapper(grid, block, kernel)
    else:
        raise ValueError("Kernel {} not found in _cupy_kernel_cache".format(k_type))


def _pack(binary):

    data_size = binary.dtype.itemsize * binary.shape[0]
    out_size = data_size

    out = cp.empty_like(binary, dtype=cp.ubyte, shape=out_size)

    threadsperblock, blockspergrid = _get_tpb_bpg()

    k_type = "pack"

    _populate_kernel_cache(out.dtype, k_type)

    kernel = _get_backend_kernel(
        out.dtype,
        blockspergrid,
        threadsperblock,
        k_type,
    )

    kernel(out_size, binary, out)

    _print_atts(kernel)

    # Remove binary data
    del binary

    return out
