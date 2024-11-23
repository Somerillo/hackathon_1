# this is a mock health tracker like a smartwatch, will generate random data to fill health record everytime its called
# this data is very random, we could get a very low BP value during an extreme exercise time... anyway, mock data
# in other words we have codependent variables, that will be treated as independent

import random


class MockTracker:
    """
    generates (very, extremely) random health data in human range values for the time interval given (default is 60 seconds)
    """

    def __init__(self, time_interval=60):
        """
        the upper and lower limits for each method should be here in __init__ but im not a dev and this way is more comfortable for me :)
        """
        self.interv = time_interval

    def get_random_steps(self):
        """
        generates a steps range in the time interval
        """
        # slow 1 hour walk 3000 - 4000 steps, fast 1 hour walk 6000 - 10000 steps
        # dividing on an hour (3600) and multiplying by the time interval we get the steps in that time
        steps_interv = random.randint(3000, 10000) / 3600 * self.interv
        return int(steps_interv)

    def get_random_heart_rate(self):
        """
        measures heart rate in bpm, i.e. *independently* of the time interval
        """
        # normal, healthy, average human heart rate 60 bpm at rest and 170 bpm in intense exercise
        return random.randint(60, 170)

    def get_random_blood_pressure_sys(self):
        '''
        generates random systolic BP value
        '''
        # normal, healthy, average human systolic BP can go from 90 mmHg at rest to 200 mmHg in extreme exercise
        return random.randint(90, 200)

    def get_random_blood_pressure_dia(self):
        '''
        generates random diastolic BP value
        '''
        # this data is harder to get for extreme exercise
        return random.randint(60, 90)

    def get_random_oxygen(self):
        '''
        generates random O2% value
        '''
        return random.randint(95, 100)

    def get_all_data(self):
        """
        builds a dictionary to catch em all
        """
        return {
            'steps': self.get_random_steps(),
            'heart_rate': self.get_random_heart_rate(),
            'blood_pressure_sys': self.get_random_blood_pressure_sys(),
            'blood_pressure_dia': self.get_random_blood_pressure_dia(),
            'oxygen': self.get_random_oxygen()
        }


## --------------------------------------------  testing  -------------------------------------------- ##
# print(MockTracker().get_all_data())
# print(MockTracker(30).get_all_data())
