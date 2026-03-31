import serial
import re
import time
from robot.communication.json_arudino import JsonArduino
from robot.detection.services.object_detection import ObjectDetection

arser = serial.Serial()
arser.port = '/dev/ttyUSB0'
arser.baudrate = 115200
arser.timeout = 0.1
arser.write_timeout = 0.1
arser.setDTR(True)
arser.open()

arrx = bytes(0)

def ar_read_from_port(ss):
    while True:
        time.sleep(0.2)
        arser.write(str(JsonArduino.get_json_data()).encode())
        while ss.in_waiting > 0:
            global arrx
            arrx = ss.read(500)
            ss.flushInput()
            txt = str(arrx, 'utf-8')
            print(txt)

            if(compare_strings(txt, "Ball Found")):
                JsonArduino.set_json_data("DetectionMode", 0)
                ObjectDetection.set_mode(0)

            if(compare_strings(txt, "Test Run Started")):        
                JsonArduino.set_json_data("Start", 0)
                JsonArduino.set_json_data("Vx", 0)
                JsonArduino.set_json_data("Vy", 0)
                JsonArduino.set_json_data("Omega", 0)
                JsonArduino.set_json_data("Dis", 0)
                JsonArduino.set_json_data("Ang", 0)
                JsonArduino.set_json_data("Time", 0)
            
def compare_strings(string1, string2):
    pattern = re.compile(string2)
    match = re.search(pattern, string1)
    if match:
        return True
    # else:
    #     print(f"'{string2}' not found in '{string1}'")

            
