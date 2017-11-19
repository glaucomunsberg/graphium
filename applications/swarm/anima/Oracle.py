#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keras, os

from system.Graphium import Graphium
from system.Logger import Logger
from assistant.Scissor import Scissor
from keras.applications.vgg16 import VGG16,preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.models import model_from_json
import numpy as np

class Oracle:

    _instance   = None
    _logger     = None
    _g          = None
    models      = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,model_name="20170821191051",logger=None):

        self._g                 = Graphium()
        self.path_model_json    = self._g.path_model()+model_name+".json"
        self.path_model_weights = self._g.path_model()+model_name+".h5"

        if not os.path.isfile(self.path_model_json):
            self._logger.info('Oracle: The model is not valid file '+self.path_model_json)
            raise ValueError('The path_model_weights is not a model.json to by used')
        if not os.path.isfile(self.path_model_weights):
            self._logger.info('Oracle: The weights is not valid file '+self.path_model_weights)
            raise ValueError('The path_model_weights is not a valid weights to by used')

        if logger != None:
            self._logger = logger
        else:
            self._logger = Logger('Oracle')

        try:
            json_file = open(self.path_model_json, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            self.model = model_from_json(loaded_model_json)
            self._logger.info('Mananger: Loading model at '+self.path_model_json)
        except:
            self._logger.error('Mananger: Error at loading model from file '+str(self.path_model_json))
            self.model = VGG16(weights='imagenet', include_top=True)

        self.model.load_weights(self.path_model_weights)
        self.model._make_predict_function() # fixing problem `ValueError("Tensor %s is not an element of this graph." % obj)`

    #
    # predictInPano
    #   check if the image in size of be analise at prediction keras
    #   load a model and weights keras
    #   predict if is or no a image wanted
    #   return true or false
    def predictInPano(self,image_path):

        scissor = Scissor(image_path)
        image_path = scissor.cut_to_fit(self._g.path_picture()+"scissor/")
        img = image.load_img(image_path, target_size=(self._g.scissor['target_min_width'], self._g.scissor['target_min_height']))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        self._logger.info('Oracle: Appending image {0} to predict'.format(image_path))
        predictions     = self.model.predict(x)
        nameProbability = decode_predictions(predictions, top=1)[0]
        print 'Probabilities', nameProbability
        print 'Probability  ', nameProbability[0][0]
        print 'Image Path   ', image_path
        if nameProbability[0][1] == "comic book" or nameProbability[0][0] == "n06596364":
            return True
        else:
            return False
