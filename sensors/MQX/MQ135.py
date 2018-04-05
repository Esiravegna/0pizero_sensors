
from __future__ import division
import time
import math
from utils.log import log
log = log.name(__name__)

class MQ135(object):

    ######################### Hardware Related Macros #########################
    RL_VALUE                     = 10       # define the load resistance on the board, in kilo ohms
    

    gas_values = {
    
    'AIR': {
        'R0': 1
    },
    'CO': {
        'R0': 10.13,
        'SCALE_FACTOR': 662.9382,
        'EXPONENT': 4.0241,
        'ATM': 1
    },
    'CO2': {
        'R0': 79.97,
        'SCALE_FACTOR': 116.6020682,
        'EXPONENT': 2.769034857,
        'ATM': 407.57
    },
    'ETHANOL': {
        'R0': 34.91,
        'SCALE_FACTOR': 75.3103,
        'EXPONENT': 3.1459,
        'ATM': 22.5
    },
    'NH4': {        
        'R0': 23.49,
        'SCALE_FACTOR': 102.694,
        'EXPONENT':2.48818,
        'ATM': 15
    },
    'TOLUENE': {
        'R0': 23.06,
        'SCALE_FACTOR': 43.7748,
        'EXPONENT': 3.42936,
        'ATM': 2.9
    },
    'ACETONE': {
        'R0': 41.00,
        'SCALE_FACTOR':  33.1197,
        'EXPONENT': 3.36587,
        'ATM': 16
        },
    } 

    #  Parameters to model temperature and humidity dependence
    CORA                       = 0.00035
    CORB                       = 0.02718
    CORC                       = 1.39538
    CORD                       = 0.0018


    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interal(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define how many samples you are going to take in normal operation
    READ_SAMPLE_TIMES            = 200      # define the time interal(in milisecond) between each samples in 
                                            # normal operation
    ######################### Application Related Macros ######################
    GAS_LPG                      = 0
    GAS_CO                       = 1
    GAS_SMOKE                    = 2

    def __init__(self, ArduinoSensor, Ro=10):
        """
        Creates the sensor. The ArduinoSensor is a proper, initialized ArduinoGasSensor
        """
        log.info("Initializing sensor")
        self.Ro = Ro
        self.sensor = ArduinoSensor
        
 
        log.debug("Calibrating...")
        self.Ro = self.MQCalibration(self.sensor)
        log.debug("Calibration is done...\n")
        log.debug("Ro=%f kohm" % self.Ro)
    
    
    def MQPercentage(self, temperature=None, humidity=None):
        val = {}
        resistance = self.MQRead()
        gas_list = self.gas_values.keys()
        gas_list.remove('AIR')
        for a_gas in gas_list:
            result = 'N/A'
            if(temperature and humidity):
                result = self.getCalibratedGasPPM(temperature, humidity, resistance, a_gas)
            else:
                result = self.getGasPPM(resistance, a_gas)
            val[a_gas] = result
        return val

    def MQResistanceCalculation(self, raw_adc):
        return float((1023. * self.RL_VALUE * 5.)/(float(raw_adc) * 5.)) - self.RL_VALUE;
        #return float(self.RL_VALUE*(1023.0-raw_adc)/float(raw_adc));

    def MQCalibration(self, mq_pin):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):          # take multiple samples
            self.sensor.update()
            val += self.MQResistanceCalculation(self.sensor.MQ135Value)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
        val = val/self.CALIBARAION_SAMPLE_TIMES                 # calculate the average value
        val = val/self.gas_values['AIR']['R0']                   # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
        return val;

    def MQRead(self):
        rs = 0.0
        for i in range(self.READ_SAMPLE_TIMES):
            self.sensor.update()
            rs += self.MQResistanceCalculation(self.sensor.MQ135Value)
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)
        rs = rs/self.READ_SAMPLE_TIMES
        return rs

     
    def getGasPPM(self, resistance, GAS):
        """
        Given a valid GAS strong and a resistance value res, returns the concentration in PPM
        """
        return self.gas_values[GAS]['SCALE_FACTOR'] * pow((resistance/self.gas_values[GAS]['R0']), -self.gas_values[GAS]['EXPONENT'])

    def GetRZero(self, GAS, resistance):
        """
        Given a gas, returns the zero level
        """
        return resistance * pow((self.gas_values[GAS]['ATM']/self.gas_values[GAS]['SCALE_FACTOR']), (1./self.gas_values[GAS]['EXPONENT']));

    def getCorrectedRZero(self, GAS, resistance):
        """
        Returns the corrected R value for the given gas
        """
        return resistance * pow((self.gas_values[GAS]['ATM']/self.gas_values[GAS]['SCALE_FACTOR']), (1./self.gas_values[GAS]['EXPONENT']))

    def getCorrectionFactor(self, temperature, humidity):
        return self.CORA * temperature * temperature - self.CORB * temperature + self.CORC - (humidity-33.)*self.CORD

    def getCorrectedResistance(self, resistance, temperature, humidity):
        return float(resistance/self.getCorrectedResistance(temperature, humidity))

    def getCalibratedGasPPM(self, temperature, humidity, resistance, GAS):
        return selg.gas_values[GAS]['SCALE_FACTOR'] * pow((self.getCorrectedResistance(resistance, temperature, humidity) / 
            self.getCorrectedRZero(GAS , self.getCorrectedResistance(temperature, humidity))), -selg.gas_values[GAS]['EXPONENT'])




