import customtkinter as ctk  
from file_handling.file_handling import TestDistanceHandler as tdh 
from file_handling.file_handling import TeamSelectionHandler as tsh
from file_handling.file_handling import TestPIDHandler as tph
from file_handling.file_handling import ObjectDetectionModeTestHandler as odmth
import threading as th
import time
from robot.communication.json_arudino import JsonArduino
import robot.communication.serialarduino as com


class TestMenuScreen(ctk.CTkFrame):
    def __init__(self, master, main_menu_screen, det_obj,**kwargs):
        super().__init__(master, **kwargs)

        self.det_obj = det_obj

        self.master = master
        self.main_menu_screen = main_menu_screen
        
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, columnspan = 3, padx=5, pady=5, sticky="we")

        self.test_distance_frame = Test_PID(self, border_width=2)
        self.test_distance_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe") 

        self.test_distance_frame = Test_Distance(self, border_width=2)
        self.test_distance_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nswe") 

        self.display_video_frame = DisplayVideo(self, self.det_obj,border_width=2)
        self.display_video_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nswe") 

    def back(self):
        print("back click")
        self.grid_forget()
        self.main_menu_screen.grid()
        self.det_obj.set_mode(0)

class Test_PID(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title_label = ctk.CTkLabel(self, text="Test PID")
        self.title_label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="we")

        self.Kpx_label = ctk.CTkLabel(self, text="Kpx")
        self.Kpx_label.grid(row=4, column=0, padx=5, pady=5)
        self.Kpx_entry = ctk.CTkEntry(self)
        self.Kpx_entry.grid(row=4, column=1, padx=5, pady=5)

        self.Kix_label = ctk.CTkLabel(self, text="Kix")
        self.Kix_label.grid(row=5, column=0, padx=5, pady=5)
        self.Kix_entry = ctk.CTkEntry(self)
        self.Kix_entry.grid(row=5, column=1, padx=5, pady=5)

        self.Kdx_label = ctk.CTkLabel(self, text="Kdx")
        self.Kdx_label.grid(row=6, column=0, padx=5, pady=5)
        self.Kdx_entry = ctk.CTkEntry(self)
        self.Kdx_entry.grid(row=6, column=1, padx=5, pady=5)

        self.Kpy_label = ctk.CTkLabel(self, text="Kpy")
        self.Kpy_label.grid(row=7, column=0, padx=5, pady=5)
        self.Kpy_entry = ctk.CTkEntry(self)
        self.Kpy_entry.grid(row=7, column=1, padx=5, pady=5)

        self.Kiy_label = ctk.CTkLabel(self, text="Kiy")
        self.Kiy_label.grid(row=8, column=0, padx=5, pady=5)
        self.Kiy_entry = ctk.CTkEntry(self)
        self.Kiy_entry.grid(row=8, column=1, padx=5, pady=5)

        self.Kdy_label = ctk.CTkLabel(self, text="Kdy")
        self.Kdy_label.grid(row=9, column=0, padx=5, pady=5)
        self.Kdy_entry = ctk.CTkEntry(self)
        self.Kdy_entry.grid(row=9, column=1, padx=5, pady=5)

        self.Kpw_label = ctk.CTkLabel(self, text="Kpw")
        self.Kpw_label.grid(row=10, column=0, padx=5, pady=5)
        self.Kpw_entry = ctk.CTkEntry(self)
        self.Kpw_entry.grid(row=10, column=1, padx=5, pady=5)

        self.Kiw_label = ctk.CTkLabel(self, text="Kiw")
        self.Kiw_label.grid(row=11, column=0, padx=5, pady=5)
        self.Kiw_entry = ctk.CTkEntry(self)
        self.Kiw_entry.grid(row=11, column=1, padx=5, pady=5)

        self.Kdw_label = ctk.CTkLabel(self, text="Kdw")
        self.Kdw_label.grid(row=12, column=0, padx=5, pady=5)
        self.Kdw_entry = ctk.CTkEntry(self)
        self.Kdw_entry.grid(row=12, column=1, padx=5, pady=5)

        self.start_all_button = ctk.CTkButton(self, text="Set", command=self.set)
        self.start_all_button.grid(row=13, columnspan = 2, padx=5, pady=5)
        
        self.Kpx, self.Kix, self.Kdx, self.Kpy, self.Kiy, self.Kdy, self.Kpw, self.Kiw, self.Kdw = tph.readPIDTestFile(self)
        self.team = tsh.readTeamFile(self)

        self.Kpx_entry.insert(0, self.Kpx)
        self.Kix_entry.insert(0, self.Kix)
        self.Kdx_entry.insert(0, self.Kdx)
        self.Kpy_entry.insert(0, self.Kpy)
        self.Kiy_entry.insert(0, self.Kiy)
        self.Kdy_entry.insert(0, self.Kdy)
        self.Kpw_entry.insert(0, self.Kpw)
        self.Kiw_entry.insert(0, self.Kiw)
        self.Kdw_entry.insert(0, self.Kdw)

    def set(self):
        print("start click")

        if self.Kpx_entry.get() == '':
            self.Kpx_entry.insert(0, '0.1')
        if self.Kix_entry.get() == '':
            self.Kix_entry.insert(0, '0.0')
        if self.Kdx_entry.get() == '':
            self.Kdx_entry.insert(0, '0.0')
        if self.Kpy_entry.get() == '':
            self.Kpy_entry.insert(0, '0.1')
        if self.Kiy_entry.get() == '':
            self.Kiy_entry.insert(0, '0.0')
        if self.Kdy_entry.get() == '':
            self.Kdy_entry.insert(0, '0.0')
        if self.Kpw_entry.get() == '':
            self.Kpw_entry.insert(0, '0.1')
        if self.Kiw_entry.get() == '':
            self.Kiw_entry.insert(0, '0.0')
        if self.Kdw_entry.get() == '':
            self.Kdw_entry.insert(0, '0.0')

        self.Kpx = self.Kpx_entry.get()
        self.Kix = self.Kix_entry.get()
        self.Kdx = self.Kdx_entry.get()
        self.Kpy = self.Kpy_entry.get()
        self.Kiy = self.Kiy_entry.get()
        self.Kdy = self.Kdy_entry.get()
        self.Kpw = self.Kpw_entry.get()
        self.Kiw = self.Kiw_entry.get()
        self.Kdw = self.Kdw_entry.get()

        tph.savePIDTestFile(self, self.Kpx, self.Kix, self.Kdx, self.Kpy, self.Kiy, self.Kdy, self.Kpw, self.Kiw, self.Kdw)
        Kx = [self.Kpx, self.Kix, self.Kdx]
        ky = [self.Kpy, self.Kiy, self.Kdy]
        kw = [self.Kpw, self.Kiw, self.Kdw]
        JsonArduino.set_json_data("Kx", Kx)
        JsonArduino.set_json_data("Ky", ky)
        JsonArduino.set_json_data("Kw", kw)

class Test_Distance(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title_label = ctk.CTkLabel(self, text="Test Distance")
        self.title_label.grid(row=0, columnspan=3, padx=10, pady=10, sticky="we")

        self.vx_label = ctk.CTkLabel(self, text="Vx")
        self.vx_label.grid(row=4, column=0, padx=5, pady=5)
        self.vx_entry = ctk.CTkEntry(self)
        self.vx_entry.grid(row=4, column=1, padx=5, pady=5)

        self.vy_label = ctk.CTkLabel(self, text="Vy")
        self.vy_label.grid(row=5, column=0, padx=5, pady=5)
        self.vy_entry = ctk.CTkEntry(self)
        self.vy_entry.grid(row=5, column=1, padx=5, pady=5)

        self.omega_label = ctk.CTkLabel(self, text="Omega")
        self.omega_label.grid(row=6, column=0, padx=5, pady=5)
        self.omega_entry = ctk.CTkEntry(self)
        self.omega_entry.grid(row=6, column=1, padx=5, pady=5)

        self.Dis_label = ctk.CTkLabel(self, text="Distance 1")
        self.Dis_label.grid(row=7, column=0, padx=5, pady=5)
        self.Dis_entry = ctk.CTkEntry(self)
        self.Dis_entry.grid(row=7, column=1, padx=5, pady=5)

        # self.dis2_label = ctk.CTkLabel(self, text="Distance 2")
        # self.dis2_label.grid(row=8, column=0, padx=5, pady=5)
        # self.dis2_entry = ctk.CTkEntry(self)
        # self.dis2_entry.grid(row=8, column=1, padx=5, pady=5)

        # self.dis3_label = ctk.CTkLabel(self, text="Distance 3")
        # self.dis3_label.grid(row=9, column=0, padx=5, pady=5)
        # self.dis3_entry = ctk.CTkEntry(self)
        # self.dis3_entry.grid(row=9, column=1, padx=5, pady=5)

        # self.dis4_label = ctk.CTkLabel(self, text="Distance 4")
        # self.dis4_label.grid(row=10, column=0, padx=5, pady=5)
        # self.dis4_entry = ctk.CTkEntry(self)
        # self.dis4_entry.grid(row=10, column=1, padx=5, pady=5)

        self.ang_label = ctk.CTkLabel(self, text="Angle")
        self.ang_label.grid(row=8, column=0, padx=5, pady=5)
        self.ang_entry = ctk.CTkEntry(self)
        self.ang_entry.grid(row=8, column=1, padx=5, pady=5)

        self.time_label = ctk.CTkLabel(self, text="Time")
        self.time_label.grid(row=9, column=0, padx=5, pady=5)
        self.time_entry = ctk.CTkEntry(self)
        self.time_entry.grid(row=9, column=1, padx=5, pady=5)

        self.start_all_button = ctk.CTkButton(self, text="Start", command=self.start)
        self.start_all_button.grid(row=10, columnspan = 2, padx=5, pady=5)
        
        self.vx, self.vy, self.omega, self.acc, self.Dis, self.ang, self.time= tdh.readTestDistanceFile(self)
        self.team = tsh.readTeamFile(self)

        self.vx_entry.insert(0, self.vx)
        self.vy_entry.insert(0, self.vy)
        self.omega_entry.insert(0, self.omega)
        self.Dis_entry.insert(0, self.Dis)
        # self.dis2_entry.insert(0, self.dis2)
        # self.dis3_entry.insert(0, self.dis3)
        # self.dis4_entry.insert(0, self.dis4)
        self.ang_entry.insert(0, self.ang)
        self.time_entry.insert(0, self.time)


    def start(self):
        print("start click")

        if self.vx_entry.get() == '':
            self.vx_entry.insert(0, '0.0')
        if self.vy_entry.get() == '':
            self.vy_entry.insert(0, '0.0')
        if self.omega_entry.get() == '':
            self.omega_entry.insert(0, '0.0')
        if self.Dis_entry.get() == '':
            self.Dis_entry.insert(0, '0.0')
        # if self.dis2_entry.get() == '':
        #     self.dis2_entry.insert(0, '0.0')
        # if self.dis3_entry.get() == '':
        #     self.dis3_entry.insert(0, '0.0')
        # if self.dis4_entry.get() == '':
        #     self.dis4_entry.insert(0, '0.0')
        if self.ang_entry.get() == '':
            self.ang_entry.insert(0, '0.0')
        if self.time_entry.get() == '':
            self.time_entry.insert(0, '0.0')

        self.vx = float(self.vx_entry.get())
        self.vy = float(self.vy_entry.get())
        self.omega = float(self.omega_entry.get())
        self.Dis = float(self.Dis_entry.get())
        # self.dis2 = float(self.dis2_entry.get())
        # self.dis3 = float(self.dis3_entry.get())
        # self.dis4 = float(self.dis4_entry.get())
        self.ang = float(self.ang_entry.get())
        self.time = float(self.time_entry.get())
        tdh.saveTestDistanceFile(self, self.vx, self.vy, self.omega, self.acc, self.Dis, self.ang, self.time)
        
        JsonArduino.set_json_data("Start", 2)
        JsonArduino.set_json_data("Vx", self.vx)
        JsonArduino.set_json_data("Vy", self.vy)
        JsonArduino.set_json_data("Omega", self.omega)
        JsonArduino.set_json_data("Dis", self.Dis)
        JsonArduino.set_json_data("Ang", self.ang)
        JsonArduino.set_json_data("Time", self.time)
        # com.arser.write(str(JsonArduino.get_json_data()).encode())

        # time.sleep(0.25)
        # JsonArduino.set_json_data("Start", 0)
        # JsonArduino.set_json_data("Vx", 0)
        # JsonArduino.set_json_data("Vy", 0)
        # JsonArduino.set_json_data("Omega", 0)
        # JsonArduino.set_json_data("Dis", 0)
        # JsonArduino.set_json_data("Ang", 0)
        # JsonArduino.set_json_data("Time", 0)
        # com.arser.write(str(JsonArduino.get_json_data()).encode())



class DisplayVideo(ctk.CTkFrame):
    def __init__(self, master, det_obj,**kwargs):
        super().__init__(master, **kwargs)

        self.det_obj = det_obj
        self.label_title = ctk.CTkLabel(self, text="Test Detection")
        self.label_title.grid(row=0, column=0, padx=10, pady=10)

        # self.launch_detection_button = ctk.CTkButton(self, text="Launch Camera", command=self.launch_camera)
        # self.launch_detection_button.grid(row=1, column=0, padx=10, pady=10)


        self.collect_ball_button = ctk.CTkButton(self, text="Collect Ball", command=self.collect_ball)
        self.collect_ball_button.grid(row=1, column=0, padx=10, pady=10)

        self.check_opp_ball_button = ctk.CTkButton(self, text="Check Opp Ball", command=self.check_opp_ball)
        self.check_opp_ball_button.grid(row=2, column=0, padx=10, pady=10)

        self.detect_silo_button = ctk.CTkButton(self, text="Detect Silo", command=self.detect_silo)
        self.detect_silo_button.grid(row=3, column=0, padx=10, pady=10)

        self.run_detection_thread = None

        self.detectionMode = odmth.saveObjectDetectionModeTestFile(self, 0)

        # self.det_obj = ObjectDetection()

    # def launch_camera(self): 
    #     self.launch_detection_button.configure(text="Close Detection", command=self.close_camera)
    #     self.stop_detection = False
    #     self.run_detection_thread = th.Thread(target=self.run_detection, daemon=True)
    #     self.run_detection_thread.start()
        
    # def run_detection(self):
    #     self.det_obj = ObjectDetection()
    #     self.det_obj.start_camera() 
    
    # def close_camera(self):
    #     self.launch_detection_button.configure(text="Launch Camera", command=self.launch_camera)
    #     self.stop_detection = True
    #     self.det_obj.stop_camera()
    #     self.run_detection_thread.join(1)
    
    def collect_ball(self):
        self.det_obj.set_mode(1)

    def check_opp_ball(self):
        self.det_obj.set_mode(2)
    
    def detect_silo(self):
        self.det_obj.set_mode(3)