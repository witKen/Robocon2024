# import customtkinter as ctk
# import time
# import robot.communication.serialarduino as com
# from robot.communication.json_arudino import JsonArduino
# from robot.detection.services.object_detection import ObjectDetection
# import threading as th

# # pos_cam = PositionCamera()
# ########################################################################################################################################################
# class StatusFrame(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#         th.Thread(target=com.ar_read_from_port, args=(com.arser,)).start()
#         th.Thread(target=self.set_detection_json).start()
#         time.sleep(3)
#         self.setting_frame = Robot_Configuration(self, border_width=2)
#         self.setting_frame.grid(row=0, column=0, padx=10, pady=10) 

#         self.robot_controller = RobotController(self, border_width=2)
#         self.robot_controller.grid(row=0, column=1, padx=10, pady=10)

#         # self.pos_plot = Detection(self, border_width=2, width=300)
#         # self.pos_plot.grid(row=0, column=2, padx=10, pady=10)

#         self.robot_pid = PIDRobot(self, border_width=2, width=300)
#         self.robot_pid.grid(row=0, column=3, padx=10, pady=10)

#         # self.path_planing = PathPlaning(self)
#         # self.path_planing.grid(row=4, column=0, ipadx=5, ipady=0, sticky="ns")

#         self.ang_vel, self.vel, self.pos = [], [], []

#     def set_detection_json(self):
#         self.det_obj = ObjectDetection()
#         self.det_obj.start_camera()



# ########################################################################################################################################################
# class RobotController(ctk.CTkFrame, JsonArduino):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#         # self.status_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
#         self.label_1 = ctk.CTkLabel(self, text="Robot Controller")
#         self.label_1.grid(row=0, column=0, padx=5, pady=5)

#         self.start_button = ctk.CTkButton(self, text="Start", command=self.start_button_event)
#         self.start_button.grid(row=1, column=0, padx=10, pady=10)

#         self.stop_button = ctk.CTkButton(self, text="Stop", command=self.stop_button_event)
#         self.stop_button.grid(row=2, column=0, padx=10, pady=10)

#         self.spin_button = ctk.CTkButton(self, text="Calibrate", command=self.calibrate_button_event)
#         self.spin_button.grid(row=3, column=0, padx=10, pady=10)

#         self.json_data = ""
        
#     def start_button_event(self):
#         print("start_button click")
#         time.sleep(3)
#         JsonArduino.set_json_data("Start", 1)
#         self.json_data = str(JsonArduino.get_json_data())
#         com.arser.write(self.json_data.encode())

#     def stop_button_event(self):
#         print("stop_button click")
#         JsonArduino.set_json_data("Start", 0)
#         self.json_data = str(JsonArduino.get_json_data())
        
#     def calibrate_button_event(self):
#         print("calibrate_button click")
#         JsonArduino.set_json_data("Calibrate", 1)
#         self.json_data = str(JsonArduino.get_json_data())
#         com.arser.write(self.json_data.encode())
#         JsonArduino.set_json_data("Calibrate", 0)


# ########################################################################################################################################################
# # class Detection(ctk.CTkFrame):
# #     def __init__(self, master, **kwargs):
# #         super().__init__(master, **kwargs)

# #         self.label_title = ctk.CTkLabel(self, text="Detection")
# #         self.label_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# #         self.launch_detection_button = ctk.CTkButton(self, text="Detection Object", command=self.launch_detection, width=100)
# #         self.launch_detection_button.grid(row=1, column=1, padx=5, pady=5, sticky="ns")

# #     def launch_detection(self):
# #         self.launch_detection_button.configure(text="Close Detection", command=self.close_detection)
# #         self.det_obj = ObjectDetection()
# #         th.Thread(target=self.det_obj.get_detetion_data).start()

# #     def close_detection(self):
# #         self.launch_detection_button.configure(text="Detection Object", command=self.launch_detection)
# #         self.det_obj.stop_detection()

# ########################################################################################################################################################
# class PIDRobot(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         self.label_1 = ctk.CTkLabel(self, text="PID Robot")
#         self.label_1.grid(row=0, column=0, padx=0, pady=0)

#         self.label_kp = ctk.CTkLabel(self, text="Kp")
#         self.label_kp.grid(row=1, column=0, padx=5, pady=5)
#         self.entry_kp = ctk.CTkEntry(self, width=50)
#         self.entry_kp.grid(row=1, column=1, padx=5, pady=5)

#         self.button_kp = ctk.CTkButton(self, text="Set X", command=self.set_kp)
#         self.button_kp.grid(row=1, column=2, padx=5, pady=5)

#         self.label_ki = ctk.CTkLabel(self, text="Ki")
#         self.label_ki.grid(row=2, column=0, padx=5, pady=5)
#         self.entry_ki = ctk.CTkEntry(self, width=50)
#         self.entry_ki.grid(row=2, column=1, padx=5, pady=5)

#         # self.button_ki = ctk.CTkButton(self, text="Set Y", command=self.set_ki)
#         # self.button_ki.grid(row=2, column=2, padx=5, pady=5)

#         self.label_kd = ctk.CTkLabel(self, text="Kd")
#         self.label_kd.grid(row=3, column=0, padx=5, pady=5)
#         self.entry_kd = ctk.CTkEntry(self, width=50)
#         self.entry_kd.grid(row=3, column=1, padx=5, pady=5)

#         # self.button_kd = ctk.CTkButton(self, text="Set Z", command=self.set_kd)
#         # self.button_kd.grid(row=3, column=2, padx=10, pady=10)

#         self.kp = 0.0
#         self.ki = 0.0
#         self.kd = 0.0

#     def set_kp(self):
#         print("set_x PID click")
#         self.kp = float(self.entry_kp.get())
#         self.ki = float(self.entry_ki.get())
#         self.kd = float(self.entry_kd.get())
#         JsonArduino.set_json_data("Kx", [self.kp, self.ki, self.kd])

#     def set_ki(self):
#         print("set_ki click")
#         self.kp = float(self.entry_kp.get())
#         self.ki = float(self.entry_ki.get())
#         self.kd = float(self.entry_kd.get())
#         JsonArduino.set_json_data("Ky", [self.kp, self.ki, self.kd])
        
#     def set_kd(self):
#         print("set_kd click")
#         self.kp = float(self.entry_kp.get())
#         self.ki = float(self.entry_ki.get())
#         self.kd = float(self.entry_kd.get())
#         JsonArduino.set_json_data("Kw", [self.kp, self.ki, self.kd])
        
# ########################################################################################################################################################
# class StatusRobot(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         self.status_frame = ctk.CTkFrame(self.master, corner_radius=0, fg_color="transparent", border_color="blue", border_width=1)
#         self.label_1 = ctk.CTkLabel(self, text="Status Robot")
#         self.label_1.grid(row=0, column=0, padx=10, pady=10, sticky="ns", columnspan=2)

#         self.label_x = ctk.CTkLabel(self, text="X: ")
#         self.label_x.grid(row=1, column=0, padx=10, pady=10)
#         self.label_x_val = ctk.CTkLabel(self, text="0")
#         self.label_x_val.grid(row=1, column=1, padx=10, pady=10)

#         self.label_y = ctk.CTkLabel(self, text="Y: ")
#         self.label_y.grid(row=2, column=0, padx=10, pady=10)
#         self.label_y_val = ctk.CTkLabel(self, text="0")
#         self.label_y_val.grid(row=2, column=1, padx=10, pady=10)

#         self.label_z = ctk.CTkLabel(self, text="Z: ")
#         self.label_z.grid(row=3, column=0, padx=10, pady=10)
#         self.label_z_val = ctk.CTkLabel(self, text="0")
#         self.label_z_val.grid(row=3, column=1, padx=10, pady=10)

#         self.label_roll = ctk.CTkLabel(self, text="Roll: ")
#         self.label_roll.grid(row=1, column=2, padx=10, pady=10)
#         self.label_roll_val = ctk.CTkLabel(self, text="0")
#         self.label_roll_val.grid(row=1, column=3, padx=10, pady=10)
        

#         self.label_pitch = ctk.CTkLabel(self, text="Pitch: ")
#         self.label_pitch.grid(row=2, column=2, padx=10, pady=10)
#         self.label_pitch_val = ctk.CTkLabel(self, text="0")
#         self.label_pitch_val.grid(row=2, column=3, padx=10, pady=10)

#         self.label_yaw = ctk.CTkLabel(self, text="Yaw: ")
#         self.label_yaw.grid(row=3, column=2, padx=10, pady=10)
#         self.label_yaw_val = ctk.CTkLabel(self, text="0")
#         self.label_yaw_val.grid(row=3, column=3, padx=10, pady=10)
    
#     # def update_status(self):
#     #     pos = self.pos_cam.get_position()
#     #     self.label_x_val.configure(text="{:.2f}".format(pos.x))

# ########################################################################################################################################################
# class Mode(ctk.CTkTabview):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         # create tabs
#         self.add("Manual")
#         self.add("Automatic")

#         self.manual_control = ManualControl(self.tab("Manual"), border_width=2, width=300, height=300)
#         self.manual_control.grid(row=0, column=0, ipadx=0, ipady=10)


# ########################################################################################################################################################
# class ManualControl(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         self.label_vx = ctk.CTkLabel(self, text="Vx")
#         self.label_vx.grid(row=0, column=0, padx=5, pady=5)
#         self.entry_vx = ctk.CTkEntry(self, width=60)
#         self.entry_vx.grid(row=0, column=1, padx=5, pady=5)

#         self.label_vy = ctk.CTkLabel(self, text="Vy")
#         self.label_vy.grid(row=1, column=0, padx=5, pady=5)
#         self.entry_vy = ctk.CTkEntry(self, width=60)
#         self.entry_vy.grid(row=1, column=1, padx=5, pady=5)

#         self.label_omega = ctk.CTkLabel(self, text="Omega")
#         self.label_omega.grid(row=2, column=0, padx=5, pady=5)
#         self.entry_omega = ctk.CTkEntry(self, width=60)
#         self.entry_omega.grid(row=2, column=1, padx=5, pady=5)

#         self.label_distance = ctk.CTkLabel(self, text="Distance", width=20)
#         self.label_distance.grid(row=0, column=2, padx=5, pady=5)
#         self.entry_distance = ctk.CTkEntry(self, width=60)
#         self.entry_distance.grid(row=0, column=3, padx=5, pady=5)

#         self.label_time = ctk.CTkLabel(self, text="Time", width=20)
#         self.label_time.grid(row=1, column=2, padx=5, pady=5)
#         self.entry_time = ctk.CTkEntry(self, width=60)
#         self.entry_time.grid(row=1, column=3, padx=5, pady=5)

#         self.send_button = ctk.CTkButton(self, text="Send", command=self.send_button_event)
#         self.send_button.grid(row=2, column=2, padx=5, pady=5, columnspan=2)

#     def send_button_event(self):
#         print("send_button click")
    


# class Robot_Configuration(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         self.title_label = ctk.CTkLabel(self, text="Robot Configuration")
#         self.title_label.grid(row=0, columnspan=2, padx=10, pady=10, sticky="we")

#         self.velo_ball_label = ctk.CTkLabel(self, text="Velocity Ball")
#         self.velo_ball_label.grid(row=1, column=0, padx=(30, 0), pady=5, sticky="e")
#         self.velo_ball_entry = ctk.CTkEntry(self)
#         self.velo_ball_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")

#         self.veloX_init_label = ctk.CTkLabel(self, text="Velocity X Init")
#         self.veloX_init_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
#         self.veloX_init_entry = ctk.CTkEntry(self)
#         self.veloX_init_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

#         self.veloY_init_label = ctk.CTkLabel(self, text="Velocity Y Init")
#         self.veloY_init_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
#         self.veloY_init_entry = ctk.CTkEntry(self)
#         self.veloY_init_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")

#         self.acc_label = ctk.CTkLabel(self, text="Accerlation")
#         self.acc_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
#         self.acc_entry = ctk.CTkEntry(self)
#         self.acc_entry.grid(row=4, column=1, padx=5, pady=5)


#         self.Dis_label = ctk.CTkLabel(self, text="Distance 1")
#         self.Dis_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
#         self.Dis_entry = ctk.CTkEntry(self)
#         self.Dis_entry.grid(row=5, column=1, padx=5, pady=5)

#         self.dis2_label = ctk.CTkLabel(self, text="Distance 2")
#         self.dis2_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
#         self.dis2_entry = ctk.CTkEntry(self)
#         self.dis2_entry.grid(row=6, column=1, padx=5, pady=5)

#         self.dis3_label = ctk.CTkLabel(self, text="Distance 3")
#         self.dis3_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
#         self.dis3_entry = ctk.CTkEntry(self)
#         self.dis3_entry.grid(row=7, column=1, padx=5, pady=5)

#         self.setting_button = ctk.CTkButton(self, text="Send", command=self.send_button_event)
#         self.setting_button.grid(row=8, column=1, padx=5, pady=5)

#         self.vel_ball = 0.0
#         self.velx_init = 0.0
#         self.vely_init = 0.0
#         self.acc = 0.0
#         self.Dis = 0.0
#         self.dis2 = 0.0
#         self.dis3 = 0.0

#     def send_button_event(self):
#         print("send_button_click")
#         self.vel_ball = float(self.velo_ball_entry.get())
#         self.velx_init = float(self.veloX_init_entry.get())
#         self.vely_init = float(self.veloY_init_entry.get())
#         self.acc = float(self.acc_entry.get())
#         self.Dis = float(self.Dis_entry.get())
#         self.dis2 = float(self.dis2_entry.get())
#         self.dis3 = float(self.dis3_entry.get())
#         JsonArduino.set_json_data("Velo_ball", self.vel_ball)
#         JsonArduino.set_json_data("VeloX_init", self.velx_init)
#         JsonArduino.set_json_data("VeloY_init", self.vely_init)
#         JsonArduino.set_json_data("Acce", self.acc)
#         JsonArduino.set_json_data("Distance_init", [self.Dis, self.dis2, self.dis3])
#         JsonArduino.display_json_data()
        
       






