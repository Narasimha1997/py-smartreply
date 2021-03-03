#ifndef __REGISTER_CUSTOM_OPS_H
#define __REGISTER_CUSTOM_OPS_H 1

#include <tensorflow/lite/context.h>
#include <tensorflow/lite/kernels/kernel_util.h>

namespace tflite
{
    namespace ops
    {
        namespace custom
        {
            namespace registry {
                TfLiteRegistration * Register_NORMALIZE();
                TfLiteRegistration * Register_EXTRACT_FEATURES();
                TfLiteRegistration * Register_PREDICT();
            }
        }
    } // namespace ops
} // namespace tflite

#endif