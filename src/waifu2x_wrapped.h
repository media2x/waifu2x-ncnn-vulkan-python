#ifndef WAIFU2X_NCNN_VULKAN_WAIFU2X_WRAPPED_H
#define WAIFU2X_NCNN_VULKAN_WAIFU2X_WRAPPED_H
#include "waifu2x.h"

// wrapper class of ncnn::Mat
typedef struct Image {
    unsigned char *data;
    int w;
    int h;
    int elempack;
    Image(unsigned char *d, int w, int h, int channels)
    {
        this->data = d;
        this->w = w;
        this->h = h;
        this->elempack = channels;
    }

} Image;

union StringType {
    std::string *str;
    std::wstring *wstr;
};

class Waifu2xWrapped : public Waifu2x
{
  public:
    Waifu2xWrapped(int gpuid, bool tta_mode = false, int num_threads = 1);
    int load(const StringType &parampath, const StringType &modelpath);
    int process(const Image &inimage, Image &outimage) const;
    int process_cpu(const Image &inimage, Image &outimage) const;
    uint32_t get_heap_budget();

  private:
    int gpuid;
};

int get_gpu_count();
void destroy_gpu_instance();
#endif // WAIFU2X_NCNN_VULKAN_WAIFU2X_WRAPPED_H
