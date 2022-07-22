# waifu2x ncnn Vulkan Python

![CI](https://github.com/media2x/waifu2x-ncnn-vulkan-python/workflows/CI/badge.svg)

## Introduction

A Python FFI of nihui/waifu2x-ncnn-vulkan achieved with SWIG.

[waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan) is nihui's ncnn implementation of waifu2x converter. Runs fast on Intel / AMD / Nvidia with Vulkan API.

This project only wrapped the original Waifu2x class. As a result, functions other than the core upscaling and denoising such as multi-thread loading and saving are not available. Of course, the auto tilesize and prepadding settings are implemented, so don't worry about them.

## Download

linux x64, Windows x64 and MacOS x64 releases are available now. For other platforms, you may compile it on your own.
The reason why MacOS ARM64 build is not available is that it needs ARM Python Dev Libs which I have no ideas on how to
get it on Github's MacOS x64 VM. Moreover, I don't have a Mac.

- ~~**However, for Linux (Like Ubuntu 18.04) with an older GLIBC (version < 2.29), you may try to use the ubuntu-1804 release or just compile it on your own.**~~
- ~~**Windows release is not working for all python version. The version of Windows build is for python 3.9. This is a known issue: [ImportError: DLL load failed while importing _rife_ncnn_vulkan_wrapper: The specified module could not be found.](https://github.com/ArchieMeng/rife-ncnn-vulkan-python/issues/1)**~~
- **Updates:**
    - The binary wheel releases on Github are now linked with specific python version. Please download the right one according to your python version.
    - it has been uploaded to PyPI, and you can install it with pip now. But you need to have all the **build dependencies** (SWIG and Vulkan Dev) installed. Because the PYPI package of this lib is a source distribution.

## Installation
```shell
pip install waifu2x-ncnn-vulkan-python
```

## Build

First, you have to install python, python development package (Python native development libs in Visual Studio), vulkan SDK and SWIG on your platform. And then, there are two ways to build it:
- Use setuptools to build and install into python package directly. (Currently in developing)
- Use CMake directly (The old way)

### Use setuptools
```shell
python setup.py install
```

### Use CMake

#### Linux
1. install dependencies: cmake, vulkan sdk, swig and python-dev

##### Debian, Ubuntu and other Debian-like Distros
```shell
apt-get install cmake libvulkan-dev swig python3-dev
```

##### Arch Distros
```shell
pacman -S base-devel cmake vulkan-headers vulkan-icd-loader swig python
```

2. Build with CMake
```shell
git clone --recursive https://github.com/media2x/waifu2x-ncnn-vulkan-python.git
cd waifu2x-ncnn-vulkan-python
cmake -B build -S waifu2x_ncnn_vulkan_python
cmake --build build
```

#### Windows
I used Visual Studio 2019 and msvc v142 to build this project for Windows.

Install visual studio and open the project directory, and build. Job done.

One way is [using Visual Studio to open the project as directory](https://www.microfocus.com/documentation/visual-cobol/vc50/VS2019/GUID-BE1C48AA-DB22-4F38-9644-E9B48658EF36.html), and build it from Visual Studio.
And another way is build it from powershell just like what is written in the [release.yml](.github/workflows/release.yml)

#### Mac OS X
1. install dependencies: cmake, vulkan sdk, swig and python-dev

- download vulkan sdk from https://vulkan.lunarg.com/sdk/home
- If you have homebrew installed, run the command below to get SWIG

```shell
brew install swig
```
- I guess python dev is out-of-box in Mac. If not, google it.
    
2. Build with CMake

- You can pass -DUSE_STATIC_MOLTENVK=ON option to avoid linking the vulkan loader library on MacOS
- The remaining steps are similar to Linux.

## Usages

### Example program

```python
from PIL import Image
from waifu2x_ncnn_vulkan import Waifu2x

with Image.open("input.png") as image:
  waifu2x = Waifu2x(gpuid=0, scale=2, noise=3)
  image = waifu2x.process(image)
  image.save("output.png")
```

## [Docs](Docs.md)

## Known issues
- [Module finalization will crash for nvidia dedicated graphics card(s) on Linux. (The image processing still works.)](https://github.com/Tencent/ncnn/issues/2666)
- Not yet tested for Mac OS. I guess it should work.

## Software that uses this package

- [Video2x](https://github.com/k4yt3x/video2x)
- [SAE](https://github.com/Justin62628/Squirrel-RIFE)

## Original waifu2x Project

- https://github.com/nagadomi/waifu2x
- https://github.com/lltcggie/waifu2x-caffe
- https://github.com/nihui/waifu2x-ncnn-vulkan

## Other Open-Source Code Used

- https://github.com/Tencent/ncnn for fast neural network inference on ALL PLATFORMS
