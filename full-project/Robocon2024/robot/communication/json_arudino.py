import json
import os
import time

class JsonArduino:

    if os.path.exists("json_data.json"):
        with open("json_data.json", "r") as file:
            data = json.load(file)
            print(data)
    else:
        data = {
                    "Team": 0,
                    "Start": 0,
                    "Retry": 0,
                    #For Distance
                    "Vx": 0,
                    "Vy": 0,
                    "Omega": 0,
                    "Dis": 0,
                    "Ang": 0,
                    "Time": 0,
                    #For Detection
                    "DetectionMode": 0,
                    "Depth": 0,
                    "Pixel": [0,0],
                    # For Position Camera
                    "Angular_velocity": [0,0,0],
                    "Velocity": [0,0,0],  
                    # PID
                    "Kx": [0.1,0,0],
                    "Ky": [0.1,0,0],
                    "Kw": [0.1,0,0],              
                }
        
    def __init__(self):
        pass
    
    @classmethod
    def set_json_data(cls, key, value):
        cls.data[key] = value
        # cls.file.write(cls.data,)
        return cls.data

    @classmethod
    def get_json_data(cls):
        return cls.data

    @classmethod
    def display_json_data(cls):
        print(cls.data)



