import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import os

# cuda disable
os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 

# MobileNet model load
model = load_model('MobileNetV2.h5')
 

def image_classification(img_path = './test4.jpg') :
	# cuda disable
	os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 

# MobileNet model load
	model = load_model('MobileNetV2.h5')
	# img_path = './test4.jpg'
	img = image.load_img(img_path, target_size=(224, 224))
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x)
	
	preds = model.predict(x)
	print('Predicted:', decode_predictions(preds, top=3)[0])

	pred_list = decode_predictions(preds, top=1)[0]
	print('class name : ', pred_list[0][0])
	print('class_description : ', pred_list[0][1])
	print('score : ', pred_list[0][2])

	# https://gist.github.com/aaronpolhamus/964a4411c0906315deb9f4a3723aac57 
	# imageNet -> map_clsolc.txt

	dog_list = ['n02096437', '0', '1', '2', '3']

	if pred_list[0][0] in dog_list  :
		print('It is Dog!!')
		return "Dog"
	return "-1"

if __name__=='__main__' :
	print(image_classification())