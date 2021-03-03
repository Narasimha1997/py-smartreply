#include "predictor.h"

#include<iostream>
#include<stdlib.h>

#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/op_resolver.h"
#include "tensorflow/lite/string_util.h"

static std::unique_ptr<::tflite::FlatBufferModel> model;

namespace tflite {
namespace custom {
namespace smartreply {
namespace runtime {

    void LoadModel(const char * path) {
        if(!path) {
            std::cout<<"Model File not found!\n";
            exit(0);
        }
        model = tflite::FlatBufferModel::BuildFromFile(path);
        if(!model) { 
            std::cout<<"Failed to load Model\n";
            exit(0); 
        }
    }

    std::map<std::string, float> MakePredictions(std::vector<std::string> inputs) {
        std::vector<smartreply::PredictorResponse> response;
        GetSegmentPredictions(inputs, *model, {{}}, &response);
        std::map<std::string, float> c_11_response;
        for(smartreply::PredictorResponse resp : response) 
           c_11_response[resp.GetText().data()] = resp.GetScore();
        
        return c_11_response;
    }
}}}}

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout<<"Provide model path as argument"<<std::endl;
        return 0;
    }

    tflite::custom::smartreply::runtime::LoadModel(argv[1]);

    std::vector<std::string> inputs = {"hello"};

    //make predictions
    std::map<std::string, float> preds = tflite::custom::smartreply::runtime::MakePredictions(inputs);

    for (std::pair<std::string, float> pred : preds) {
        std::cout<<pred.first<<" : " <<pred.second <<std::endl;
    }
    return 0;
}
