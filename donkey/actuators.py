# Simple car movement using the PCA9685 PWM servo/LED controller library.
# 
# Attribution: hacked from sample code from Tony DiCola

import time
import sys

# Import the PCA9685 module.



# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)


def map_range(x, X_min, X_max, Y_min, Y_max):
    X_range = X_max - X_min
    Y_range = Y_max - Y_min
    XY_ratio = X_range/Y_range

    y = ((x-X_min) / XY_ratio + Y_min) // 1

    return int(y)


class BaseMixer():

    def update_angle(self, angle):
        print('BaseSteeringActuator.update: angle=%s' %angle)

    def update_throttle(self, throttle):
        print('BaseThrottleActuator.update: throttle=%s' %throttle)

    def update(self, angle=0, throttle=0):
        '''Convenience function to update
        angle and throttle at the same time'''
        self.update_angle(angle)
        self.update_throttle(throttle)


class FrontSteeringMixer(BaseActuatorMixer):

    def __init__(self, 
                 steering_actuator=None, 
                 throttle_actuator=None)
        self.steering_actuator = steering_actuator
        self.throttle_actuator = throttle_actuator

    def update_angle(self, angle):
        self.steering_actuator.update_angle(angle)

    def update_throttle(self, throttle):
        self.throttle_actuator.update_throttle(throttle)


class DifferentialSteeringMixer(BaseActuatorMixer):

    def __init__(self, 
                 left_actuator=None, 
                 right_actuator=None,
                 angle_throttle_multiplier = 1.0)
        self.left_actuator = left_actuator
        self.right_actuator = right_actuator
        self.angle = 0
        self.throttle = 0
        self.angle_throttle_multiplier = angle_throttle_multiplier

    def update_angle(self, angle):
        self.angle = angle
        self.update_actuators()

    def update_throttle(self, throttle):
        self.throttle = throttle
        self.update_actuators()

    def update_actuators(self):
        self.left_actuator.update(self.throttle - self.angle * angle_throttle_multiplier)
        self.right_actuator.update(self.throttle + self.angle * angle_throttle_multiplier)


class Adafruit_PCA9685_Actuator():

    def __init__(self, channel, frequency=60):
        import Adafruit_PCA9685
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()

        # Set frequency to 60hz, good for servos.
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel


class PWMSteeringActuator(Adafruit_PCA9685_Actuator):

    #max angle wheels can turn
    LEFT_ANGLE = -45 
    RIGHT_ANGLE = 45

    def __init__(self, channel=1, 
                       frequency=60,
                       left_pulse=290,
                       right_pulse=490):

        super().__init__(channel, frequency)
        self.left_pulse = left_pulse
        self.right_pulse = right_pulse

    def update(self, angle):
        #map absolute angle to angle that vehicle can implement.
        pulse = map_range(angle, 
                          self.LEFT_ANGLE, self.RIGHT_ANGLE,
                          self.left_pulse, self.right_pulse)

        self.pwm.set_pwm(self.channel, 0, pulse)


class PWMThrottleActuator(Adafruit_PCA9685_Actuator):

    MIN_THROTTLE = -100
    MAX_THROTTLE =  100

    def __init__(self, channel=0, 
                       frequency=60,
                       max_pulse=300,
                       min_pulse=490,
                       zero_pulse=350):

        super().__init__(channel, frequency)
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.zero_pulse = zero_pulse
        self.calibrate()


    def calibrate(self):
        #Calibrate ESC (TODO: THIS DOES NOT WORK YET)
        print('center: %s' % self.zero_pulse)
        self.pwm.set_pwm(self.channel, 0, self.zero_pulse)  #Set Max Throttle
        time.sleep(1)


    def update(self, throttle):
        print('throttle update: %s' %throttle)
        if throttle > 0:
            pulse = map_range(throttle,
                              0, self.MAX_THROTTLE, 
                              self.zero_pulse, self.max_pulse)
        else:
            pulse = map_range(throttle,
                              self.MIN_THROTTLE, 0, 
                              self.min_pulse, self.zero_pulse)

        print('pulse: %s' % pulse)
        sys.stdout.flush()
        self.pwm.set_pwm(self.channel, 0, pulse)
        return '123'














