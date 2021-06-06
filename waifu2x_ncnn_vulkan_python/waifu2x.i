%module waifu2x_ncnn_vulkan_wrapper

%include "cpointer.i"
%include "carrays.i"
%include "std_string.i"
%include "std_wstring.i"
%include "stdint.i"
%include "pybuffer.i"

%pybuffer_mutable_string(unsigned char *d);
%pointer_functions(std::string, str_p);
%pointer_functions(std::wstring, wstr_p);

%{
    #include "waifu2x.h"
    #include "waifu2x_wrapped.h"
%}

class Waifu2x
{
    public:
        Waifu2x(int gpuid, bool tta_mode = false, int num_threads = 1);
        ~Waifu2x();

    public:
        // waifu2x parameters
        int noise;
        int scale;
        int tilesize;
        int prepadding;
};

%include "waifu2x_wrapped.h"
