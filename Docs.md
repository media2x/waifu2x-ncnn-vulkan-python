# Docs

## Methods
class **Waifu2x**(
gpuid: int = 0,
scale: int = 2,
noise: int = 0,
tilesize: int = 0,
model: str = "models-cunet",
tta_mode: bool = False,
num_threads: int = 1,
)

> waifu2x-ncnn-vulkan class which can do image super resolution.
>
> ### **Parameters**
>
> **gpuid**: int
> >the id of the gpu device to use. -1 for cpu mode.
>
> **model**: str
> > the name or the path to the model
>
> **tta_mode**: bool
> > whether to enable tta mode or not
>
> **num_threads**: int
> > the number of threads in upscaling
> >
> > default 1
>
> **scale**: int
> > scale level, 1 = no scaling, 2 = upscale 2x
> >
> > value: float. default: 2
>
> **noise**: int
> > denoise level, large value means strong denoise effect, -1 = no effect
> >
> > value: -1/0/1/2/3. default: -1
>
> **tilesize**: int
> > tile size, use smaller value to reduce GPU memory usage, default selects automatically
> >
> > 0 for automatically setting the size. default: 0

Waifu2x.**process**(self, im: PIL.Image)
> Process the incoming PIL.Image
>
> ### **Parameters**
>
> **im**: PIL.Image
> > the image object to process
>
> ### **Returns**: PIL.Image
> > The result PIL.Image object.

### Properties

Waifu2x.**gpuid**
> The id of gpu this Waifu2x Object is using.
>
Waifu2x.**model**
> The model name or path this object is going to use. Waifu2x.load() should be called manually after updating this property.
>
Waifu2x.**scale**
> The result scale ratio. It is different to the self._raw_w2xobj.scale. Waifu2x.scale controls the result scale size while
> self._raw_w2xobj.scale controls the scale ratio at each raw image process method call.
>
> ( Waifu2x.**_process**(im) is the raw image process call. A upscaling task is done by repeatedly calling 2 times super-resolution)
>
Waifu2x.**_waifu2x_object**
> The raw binding object of the original Waifu2x class. All the processing parameters are actually passed to this object eventually.
>
> It is not recommend to operate on this object directly since there are many important parameter settings like tilesize setting have already been included in Python Waifu2x class.