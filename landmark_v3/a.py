import time
startTime = time.time()
from keras.models import model_from_json, load_model
print(time.time()-startTime)
json_file = open("model.json", "r") 
loaded_model_json = json_file.read() 
json_file.close() 
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("weight_drawing.hdf5")
