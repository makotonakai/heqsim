from .Processor import PhysicalProcessor
import configparser
import sys
import os

class QCluster:
    def __init__(self):
        self.n = 0
        self.ProcessorList = []
        self.setup()

    def setup(self):
        path = os.path.dirname(os.path.realpath(__file__))
        configdir = '/'.join([path,'config.ini'])
        config = configparser.ConfigParser()
        config.read(configdir, encoding="utf-8")
        print(config.sections())
        for DeviceName in config.sections():
            NewProcessor = PhysicalProcessor()
            NewProcessor.QubitNumber = int(config[DeviceName]["QubitNumber"])
            NewProcessor.OneQubitGateTime = float(config[DeviceName]["OneQubitGateTime"])
            NewProcessor.TwoQubitGateTime = float(config[DeviceName]["TwoQubitGateTime"])
            self.ProcessorList.append(NewProcessor) 
