from . import smartreply

import os
import string



DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.tflite")
PUNCTUATIONS = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

class ModelNotFoundException(Exception):

    def __init__(self, model_path):
        self.model_path = model_path

    def __str__(self):
        return "Model file {} does not exist".format(self.model_path)

class ModelLoadFailedException(Exception):

    def __init__(self, model_path):
        self.model_path = model_path
    
    def __str__(self):
        return "Failed to load model {}, provide a proper TFLite model.".format(self.model_path)


class InvalidInputException(Exception):

    def __init__(self, required_type, got_type):
        self.input_type = got_type
        self.required_type = required_type
    
    def __str__(self):
        return "Input must be a {}, but got {}".format(self.required_type, self.input_type)

class SmartReplyRuntime :

    def __init__(self, model_file = DEFAULT_MODEL_PATH):
        if not os.path.exists(model_file):
            raise ModelNotFoundException(model_file)

        model_load_result = smartreply.load(model_file)
        if model_load_result == -1:
            raise ModelLoadFailedException(model_file) 

    
    def __remove_puncts(self, text):
        return "".join([ch for ch in text if ch not in PUNCTUATIONS])
    
    def predict(self, text):
        if not type(text) == str :
            raise InvalidInputException(str, type(text))

        clean_text = self.__remove_puncts(text)
        
        return smartreply.predict(clean_text)
    
    def predictMultiple(self, texts, batch = False) :
        if not type(texts) == list:
            raise InvalidInputException(list, type(texts))

        clean_texts = []

        for text in texts:
            if type(text) != str:
                raise InvalidInputException(str, type(text))
            clean_texts.append(self.__remove_puncts(text))

        if not batch: 
            return smartreply.multi_predict(clean_texts)

        return smartreply.batch_predict(clean_texts)