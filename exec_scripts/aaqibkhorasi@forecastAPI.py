#!/usr/bin/env python
# coding: utf-8
# In[14]:
import pandas as pd
def getData(report, date, locations):
    """
    Get the precipitation probability of all the locations for
    the given date
    """
    data = []
    for location in locations:
        try:
            data.append(report[location]['weather'][date]['precipProbability']*100)
        except:
            data.append('NaN')
    return data
frames=[]
locations = []
data=[]
pivotTable={}
locations.append('9be000ae23275d57e1273d211a54ffd7')
locations.append('a35e427b4130be7b2a892e286f0ebb91')
report={"9be000ae23275d57e1273d211a54ffd7": {"weather": {"2017-02-01": {"apparentTemperatureMinTime": 1485907200, "precipType": "rain", "cloudCover": 0.95, "temperatureMin": 46.65, "summary": "Foggy in the morning.", "dewPoint": 48.09, "apparentTemperatureMax": 50.46, "temperatureMax": 50.46, "temperatureMaxTime": 1485961200, "windBearing": 173, "moonPhase": 0.15, "visibility": 4.39, "sunsetTime": 1485967844, "pressure": 1006.49, "apparentTemperatureMin": 42.53, "icon": "fog", "apparentTemperatureMaxTime": 1485961200, "humidity": 0.96, "windSpeed": 8.52, "time": 1485907200, "sunriseTime": 1485934901, "temperatureMinTime": 1485907200}, "2017-02-02": {"apparentTemperatureMinTime": 1485907200, "precipType": "rain", "cloudCover": 0.95, "temperatureMin": 46.65, "summary": "Foggy in the morning.", "dewPoint": 48.09, "apparentTemperatureMax": 50.46, "temperatureMax": 50.46, "temperatureMaxTime": 1485961200, "windBearing": 173, "moonPhase": 0.15, "visibility": 4.39, "sunsetTime": 1485967844, "pressure": 1006.49, "apparentTemperatureMin": 42.53, "icon": "fog", "apparentTemperatureMaxTime": 1485961200, "humidity": 0.96, "windSpeed": 8.52, "time": 1485907200, "precipProbability": 0.5, "sunriseTime": 1485934901, "temperatureMinTime": 1485907200}}}
,"a35e427b4130be7b2a892e286f0ebb91": {"weather": {"2017-02-04": {"apparentTemperatureMinTime": 1485907200, "precipType": "rain", "cloudCover": 0.95, "temperatureMin": 46.65, "summary": "Foggy in the morning.", "dewPoint": 48.09, "apparentTemperatureMax": 50.46, "temperatureMax": 50.46, "temperatureMaxTime": 1485961200, "windBearing": 173, "moonPhase": 0.15, "visibility": 4.39, "sunsetTime": 1485967844, "pressure": 1006.49, "apparentTemperatureMin": 42.53, "icon": "fog", "apparentTemperatureMaxTime": 1485961200, "humidity": 0.96, "windSpeed": 8.52, "time": 1485907200, "sunriseTime": 1485934901, "temperatureMinTime": 1485907200}, "2017-02-05": {"apparentTemperatureMinTime": 1485907200, "precipType": "rain", "cloudCover": 0.95, "temperatureMin": 46.65, "summary": "Foggy in the morning.", "dewPoint": 48.09, "apparentTemperatureMax": 50.46, "temperatureMax": 50.46, "temperatureMaxTime": 1485961200, "windBearing": 173, "moonPhase": 0.15, "visibility": 4.39, "sunsetTime": 1485967844, "pressure": 1006.49, "apparentTemperatureMin": 42.53, "icon": "fog", "apparentTemperatureMaxTime": 1485961200, "humidity": 0.96, "windSpeed": 8.52, "time": 1485907200, "precipProbability": 0.75, "sunriseTime": 1485934901, "temperatureMinTime": 1485907200}}}
}
#report = {"9be000ae23275d57e1273d211a54ffd7": {"weather": {"2017-02-01": {"apparentTemperatureMinTime": 1485907200, "precipType": "rain", "cloudCover": 0.95, "temperatureMin": 46.65, "summary": "Foggy in the morning.", "dewPoint": 48.09, "apparentTemperatureMax": 50.46, "temperatureMax": 50.46, "temperatureMaxTime": 1485961200, "windBearing": 173, "moonPhase": 0.15, "visibility": 4.39, "sunsetTime": 1485967844, "pressure": 1006.49, "apparentTemperatureMin": 42.53, "icon": "fog", "apparentTemperatureMaxTime": 1485961200, "humidity": 0.96, "windSpeed": 8.52, "time": 1485907200, "sunriseTime": 1485934901, "temperatureMinTime": 1485907200}, "2017-02-02": {"apparentTemperatureMinTime": 1485907200, "precipType": "rain", "cloudCover": 0.95, "temperatureMin": 46.65, "summary": "Foggy in the morning.", "dewPoint": 48.09, "apparentTemperatureMax": 50.46, "temperatureMax": 50.46, "temperatureMaxTime": 1485961200, "windBearing": 173, "moonPhase": 0.15, "visibility": 4.39, "sunsetTime": 1485967844, "pressure": 1006.49, "apparentTemperatureMin": 42.53, "icon": "fog", "apparentTemperatureMaxTime": 1485961200, "humidity": 0.96, "windSpeed": 8.52, "time": 1485907200, "precipProbability": 0.75, "sunriseTime": 1485934901, "temperatureMinTime": 1485907200}}}}
frames.append(pd.DataFrame.from_dict(report['9be000ae23275d57e1273d211a54ffd7']['weather']))
frames.append(pd.DataFrame.from_dict(report['a35e427b4130be7b2a892e286f0ebb91']['weather']))
allDates = ['2017-02-01','2017-02-02','2017-02-04','2017-02-05']
t = pd.concat(frames, keys=locations)
t.index.set_names(['loc_id', 'weather'], inplace=True)
t.to_csv('weatherreport.csv')
for date in allDates:
    pivotTable[date] = pd.Series((getData(report, date, locations)), index=locations)
print( pd.DataFrame(pivotTable))