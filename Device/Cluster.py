import configparser
import sys
import os
from Device.Processor import Processor

class Cluster:
    def __init__(self):
        self.n = 0
        self.ProcessorList = []
        self.setup()

    def setup(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        for DeviceName in config.sections():
            NewProcessor = Processor()
            NewProcessor.QubitNumber = int(config[DeviceName]["QubitNumber"])
            NewProcessor.OneQubitGateTime = float(config[DeviceName]["OneQubitGateTime"])
            NewProcessor.TwoQubitGateTime = float(config[DeviceName]["TwoQubitGateTime"])
            self.ProcessorList.append(NewProcessor) 

if __name__ == "__main__":

    print(sys.path)