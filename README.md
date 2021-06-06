# waifu2x ncnn Vulkan Python

A Python FFI of nihui/waifu2x-ncnn-vulkan achieved with SWIG.

## Usages

```python
from waifu2x_ncnn_vulkan import Waifu2x
from PIL import Image

with Image.open("input.png") as image:
  waifu2x = Waifu2x(gpuid=0, scale=2, noise=3)
  image = waifu2x.process(image)
  image.save("output.png")
```

More descriptions are to be added.
