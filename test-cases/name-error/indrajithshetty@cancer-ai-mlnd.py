#!/usr/bin/env python
# coding: utf-8
# In[3]:
#val data generator
val_datagen = ImageDataGenerator(rescale=1. / 255)
    # this is a similar generator, for validation data
validation_generator = val_datagen.flow_from_directory(
        '../data/valid',
        target_size=(input_h, input_h),
        batch_size=batch_size,
        class_mode=None,
        seed=1)
# In[4]:
#test data generator
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator=test_datagen.flow_from_directory(
        '../data/test',
        target_size=(input_h, input_h),
        batch_size=batch_size,
        class_mode='categorical')
# In[5]:
score=model.evaluate_generator(test_generator)
score[1]
# In[6]:
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
# In[8]:
df1= pd.DataFrame(columns=['Id','task_1','task_2'])
df1=df1.append(pd.DataFrame({'Id':Id,'task_1':task1,'task_2':task2}))
df1.to_csv('sample.csv',index=False)