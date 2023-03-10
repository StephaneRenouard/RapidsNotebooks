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

from setuptools import find_packages, setup

import versioneer

INSTALL_REQUIRES = ["numba"]

setup(
    name="cusignal",
    version=versioneer.get_version(),
    description="cuSignal - GPU Signal Processing",
    url="https://github.com/rapidsai/cusignal",
    author="NVIDIA Corporation",
    license="Apache 2.0",
    packages=find_packages(include=["cusignal", "cusignal.*"]),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
    package_data={"": ["*.fatbin"]},
)
