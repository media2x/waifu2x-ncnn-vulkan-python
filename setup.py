#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import setuptools

import cmake_build_extension


cmake_flags = [
    "-DBUILD_SHARED_LIBS:BOOL=OFF",
    "-DCALL_FROM_SETUP_PY:BOOL=ON",
]
cmake_flags.extend(os.environ.get("CMAKE_FLAGS", "").split())

setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="waifu2x-ncnn-vulkan-python",
            install_prefix="waifu2x_ncnn_vulkan_python",
            write_top_level_init="from .waifu2x_ncnn_vulkan import Waifu2x",
            source_dir=str(
                pathlib.Path(__file__).parent / "waifu2x_ncnn_vulkan_python"
            ),
            cmake_configure_options=cmake_flags,
        )
    ],
    cmdclass={"build_ext": cmake_build_extension.BuildExtension},
)
