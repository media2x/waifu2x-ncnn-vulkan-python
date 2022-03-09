#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: waifu2x ncnn Vulkan Python wrapper
Author: ArchieMeng
Date Created: February 4, 2021
Last Modified: May 13, 2021

Dev: K4YT3X
Last Modified: February 5, 2022
"""

# built-in imports
import importlib
import pathlib
import sys

# third-party imports
from PIL import Image

# local imports
if __package__ is None:
    import waifu2x_ncnn_vulkan_wrapper as wrapped
else:
    wrapped = importlib.import_module(f"{__package__}.waifu2x_ncnn_vulkan_wrapper")


class Waifu2x:
    def __init__(
        self,
        gpuid: int = 0,
        scale: int = 2,
        noise: int = 0,
        tilesize: int = 0,
        model: str = "models-cunet",
        tta_mode: bool = False,
        num_threads: int = 1,
    ):
        """
        Waifu2x class which can do image super resolution.

        :param gpuid: the id of the gpu device to use. -1 for cpu mode.
        :param model: the name or the path to the model
        :param tta_mode: whether to enable tta mode or not
        :param num_threads: the number of threads in upscaling
        :param scale: scale level, 1 = no scaling, 2 = upscale 2x. value: float. default: 2
        :param noise: denoise level, large value means strong denoise effect, -1 = no effect. value: -1/0/1/2/3. default: 0
        :param tilesize: tile size. 0 for automatically setting the size. default: 0
        """

        # check arguments' validity
        assert scale in (1, 2), "scale must be 1 or 2"
        assert noise in range(-1, 4), "noise must be [-1, 3]"
        assert isinstance(tta_mode, bool), "tta_mode isn't a boolean value"
        assert num_threads >= 1, "num_threads must be an integer >= 1"

        self._waifu2x_object = wrapped.Waifu2xWrapped(gpuid, tta_mode, num_threads)
        self._model = model
        self._gpuid = gpuid
        self._waifu2x_object.scale = scale
        self._waifu2x_object.noise = noise
        self._waifu2x_object.tilesize = (
            self._get_tilesize() if tilesize <= 0 else tilesize
        )
        self._waifu2x_object.prepadding = self._get_prepadding()
        self._load()

    def _load(
        self, param_path: pathlib.Path = None, model_path: pathlib.Path = None
    ) -> None:
        """
        Load models from given paths. Use self.model if one or all of the parameters are not given.

        :param parampath: the path to model params. usually ended with ".param"
        :param modelpath: the path to model bin. usually ended with ".bin"
        :return: None
        """
        if param_path is None or model_path is None:
            model_path = pathlib.Path(self._model)
            if not model_path.is_dir():
                model_path = pathlib.Path(__file__).parent / "models" / self._model

            if self._waifu2x_object.noise == -1:
                param_path = model_path / "scale2.0x_model.param"
                model_path = model_path / "scale2.0x_model.bin"
                self._waifu2x_object.scale = 2
            elif self._waifu2x_object.scale == 1:
                param_path = (
                    model_path / f"noise{self._waifu2x_object.noise}_model.param"
                )
                model_path = model_path / f"noise{self._waifu2x_object.noise}_model.bin"
            elif self._waifu2x_object.scale == 2:
                param_path = (
                    model_path
                    / f"noise{self._waifu2x_object.noise}_scale2.0x_model.param"
                )
                model_path = (
                    model_path
                    / f"noise{self._waifu2x_object.noise}_scale2.0x_model.bin"
                )

        if param_path.exists() and model_path.exists():
            param_path_str, model_path_str = wrapped.StringType(), wrapped.StringType()
            if sys.platform in ("win32", "cygwin"):
                param_path_str.wstr = wrapped.new_wstr_p()
                wrapped.wstr_p_assign(param_path_str.wstr, str(param_path))
                model_path_str.wstr = wrapped.new_wstr_p()
                wrapped.wstr_p_assign(model_path_str.wstr, str(model_path))
            else:
                param_path_str.str = wrapped.new_str_p()
                wrapped.str_p_assign(param_path_str.str, str(param_path))
                model_path_str.str = wrapped.new_str_p()
                wrapped.str_p_assign(model_path_str.str, str(model_path))

            self._waifu2x_object.load(param_path_str, model_path_str)
        else:
            raise FileNotFoundError(f"{param_path} or {model_path} not found")

    def process(self, image: Image) -> Image:
        """
        Process the incoming PIL.Image

        :param im: PIL.Image
        :return: PIL.Image
        """
        in_bytes = bytearray(image.tobytes())
        channels = int(len(in_bytes) / (image.width * image.height))
        out_bytes = bytearray((self._waifu2x_object.scale ** 2) * len(in_bytes))

        raw_in_image = wrapped.Image(in_bytes, image.width, image.height, channels)
        raw_out_image = wrapped.Image(
            out_bytes,
            self._waifu2x_object.scale * image.width,
            self._waifu2x_object.scale * image.height,
            channels,
        )

        if self._gpuid != -1:
            self._waifu2x_object.process(raw_in_image, raw_out_image)
        else:
            self._waifu2x_object.tilesize = max(image.width, image.height)
            self._waifu2x_object.process_cpu(raw_in_image, raw_out_image)

        return Image.frombytes(
            image.mode,
            (
                self._waifu2x_object.scale * image.width,
                self._waifu2x_object.scale * image.height,
            ),
            bytes(out_bytes),
        )

    def _get_prepadding(self) -> int:
        if self._model == "models-cunet":
            if self._waifu2x_object.noise == -1:
                return 18
            elif self._waifu2x_object.scale == 1:
                return 28
            elif self._waifu2x_object.scale == 2:
                return 18
            else:
                return 18
        elif self._model == "models-upconv_7_anime_style_art_rgb":
            return 7
        elif self._model == "models-upconv_7_photo":
            return 7
        else:
            raise ValueError(f'model "{self._model}" is not supported')

    def _get_tilesize(self):
        if self._gpuid == -1:
            return 4000
        else:
            heap_budget = self._waifu2x_object.get_heap_budget()
            if "models-cunet" in self._model:
                if heap_budget > 2600:
                    return 400
                elif heap_budget > 740:
                    return 200
                elif heap_budget > 250:
                    return 100
                else:
                    return 32
            else:
                if heap_budget > 1900:
                    return 400
                elif heap_budget > 550:
                    return 200
                elif heap_budget > 190:
                    return 100
                else:
                    return 32
