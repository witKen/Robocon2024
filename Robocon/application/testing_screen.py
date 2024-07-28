import customtkinter as ctk  
from file_handling.file_handling import TeamSelectionHandler as tsh
from file_handling.file_handling import TestPIDHandler as tph
from robot.communication.json_arudino import JsonArduino
from file_handling.file_handling import testPosHandler as testPos, SetPos0Handler as spo


class TestMenuScreen(ctk.CTkFrame):
    def __init__(self, master, main_menu_screen, det_obj,**kwargs):
        super().__init__(master, **kwargs)

        self.det_obj = det_obj

        self.master = master
        self.main_menu_screen = main_menu_screen
        
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=0, columnspan = 4, padx=5, pady=5, sticky="we")
        
        self.movement_test_frame = MovementTesting(self, self.det_obj ,border_width=2)
        self.movement_test_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nswe") 

        self.display_video_frame = DisplayVideo(self, self.det_obj,border_width=2)
        self.display_video_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nswe") 

    def back(self):
        print("back click")
        self.grid_forget()
        self.main_menu_screen.grid()
        self.det_obj.set_status(0)
        self.det_obj.start_posCam(0)
        JsonArduino.set_json_data("Status", 0)

class Test_T265(ctk.CTkFrame):
    def __init__(self, master, det_obj,**kwargs):
        super().__init__(master, **kwargs)

        self.det_obj = det_obj

        self.title_label = ctk.CTkLabel(self, text="T265")
        self.title_label.grid(row=3, columnspan=2, padx=10, pady=10)

        self.x_label = ctk.CTkLabel(self, text="X")
        self.x_label.grid(row=4, column=0, padx=5, pady=5)
        self.x_entry = ctk.CTkEntry(self)
        self.x_entry.grid(row=4, column=1, padx=5, pady=5)

        self.y_label = ctk.CTkLabel(self, text="Y")
        self.y_label.grid(row=5, column=0, padx=5, pady=5)
        self.y_entry = ctk.CTkEntry(self)
        self.y_entry.grid(row=5, column=1, padx=5, pady=5)

        self.w_label = ctk.CTkLabel(self, text="W")
        self.w_label.grid(row=6, column=0, padx=5, pady=5)
        self.w_entry = ctk.CTkEntry(self)
        self.w_entry.grid(row=6, column=1, padx=5, pady=5)

        self.start_all_button = ctk.CTkButton(self, text="Start", command=self.start)
        self.start_all_button.grid(row=7, columnspan=2, padx=5, pady=5)

        self.x, self.y, self.w = testPos.readTestPosFile(self)

        self.x_entry.insert(0, self.x)
        self.y_entry.insert(0, self.y)
        self.w_entry.insert(0, self.w)

    def start(self):
        
        if self.x_entry.get() == '':
            self.x_entry.insert(0, '0')
        if self.y_entry.get() == '':
            self.y_entry.insert(0, '0')
        if self.w_entry.get() == '':
            self.w_entry.insert(0, '0')

        self.x = float(self.x_entry.get())
        self.y = float(self.y_entry.get())
        self.w = float(self.w_entry.get())

        JsonArduino.set_json_data("Status", 51)
        testPos.saveTestPosFile(self, self.x, self.y, self.w)
        self.det_obj.set_location(self.x, self.y, self.w, 1)

class MovementTesting(ctk.CTkFrame):
    def __init__(self, master, det_obj,**kwargs):
        super().__init__(master, **kwargs)

        self.det_obj = det_obj
        self.label_title = ctk.CTkLabel(self, text="Movement Testing")
        self.label_title.grid(row=0, column=0, padx=10, pady=10)

        self.move_button = ctk.CTkButton(self, text="Move To Zone 3", command=self.move)
        self.move_button.grid(row=1, column=0, padx=10, pady=10)

        self.move_button = ctk.CTkButton(self, text="Retry Zone", command=self.retry)
        self.move_button.grid(row=2, column=0, padx=10, pady=10)

        self.spin_button = ctk.CTkButton(self, text="Spin", command=self.spin)
        self.spin_button.grid(row=3, columnspan=2, padx=5, pady=5)

        self.find_pos0_button = ctk.CTkButton(self, text="Find Pos_0 1", command=self.find_pos0_1)
        self.find_pos0_button.grid(row=4, columnspan=2, padx=5, pady=5)

        self.find_pos0_button = ctk.CTkButton(self, text="Find Pos_0 2", command=self.find_pos0_2)
        self.find_pos0_button.grid(row=5, columnspan=2, padx=5, pady=5)

        self.status = 0

    def spin(self):
        JsonArduino.set_json_data("Status", 70)

    def find_pos0_1(self):
        JsonArduino.set_json_data("Status", 40)
    
    def find_pos0_2(self):
        self.det_obj.set_status(8)

    def move(self):
        JsonArduino.set_json_data("Status", 39)
        self.det_obj.set_status(6)

    def retry(self):
        JsonArduino.set_json_data("Status", 38)
        self.det_obj.set_status(6)


class DisplayVideo(ctk.CTkFrame):
    def __init__(self, master, det_obj,**kwargs):
        super().__init__(master, **kwargs)

        self.det_obj = det_obj
        self.label_title = ctk.CTkLabel(self, text="Test Detection")
        self.label_title.grid(row=0, column=0, padx=10, pady=10)

        self.collect_ball_button = ctk.CTkButton(self, text="Collect Ball", command=self.collect_ball)
        self.collect_ball_button.grid(row=1, column=0, padx=10, pady=10)

        self.check_opp_ball_button = ctk.CTkButton(self, text="Check Opp Ball", command=self.check_opp_ball)
        self.check_opp_ball_button.grid(row=2, column=0, padx=10, pady=10)

        self.detect_silo_button = ctk.CTkButton(self, text="Detect Silo", command=self.detect_silo)
        self.detect_silo_button.grid(row=3, column=0, padx=10, pady=10)

        self.start_pos_button = ctk.CTkButton(self, text="Start Pos", command=self.start_pos)
        self.start_pos_button.grid(row=4, column=0, padx=10, pady=10)

        self.set_new_pos_button = ctk.CTkButton(self, text="New Pos", command=self.set_new_pos)
        self.set_new_pos_button.grid(row=5, column=0, padx=10, pady=10)

        self.Y_Button = ctk.CTkButton(self, text="Set To True", command=self.changeY)
        self.Y_Button.grid(row=6, column=0, padx=10, pady=10)

        self.auto_button = ctk.CTkButton(self, text="Set Auto True", command=self.auto)
        self.auto_button.grid(row=7, column=0, padx=10, pady=10)

        self.run_detection_thread = None

        self.status = 0

    def start_pos(self):
        self.start_pos_button.configure(text="Close Pos", command=self.closePos)
        self.det_obj.start_posCam(1)

    def closePos(self):
        self.start_pos_button.configure(text="Start Pos", command=self.start_pos)
        self.det_obj.start_posCam(0)
    
    def changeY(self):
        self.Y_Button.configure(text="Set To False", command=self.changeN)
        self.det_obj.disYCorrect = True

    def changeN(self):
        self.Y_Button.configure(text="Set To True", command=self.changeY)
        self.det_obj.disYCorrect = False

    def auto(self):
        self.auto_button.configure(text="Set Auto False", command=self.autoF)
        JsonArduino.set_json_data("Status", 37)
        
    def autoF(self):
        self.auto_button.configure(text="Set Auto Trye", command=self.auto)
        JsonArduino.set_json_data("Status", 36)

    def set_new_pos(self):
        x,y,z = self.det_obj.translation.z, self.det_obj.translation.x, self.det_obj.yaw
        x = x * 1000
        y = y * 1000
        spo().savePosFile(x,y,z)
    
    def collect_ball(self):
        self.det_obj.set_status(2)

    def check_opp_ball(self):
        self.det_obj.set_status(100)
    
    def detect_silo(self):
        self.det_obj.set_status(4)
