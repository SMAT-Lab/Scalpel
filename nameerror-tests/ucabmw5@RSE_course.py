import requests
spots=requests.get('http://www.sidc.be/silso/INFO/snmtotcsv.php')
spots.text.split('\n')[0]
import numpy as np
import requests
spots=requests.get('http://www.sidc.be/silso/INFO/snmtotcsv.php', stream=True)
sunspots= np.genfromtxt(spots.raw, delimiter=';')
sunspots[0][3]
from matplotlib import pyplot as plt
plt.plot(sunspots[:,2], sunspots[:,3]) # Numpy syntax to access all 
                                       #rows, specified column.
sunspots= np.genfromtxt(StringIO(spots), delimiter=';', 
                        names=['year','month','date',
                        'mean','deviation','observations','definitive'])
sunspots
spots=requests.get('http://www.sidc.be/silso/INFO/snmtotcsv.php')
from io import BytesIO
data = BytesIO(spots.content)
sunspots= np.genfromtxt(data, delimiter=';', 
                        names=['year','month','date',
                        'mean','deviation','observations','definitive'],
                        dtype=[int, int, float, float, float, int, int])
sunspots
sunspots['year']
plt.plot(sunspots['year'],sunspots['mean'])