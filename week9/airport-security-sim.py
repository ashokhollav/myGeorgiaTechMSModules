import random
import numpy as np
import simpy
import pandas as pd

RANDOM_SEED = 42
ARRIVAL_RATE = 0.02  # 50 passengers arrive / minute
ID_CHECK_RATE = 0.75  # mean time to check ID is 45 seconds
SIM_TIME = 600  # simulate for 10 hours
passengers = {}

class AirportSecurity(object):
   

    def __init__(self, env, num_id_checkers, num_personal_check_queues,
                 id_check_rate):
        """Initialize the airport.
        - Number of ID checkers
        - Number of personal check queues
        - The ID check rate lambda.
        """
        self.env = env
        self.id_checkers = simpy.Resource(env, num_id_checkers)
        self.personal_check_queues = simpy.Resource(env,
                                                    num_personal_check_queues)
        self.id_check_rate = id_check_rate

#Check ID for each passenger, at a id check rate of 0.75, mean check rate is 45 sec
    def check_id(self, passenger):
        id_check_time = np.random.poisson(self.id_check_rate)
        yield self.env.timeout(id_check_time)
        print("Checked %s's ID. It took %d minutes" %
              (passenger, id_check_time))

#Personal check for each passenger time is uniformly distributed between 0.5 minutes and 1 minute

    def personal_check(self, passenger):
        
        scanner_time = np.random.uniform(low=0.5, high=1.0, size=None)
        yield self.env.timeout(scanner_time)
        print("%s has gone through the scanner, it took %d minutes" %
              (passenger, scanner_time))

#The passenger function simulates arrival, id check ,personal check and leaving of security

def passenger(env, name, airport_security, passengers):
    
    print('%s arrives at airport security at %.2f.' % (name, env.now))
    passengers[name][0] = float(env.now)
    with airport_security.id_checkers.request() as request:
        yield request
        print('%s enters the id check at %.2f.' % (name, env.now))
        yield env.process(airport_security.check_id(name))
        print('%s leaves the id check at %.2f.' % (name, env.now))

    with airport_security.personal_check_queues.request() as request:
        print('%s enters the personal check at %.2f.' % (name, env.now))
        yield env.process(airport_security.personal_check(name))
        print('%s leaves personal check at %.2f.' % (name, env.now))

    print('%s leaves security at %.2f.' % (name, env.now))
    passengers[name][1] = float(env.now)
    passengers[name][2] = passengers[name][1] - passengers[name][0]


def setup(env, num_id_checkers, num_personal_check_queues,
          arrival_rate, id_check_rate):
    """Set up passengers in airport security system."""
    airport_security = AirportSecurity(env, num_id_checkers,
                                             num_personal_check_queues,
                                             id_check_rate)
    i = 0
    while True:
        yield env.timeout(np.random.poisson(ARRIVAL_RATE))
        i += 1
        passengers['Passenger ' + str(i)] = [0, 0, 0]
        env.process(passenger(env, 'Passenger %d' % i,
                              airport_security, passengers))

 


if __name__ == '__main__':
    
    num_id_checkers = 15
    num_personal_check_queues = 40
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    env.process(setup(env, num_id_checkers, num_personal_check_queues,
                      ARRIVAL_RATE, ID_CHECK_RATE))
    env.run(until=SIM_TIME)
    
    