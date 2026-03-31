import robot.communication.serialarduino as com
from robot.communication.json_arudino import JsonArduino
import numpy as np 
import json
from ultralytics import YOLO
import cv2 as cv
from application.screen.main_menu1 import *
from file_handling.file_handling import TeamSelectionHandler as tsh
from file_handling.file_handling import ObjectDetectionModeTestHandler as odmth
import time
from robot.ai.ai_mode import AI

class ObjectDetection:
    def __init__(self):
        self.model = YOLO("./models/best.pt")
        self.team = tsh.readTeamFile(self)
        self.team_ball = ""
        self.opp_ball = ""
        self.team_color = (0,0,0) 
        self.opp_color = (0,0,0)

        self.ball_collected = False

        if self.team == "1":
            self.team_ball = "Red ball"
            self.opp_ball = "Blue ball"
            self.team_color = (0, 0, 255)
            self.opp_color = (255, 0, 0)
        elif self.team == "2":
            self.team_ball = "Blue ball"
            self.opp_ball = "Red ball"
            self.team_color = (255, 0, 0)
            self.opp_color = (0, 0, 255)

        self.stop = False
        self.mode = 0
        self.first = True

        self.silo = np.zeros((3, 5))
        self.detectedSilo = np.zeros((3, 5))
    
    def start_camera(self, cam):
        self.stop = False
        while True:
            ret, depth_frame, color_frame = cam.get_frame()
            # self.mode = odmth.readObjectDetectionModeTestFile(self)
            if not ret:
                continue

            # self.collect_ball(depth_frame, color_frame)
            # print(self.mode)
            if self.first:
                self.collect_ball(depth_frame, color_frame)
                self.first = False

            if self.mode == 1:
                self.collect_ball(depth_frame, color_frame)
            elif self.mode == 2:
                self.check_opp_reserve_ball(depth_frame, color_frame)
            elif self.mode == 3:
                self.detect_silo(depth_frame, color_frame)
            else:
                JsonArduino.set_json_data("Depth", 0)
                JsonArduino.set_json_data("Pixel", [0, 0])

            cv.imshow('Testing Screen', color_frame)
            cv.waitKey(1) 
            if self.stop == True:
                break

        cam.close()
        cv.destroyAllWindows()


    def stop_camera(self):
        print("stop camera")
        self.stop = True

    def set_mode(self, mode):
        self.mode = mode
        # self.mode = odmth.saveObjectDetectionModeTestFile(self, mode)

    def update_team(self):
        self.team = tsh.readTeamFile(self)
        self.team_ball = ""
        self.opp_ball = ""
        self.team_color = (0,0,0) 
        self.opp_color = (0,0,0)

        self.ball_collected = False

        if self.team == "1":
            self.team_ball = "Red ball"
            self.opp_ball = "Blue ball"
            self.team_color = (0, 0, 255)
            self.opp_color = (255, 0, 0)
        elif self.team == "2":
            self.team_ball = "Blue ball"
            self.opp_ball = "Red ball"
            self.team_color = (255, 0, 0)
            self.opp_color = (0, 0, 255)

    def collect_ball(self, depth_frame, color_frame):
        results = self.model.track(source=color_frame, verbose=False) 
        min_distance = 900000
        min_position = (0, 0)
        _x1,_x2,_y1,_y2 = 0,0,0,0
        for r in results:
            try:
                if len(r.boxes.cls) == 0:
                    continue
                for i in range(len(r.boxes.cls)):
                    
                    class_label = r.names[r.boxes.cls[i].item()]
                    
                    if class_label != self.team_ball:
                        continue
                    else:
                        x1, y1, x2, y2 = map(int, r.boxes.xyxy[i])
                        coreX = (x1 + x2) // 2
                        coreY = (y1 + y2) // 2

                        radius = max((x2 - x1) // 2, (y2 - y1) // 2)
                        
                        depth = depth_frame[coreY, coreX]
                        if(depth < min_distance):
                            min_distance = depth
                            min_position = (coreX, coreY)
                            _x1,_x2,_y1,_y2 = x1,x2,y1,y2
                        
            except IndexError:
                continue

            # if min_distance == 0:
            #     self.mode = 0
            #     JsonArduino.set_json_data("Depth", 0)
            #     JsonArduino.set_json_data("Pixel", [0, 0])
            #     JsonArduino.set_json_data("DetectionMode", self.mode)
            #     com.arser.write(str(JsonArduino.get_json_data()).encode())
                # break
            
            if min_distance != 900000:
                coreX, coreY = min_position
                radius = max((_x2 - _x1) // 2, (_y2 - _y1) // 2)

                cv.circle(color_frame, (coreX, coreY), radius, self.team_color, 2)
                cv.putText(color_frame, f"{self.team_ball}: {depth:.2f} mm", (coreX, coreY), cv.FONT_HERSHEY_SIMPLEX, 1, self.team_color, 2, cv.LINE_AA)
                self.ball_collected = True

                JsonArduino.set_json_data("Depth", depth)
                JsonArduino.set_json_data("Pixel", [coreX, coreY])
                JsonArduino.set_json_data("DetectionMode", self.mode)
            

    def check_opp_reserve_ball(self,depth_frame, color_frame):

        results = self.model.track(source=color_frame, verbose=False) 
        counted = False
        opp_reserve_balls_distances = []
        opp_reserve_balls_positions = []
        _x1 = _x2 =_y1 = _y2 = []
        for r in results:
            # print(r.names)
            try:
                #0 = blue, 1 = purple, 2 = red, else = silo
                # print(r.boxes.cls)
                if len(r.boxes.cls) == 0:
                    continue
                for i in range(len(r.boxes.cls)):
                    
                    class_label = r.names[r.boxes.cls[i].item()]
                    
                    if class_label != self.opp_ball:
                        continue
                    else:
                        x1, y1, x2, y2 = map(int, r.boxes.xyxy[i])
                        coreX = (x1 + x2) // 2
                        coreY = (y1 + y2) // 2

                        radius = max((x2 - x1) // 2, (y2 - y1) // 2)
                        
                        depth = depth_frame[coreY, coreX]

                        if depth < 6000:
                            opp_reserve_balls_distances.append(depth)
                            opp_reserve_balls_positions.append((coreX, coreY))
                            _x1.append(x1)
                            _x2.append(x2)
                            _y1.append(y1)
                            _y2.append(y2)
                            cv.circle(color_frame, (coreX, coreY), radius, self.opp_color, 2)
                            cv.putText(color_frame, f"{self.opp_ball}: {depth:.2f} mm", (coreX, coreY), cv.FONT_HERSHEY_SIMPLEX, 1, self.opp_color, 2, cv.LINE_AA)
            except IndexError:
                continue
            
            print(len(opp_reserve_balls_distances))
            # for i in range(len(opp_reserve_balls_distances)):
            #     coreX, coreY = opp_reserve_balls_positions[i]
            #     radius = max((_x2[i] - _x1[i]) // 2, (_y2[i] - _y1[i]) // 2)
            #     print(len(opp_reserve_balls_distances))
            #     cv.circle(color_frame, (coreX, coreY), radius, self.opp_color, 2)
            #     cv.putText(color_frame, f"{self.opp_ball}: {opp_reserve_balls_distances[i]:.2f} mm", (coreX, coreY), cv.FONT_HERSHEY_SIMPLEX, 1, self.opp_color, 2, cv.LINE_AA)
        
    def detect_silo(self,depth_frame, color_frame):
        results = self.model.track(source=color_frame, verbose=False, conf=0.5) 
        silo_distances = []
        silo_positions = []
        for r in results:
            # print(r.names)
            try:
                count = 0
                #0 = blue, 1 = purple, 2 = red, else = silo
                # print(r.boxes.cls)
                if len(r.boxes.cls) == 0:
                    continue
                for i in range(len(r.boxes.cls)):
                    class_label = r.names[r.boxes.cls[i].item()]
                    if class_label == 'Blue ball' or class_label == 'Purple ball' or class_label == 'Red ball':
                        continue
                    else:
                        index = 0
                        x1, y1, x2, y2 = map(int, r.boxes.xyxy[i])
                        mid_x_silo = (x1 + x2) // 2
                        mid_y_silo = (y1 + y2) // 2

                        text_pos = (y1 + y2) // 4
                        depth = depth_frame[mid_y_silo, mid_x_silo]
                        silo_distances.append(depth)
                        silo_positions.append((mid_x_silo, mid_y_silo))
                        
                        if mid_x_silo >= 27 and mid_x_silo <= 88:
                            index = 0
                        elif mid_x_silo >= 171 and mid_x_silo <= 224:
                            index = 1
                        elif mid_x_silo >= 299 and mid_x_silo <= 346:
                            index = 2
                        elif mid_x_silo >= 427 and mid_x_silo <= 482:
                            index = 3
                        elif mid_x_silo >= 556 and mid_x_silo <= 618:
                            index = 4
                        else:
                            index = -1

                        if index != -1:
                            if class_label == 'Silo':
                                for row in range(0,3):
                                    self.silo[row][index] = 0
                            elif class_label == 'SB':
                                self.silo[0][index] = 2
                                self.silo[1][index] = 0
                                self.silo[2][index] = 0
                            elif class_label == 'B-R':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 2
                                self.silo[2][index] = 0
                            elif class_label == 'SBB':
                                self.silo[0][index] = 2
                                self.silo[1][index] = 2
                                self.silo[2][index] = 0
                            elif class_label == 'SBBB':
                                self.silo[0][index] = 2
                                self.silo[1][index] = 2
                                self.silo[2][index] = 2
                            elif class_label == 'SBBR':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 2
                                self.silo[2][index] = 2
                            elif class_label == 'SBRB':
                                self.silo[0][index] = 2
                                self.silo[1][index] = 1
                                self.silo[2][index] = 2
                            elif class_label == 'SBRR':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 1
                                self.silo[2][index] = 2
                            elif class_label == 'SR':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 0
                                self.silo[2][index] = 0
                            elif class_label == 'SRBB':
                                self.silo[0][index] = 2
                                self.silo[1][index] = 2
                                self.silo[2][index] = 1
                            elif class_label == 'SRBR':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 2
                                self.silo[2][index] = 1
                            elif class_label == 'SRR':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 1
                                self.silo[2][index] = 0
                            elif class_label == 'SRRB':
                                self.silo[0][index] = 2
                                self.silo[1][index] = 1
                                self.silo[2][index] = 1
                            elif class_label == 'SRRR':
                                self.silo[0][index] = 1
                                self.silo[1][index] = 1
                                self.silo[2][index] = 1
                                
                                
                        cv.rectangle(color_frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                        cv.putText(color_frame, f"Index: {index}", (x1, text_pos - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)
                        cv.putText(color_frame, f"Pos: {mid_x_silo}, {mid_y_silo}", (x1, text_pos + 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)
                        cv.putText(color_frame, f"Type: {class_label}", (x1, text_pos + 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)
                        count += 1
                    
            except IndexError:
                continue
            

            AI(self.silo)
            if silo_distances:
                silo_distances.clear()
                silo_positions.clear()
            # for i in range(len(opp_reserve_balls_distances)):
            #     coreX, coreY = opp_reserve_balls_positions[i]
            #     radius = max((_x2[i] - _x1[i]) // 2, (_y2[i] - _y1[i]) // 2)
            #     print(len(opp_reserve_balls_distances))
            #     cv.circle(color_frame, (coreX, coreY), radius, self.opp_color, 2)
            #     cv.putText(color_frame, f"{self.opp_ball}: {opp_reserve_balls_distances[i]:.2f} mm", (coreX, coreY), cv.FONT_HERSHEY_SIMPLEX, 1, self.opp_color, 2, cv.LINE_AA)