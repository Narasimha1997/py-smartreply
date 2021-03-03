from __future__ import absolute_import

import pytest
import smartreply


def test_load_default_model():
    #should load the default model automatically
    model = smartreply.SmartReplyRuntime()


def test_exception_on_unknwon_model():

    with pytest.raises(smartreply.ModelNotFoundException):
        model = smartreply.SmartReplyRuntime(model_file = "unknown_model.tflite")

def test_exception_on_improper_model():

    with pytest.raises(smartreply.ModelLoadFailedException):
        model = smartreply.SmartReplyRuntime(model_file = "tests/smartreply_samples.tsv")

def test_load_and_run_prediction():

    model = smartreply.SmartReplyRuntime()
    preds = model.predict(text = "I am good")

    assert(len(preds) != 0)

def test_load_and_run_prediction_multi():

    model = smartreply.SmartReplyRuntime()
    preds = model.predictMultiple(["hi how are you", "I am hungry"])

    assert(len(preds) == 2)
    for pred in preds:
        assert(len(pred) != 0)

def test_string_with_punctuation():

    model = smartreply.SmartReplyRuntime()
    pred = model.predict("Hi!! How are you???")
    
    assert(len(pred) != 0)

def test_exception_invalid_input():

    model = smartreply.SmartReplyRuntime()
    
    with pytest.raises(smartreply.InvalidInputException):
        model.predict(1022)
    
    with pytest.raises(smartreply.InvalidInputException):
        model.predictMultiple(["hello", "hi", 122, "doing good"])


