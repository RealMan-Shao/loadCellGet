from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time

#Insert your gain value from the Phidget Control Panel
gain = 2e8

#The offset is calculated in tareScale
offset = 0

calibrated = False

def onVoltageRatioChange(self, voltageRatio):
    if(calibrated):
        #Apply the calibration parameters (gain, offset) to the raw voltage ratio
        weight = (voltageRatio - offset) * gain        
        print("Weight(Kg): " + str(weight))
    

def tareScale(ch):    
    global offset, calibrated
    num_samples = 16

    for i in range(num_samples):
        offset += ch.getVoltageRatio()
        time.sleep(ch.getDataInterval()/1000.0)
        
    offset /= num_samples
    calibrated = True    
    
def main():
    voltageRatioInput0 = VoltageRatioInput()
    voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
    voltageRatioInput0.openWaitForAttachment(5000)
    
    #Set the data interval for the application
    voltageRatioInput0.setDataInterval(100)
    
    print("Taring")
    time.sleep(1)
    tareScale(voltageRatioInput0)
    
    print("Taring Complete")
        
    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    voltageRatioInput0.close()

main()