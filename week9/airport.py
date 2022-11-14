'''
In this problem you, can simulate a simplified airport security system at a busy airport. Passengers arrive
according to a Poisson distribution with λ1 = 5 per minute (i.e., mean interarrival rate 1 = 0.2 minutes)
to the ID/boarding-pass check queue, where there are several servers who each have exponential
service time with mean rate 2 = 0.75 minutes. [Hint: model them as one block that has more than one
resource.] After that, the passengers are assigned to the shortest of the several personal-check queues,
where they go through the personal scanner (time is uniformly distributed between 0.5 minutes and 1
minute).
Use the Arena software (PC users) or Python with SimPy (PC or Mac users) to build a simulation of the
system, and then vary the number of ID/boarding-pass checkers and personal-check queues to
determine how many are needed to keep average wait times below 15 minutes. [If you’re using SimPy,
or if you have access to a non-student version of Arena, you can use λ1 = 50 to simulate a busier airport.]

'''
import random
import numpy as np
import simpy
import pandas as pd
from multiprocessing import Pool

RANDOM_SEED = 42
ARRIVAL_RATE = 0.02  # 50 passengers arrive / minute
ID_CHECK_RATE = 0.75  # mean time to check ID is 45 seconds
SIM_TIME = 480  # simulate for 8 hours
passengers = {}


def generate_poisson_distribution(lam):
    """Generate a poisson distribution given lambda."""
    return np.random.poisson(lam=lam)


def generate_scanner_time():
    """Generate uniformly distributed scanner time, from 0.5 to 1 min."""
    return np.random.uniform(low=0.5, high=1.0, size=None)


random.seed(RANDOM_SEED)
class AirportSecuritySystem(object):
    def __init__(self, env, num_id_checkers, num_personal_check_queues,
                 id_check_rate):
        """Initialize the airport.
        Set properties for the following:
        - Number of ID checkers
        - Number of personal check queues
        - The ID check rate lambda.
        """
        self.env = env
        self.id_checkers = simpy.Resource(env, num_id_checkers)
        self.personal_check_queues = simpy.Resource(env,
                                                    num_personal_check_queues)
        self.id_check_rate = id_check_rate
        
    def check_id(self, passenger):
    """Send passenger through ID check."""
    id_check_time = generate_poisson_distribution(ID_CHECK_RATE)
    yield self.env.timeout(id_check_time)
    print("Checked %s's ID. It took %d minutes" %
    (passenger, id_check_time))

    def personal_check(self, passenger):
        """Send passenger through personal check."""
        scanner_time = generate_scanner_time()
        yield self.env.timeout(generate_scanner_time())
        print("%s has gone through the scanner, it took %d minutes" %
                (passenger, scanner_time))
              
# Create environment and start processes
env = simpy.Environment()
gas_station = simpy.Resource(env, 2)
fuel_pump = simpy.Container(env, GAS_STATION_SIZE, init=GAS_STATION_SIZE)
env.process(gas_station_control(env, fuel_pump))
env.process(car_generator(env, gas_station, fuel_pump))

# Execute!
env.run(until=SIM_TIME)