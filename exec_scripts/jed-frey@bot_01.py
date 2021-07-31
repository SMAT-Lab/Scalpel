#!/usr/bin/env python
# coding: utf-8
# In[11]:
from jinja2 import Template
import os
os.chdir("../HAL/")
# In[4]:
class ArduinoIO(object):
    def __init__(self):
        self.items = list()
class Analog(object):
    def __init__(self, pin="A0"):
        if isinstance(pin, str):
            if pin[0]=="A":
                self.pin = int(pin[1:])
            else:
                self.pin = int(pin)
        else:
            self.pin = int(pin)
            
    @property
    def variable(self):
        return "analogValue_{}".format(self.pin)
        
    @property
    def header(self):
        return "int {} = 0;".format(self.variable)
    
    @property
    def loop(self):
        return """
  // Analog Input {pin}
  {variable} = analogRead({pin});
  Serial.print("A{pin}=");
  Serial.print({variable});
  Serial.print(",");
        """.format(pin = self.pin, variable = self.variable)
    
a0 = Analog(0)
a0.header
# In[5]:
arduino = ArduinoIO()
for i in range(6):
    arduino.items.append(Analog(i))
# In[15]:
ino = Template("""
{%- for item in arduino.items %}
{{ item.header }}
{%-endfor %}
void setup() {
  Serial.begin(115200);
  
}
void loop() {
{%- for item in arduino.items %}
{{- item.loop }}
{%-endfor %}
  Serial.println("");
  delay(2500);
}
""")
# In[16]:
with open("HAL.ino", "w") as fid:
    print(ino.render(arduino = arduino), file=fid)
# In[17]:
get_ipython().system('make')
get_ipython().system('make upload')
# In[18]: