#include "waifu2x_wrapped.h"

int Waifu2xWrapped::process(const Image &inimage, Image &outimage) const
{
    int c = inimage.elempack;
    ncnn::Mat inimagemat =
        ncnn::Mat(inimage.w, inimage.h, (void *)inimage.data, (size_t)c, c);
    ncnn::Mat outimagemat =
        ncnn::Mat(outimage.w, outimage.h, (void *)outimage.data, (size_t)c, c);
    return Waifu2x::process(inimagemat, outimagemat);
}

int Waifu2xWrapped::process_cpu(const Image &inimage, Image &outimage) const
{
    int c = inimage.elempack;
    ncnn::Mat inimagemat =
        ncnn::Mat(inimage.w, inimage.h, (void *)inimage.data, (size_t)c, c);
    ncnn::Mat outimagemat =
        ncnn::Mat(outimage.w, outimage.h, (void *)outimage.data, (size_t)c, c);
    return Waifu2x::process_cpu(inimagemat, outimagemat);
}

Waifu2xWrapped::Waifu2xWrapped(int gpuid, bool tta_mode, int num_threads)
    : Waifu2x(gpuid, tta_mode, num_threads)
{
    this->gpuid = gpuid;
}

uint32_t Waifu2xWrapped::get_heap_budget()
{
    return ncnn::get_gpu_device(this->gpuid)->get_heap_budget();
}

int Waifu2xWrapped::load(const StringType &parampath,
                         const StringType &modelpath)
{
#if _WIN32
    return Waifu2x::load(*parampath.wstr, *modelpath.wstr);
#else
    return Waifu2x::load(*parampath.str, *modelpath.str);
#endif
}

int get_gpu_count() { return ncnn::get_gpu_count(); }

void destroy_gpu_instance() { ncnn::destroy_gpu_instance(); }