#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pathlib
import setuptools
import sys

os.environ.pop("PYTHONNOUSERSITE")
sys.path.append(
    str(
        pathlib.Path.home()
        / ".local/lib/python{}.{}/site-packages".format(
            sys.version_info.major, sys.version_info.minor
        )
    )
)
sys.path.append(
    "/usr/lib/python{}.{}/site-packages".format(
        sys.version_info.major, sys.version_info.minor
    )
)

import cmake_build_extension

setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="waifu2x-ncnn-vulkan-python",
            install_prefix="waifu2x_ncnn_vulkan_python",
            write_top_level_init="from .waifu2x_ncnn_vulkan import Waifu2x",
            source_dir=str(
                pathlib.Path(__file__).parent / "waifu2x_ncnn_vulkan_python"
            ),
            cmake_configure_options=[
                "-DBUILD_SHARED_LIBS:BOOL=OFF",
                "-DCALL_FROM_SETUP_PY:BOOL=ON",
            ],
        )
    ],
    cmdclass={"build_ext": cmake_build_extension.BuildExtension},
)
