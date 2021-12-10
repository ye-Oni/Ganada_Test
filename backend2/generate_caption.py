from pickle import load
from numpy import argmax
import argparse
import os
from gtts.tts import gTTS
from keras.preprocessing.sequence import pad_sequences
from keras.applications.resnet import ResNet101
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.resnet import preprocess_input
from keras.models import Model
from keras.models import load_model
from keras import backend as K

def extract_features(filename):
	model = ResNet101()
	model.layers.pop()
	model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
	image = load_img(filename, target_size=(224, 224))
	image = img_to_array(image)
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	image = preprocess_input(image)
	feature = model.predict(image, verbose=0)
	return feature
 
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None
 

# def generate_desc(model, tokenizer, photo, max_length):
# 	in_text = 'startseq'
# 	for i in range(max_length):
# 		sequence = tokenizer.texts_to_sequences([in_text])[0]
# 		sequence = pad_sequences([sequence], maxlen=max_length)
# 		yhat = model.predict([photo,sequence], verbose=0)
# 		yhat = argmax(yhat)
# 		word = word_for_id(yhat, tokenizer)
# 		if word is None:
# 			break
# 		in_text += ' ' + word
# 		if word == 'endseq':
# 			break
# 	return in_text

def generate_desc(model, tokenizer, photo, max_length):
	in_text = 'startseq'
	for i in range(max_length):
		sequence = tokenizer.texts_to_sequences([in_text])[0]
		sequence = pad_sequences([sequence], maxlen=max_length)
		yhat = model.predict([photo,sequence], verbose=0)
		yhat = argmax(yhat)
		# print("{0} : {1}".format(i, yhat))
		word = word_for_id(yhat, tokenizer)
		if word is None:
			break
		in_text += ' ' + word
		if word == 'endseq':
			break
	return in_text

def generate_captions(photo_path):
        tokenizer = load(open('tokenizer.pkl', 'rb'))
        #tokenizer = load(open('features.pkl', 'rb'))
        max_length = 34
        model = load_model('model_300.h5')
        photo = extract_features(photo_path)
        description = generate_desc(model, tokenizer, photo, max_length)
        description = description[9:-6]
        return description

# K.clear_session()


# fileN = './test_image/Select_image/In_train_image/111766423_4522d36e56.jpg'
# print(generate_captions(fileN))

# K.clear_session()