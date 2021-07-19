import requests
import json
r = requests.get('http://3d-kenya.chordsrt.com/instruments/1.geojson?start=2016-09-01T00:00&end=2016-11-01T00:00')
if r.status_code == 200:
    d = r.json()['Data']
else:
    print("Please verify that the URL for the weather station is correct. You may just have to try again with a different/smaller date range or different dates.")
d
for o in d:
    if o['variable_shortname'] == 'msl1':
        print(o['time'], o['value'], o['units'])
davad_tuple = (
    'f1',
    'f2',
    'f3',
    'f4',
    'f5',
    'f6',
    'f7',
    'f8',
    'f9',
    'f10',
    'f11',
    'f12',
    'f13',
    'f14',
)
def make_data_set(d):
    data_list = []
    for o in d:
        if o['variable_shortname'] == 'rain':
            t = o['time'].split("T")
            tdate = t[0].replace('-', '')
            ttime = ''.join(t[1].split(':')[:-1])
            rain = o['value']
            if ttime.endswith('00') or ttime.endswith('15') or ttime.endswith('30') or ttime.endswith('45'):
                davad_tuple = ['DAVAD', 'GLIDGDTR', 'SITE_ID:45015']+['X']*11
                davad_tuple[3] = tdate + ttime
                davad_tuple[11] = str(rain)
                data_list.append('{}'.format(' '.join(davad_tuple)))
    #print('//AA\n{}\n//ZZ'.format('\n'.join(data_list)))
    return data_list
make_data_set(d)
def email_data(data_list):
    import os
    
    from sparkpost import SparkPost
    
    FROM_EMAIL = os.getenv('FROM_EMAIL')
    BCC_EMAIL = os.getenv('BCC_EMAIL')
    # Send email using the SparkPost api
    sp = SparkPost() # uses environment variable named SPARKPOST_API_KEY
    response = sp.transmission.send(
            recipients=['data@globe.gov'],
            bcc=[BCC_EMAIL],
            text='//AA\n{}\n//ZZ'.format('\n'.join(data_list)),
            from_email=FROM_EMAIL,
            subject='DATA'
    )
    print(response)
email_data(make_data_set(d))