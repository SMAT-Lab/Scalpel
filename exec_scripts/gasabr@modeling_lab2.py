#!/usr/bin/env python
# coding: utf-8
# In[1]:
import simpy
import numpy as np
import pandas as pd
from random import expovariate, seed
# In[2]:
# global constants
N_PROCESSORS = 1
N_REQUESTS = 2000
MAX_QUEUE_LEN = 100
AVG_REQUEST_INTERVAL = 700
AVG_SERVING_TIME = 100
MAX_TIME = 30000
SEED = 42
seed(SEED)
payload_balance = {
    30000: {
        0.1: {'a': 700, 'b': 100},
        0.9: {'a': 104, 'b': 100},
    },
    20000: {
        0.1: {'a': 1100, 'b': 100},
        0.9: {'a': 104, 'b': 100},
    },
    10000: {
        0.1: {'a': 450, 'b': 100},
        0.9: {'a': 104, 'b': 100},
    },
    8000: {
        0.1: {'a': 450, 'b': 100},
        0.9: {'a': 102, 'b': 100},
    },
    6000: {
        0.1: {'a': 450, 'b': 100},
        0.9: {'a': 102, 'b': 100},
    }
}
n_requests = [10, 100, 500, 2000, 4000, 6000, 8000, 10000, 20000, 30000, 50000, 100000, 150000]
# In[3]:
class ProcessMonitor:
    ''' Collects the data about running inside process. 
    
    This class does not pretend to be general by any means.
    
    Attributes:
        env(simpy.Environment): to not use the global env each monitored
            object has its own env
        resource(simpy.Resource): resource being monitored
        _serving_time(list of floats): amounts of time that were spend to
            serve request
        _waiting_time(list of floats): amounts of time requests had to wait
            until they would be served
        _entry_time(list of float): times when events arrived at the 
            processor/queue
        _num_rejected(int): amount of rejected request. Would be better to make
            it list of times.
    '''
    def __init__(self, env, resource):
        self.env = env
        self.resource = resource
        
        self._serving_time = []
        self._waiting_time = []
        self._entry_time = []
        self._num_rejected = 0
        
    def collect_data(self, n_requests, avg_request_interval, avg_serving_time, max_time):
        ''' Gets results of simulation with given parameters. 
        
        Args:
            n_requests(int)            : number of jobs/request in simulation
            avg_request_interval(float): in term of model this is `a`
            avg_serving_time(float)    : in term of model this is `b`
            max_time(int)              : time limit of simulation
            
        Note: 
            to start a new simulation you should restart environment by doing
            `env = simpy.Environment(0)`.
        '''
        self.n_requests = n_requests
        self._avg_request_interval = avg_request_interval
        self._avg_serving_time = avg_serving_time
        
        self.env.process(self._generate_requests())
        self.env.run(until=max_time)
        
        return {
            'n_requests': n_requests,
            'avg_request_interval': avg_request_interval,
            'avg_serving_time': avg_serving_time,
            'max_time': max_time,
            'waiting_time': self._waiting_time, 
            'serving_time': self._serving_time,
            'entry_time': self._entry_time,
            'experiment_payload': sum(self._serving_time),
            'n_rejected': self._num_rejected,
        }
    
    def _generate_requests(self):
        for i in range(self.n_requests):
            self.env.process(self._serve())
            t = expovariate(1.0/self._avg_request_interval)
            yield self.env.timeout(t) # wait for the next request to appear      
        
    def _serve(self):
        num_rejected = 0
        arrive = self.env.now
        
        self._entry_time.append(arrive)
        
        if len(self.resource.queue) < MAX_QUEUE_LEN:
            with self.resource.request() as req:
                yield req
                wait_time = self.env.now-arrive
                self._waiting_time.append(wait_time)
                service_time = expovariate(1.0/self._avg_serving_time)
                before_service = env.now
                yield self.env.timeout(service_time) # wait to be served
                self._serving_time.append(service_time)
        else:
            num_rejected += 1
# In[4]:
results_list = []
for simulation_time in payload_balance:
    for expected_payload, params in payload_balance[simulation_time].items():
        for nr in n_requests:
            # start simulation from the scratch
            env = simpy.Environment(0)
            k = simpy.Resource(env, capacity=N_PROCESSORS)
            # add process to monitor
            m = ProcessMonitor(env, k)
            # record results
            results_list.append(m.collect_data(nr, params['a'], params['b'], simulation_time))
            results_list[-1]['expected_payload'] = expected_payload
results = pd.DataFrame(results_list)
results.head(5)
# In[5]:
# DataFrame describing payload
p = results.loc[:,['n_requests', 'max_time', 'experiment_payload', 'expected_payload']]
p.loc[:,'exp_payload_percents'] = p.loc[:,'experiment_payload']/p.loc[:,'max_time']
p.loc[:,'diff'] = p.loc[:,'expected_payload'] - p.loc[:,'experiment_payload']/p.loc[:,'max_time']
p[p['max_time']==30000].head(15)