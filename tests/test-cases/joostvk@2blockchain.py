#!/usr/bin/env python
# coding: utf-8
# In[47]:
config_path = os.path.abspath(os.path.join(os.getcwd(), 'app.cfg'))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', 'lib')))
# In[48]:
config_path
# In[49]:
import configparser
# In[50]:
import sys, os
config_path = os.path.abspath(os.path.join(os.getcwd(), 'app.cfg'))
import json
from datautils import get_connection, read_config, sql_fetchone, to_onesignal, execute_sql
# In[51]:
config = read_config(config_path,['2blockchain'])
# In[52]:
config
# In[42]:
pymssql.connect(database= 'alerts',password= 'KtvF62dArWTQvGCg6dAx',server= 'datactively.database.windows.net',user= 'alerts@datactively.database.windows.net')
# In[53]:
x = get_connection(config['2blockchain'])
# In[21]:
SELECT_USER_QUERY = """
SELECT * FROM DBO.USERS
WHERE email_address = '{email_address}';
"""
http = HTTPHelper()
http_params = http.post
print "HTTP Post parameters: {}".format(http_params)
email_address = get_param_value(http_params, 'email_address', ptype=str, 
                                pmatch='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
config_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'app.cfg'))
config = read_config(config_path, ['alerts_db'])
with get_connection(config['alerts_db']) as conn:
    user_rowcount = execute_sql(conn, UPDATE_USER_QUERY.format(user_id=user_id,
                                                               email_address=email_address))
    device_rowcount = execute_sql(conn, UPDATE_DEVICE_QUERY.format(user_id=user_id,
                                                                   device_id=device_id))
    print 'updating {} rows in users'.format(user_rowcount)
    print 'updating {} rows in devices'.format(device_rowcount)
    
    if (user_rowcount==1) and (device_rowcount==1):
        conn.commit()
    else:
        raise Exception('Expected number of rows to be updated 1 for users and 1 for devices, observed differently.')