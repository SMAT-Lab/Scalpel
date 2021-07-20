from my_model import MyModel
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator,load_img,img_to_array
input_h=150
batch_size = 100
import pprint
pp=pprint.pprint
model=  MyModel().get_model(input_h)
model.load_weights('first_try.h5')
#val data generator
val_datagen = ImageDataGenerator(rescale=1. / 255)
    # this is a similar generator, for validation data
validation_generator = val_datagen.flow_from_directory(
        '../data/valid',
        target_size=(input_h, input_h),
        batch_size=batch_size,
        class_mode=None,
        seed=1)
#test data generator
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator=test_datagen.flow_from_directory(
        '../data/test',
        target_size=(input_h, input_h),
        batch_size=batch_size,
        class_mode='categorical')
score=model.evaluate_generator(test_generator)
score[1]
print(validation_generator.class_indices)
import pandas as pd
df= pd.DataFrame(columns=['Id','task_1','task_2'])
Id=list()
task1=list()
task2=list()
for filename in validation_generator.filenames:
    fullpath=validation_generator.directory+"/"+filename
    img =load_img(fullpath, target_size=(input_h, input_h))
    x = img_to_array(img)
    x=x/255
    x = x.reshape((1,) + x.shape)
    pred=model.predict(x)
    filename_for_csv="data/test/"+filename
    Id.append(filename_for_csv)
    
    task1.append(pred[0][0])
    task2.append(pred[0][2])
    df=df.append(pd.DataFrame({'Id':Id,'task_1':task1,'task_2':task2}))
    
df.to_csv('sample.csv',index=False)
    
print(test_generator.class_indices)
import pandas as pd
df= pd.DataFrame(columns=['Id','task_1','task_2'])
Id=list()
task1=list()
task2=list()
for filename in test_generator.filenames:
    fullpath=test_generator.directory+"/"+filename
    img =load_img(fullpath, target_size=(input_h, input_h))
    x = img_to_array(img)
    x=x/255
    x = x.reshape((1,) + x.shape)
    pred=model.predict(x)
    filename_for_csv="data/test/"+filename
    Id.append(filename_for_csv)
    
    task1.append(pred[0][0])
    task2.append(pred[0][2])
df1= pd.DataFrame(columns=['Id','task_1','task_2'])
df1=df1.append(pd.DataFrame({'Id':Id,'task_1':task1,'task_2':task2}))
df1.to_csv('sample.csv',index=False)