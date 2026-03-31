import customtkinter as ctk
from file_handling.file_handling import TeamSelectionHandler as tsh
from application.screen.main_menu import MainMenu
from robot.detection.camera.camera import Camera
from robot.detection.services.object_detection import ObjectDetection  
from robot.communication.json_arudino import JsonArduino
import threading as th

class TeamSelectionScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.run_camera_thread = None

        self.cam = Camera()

        self.run_camera_thread = th.Thread(target=self.set_detection_json, daemon=True)
        self.run_camera_thread.start()

        self.title_label = ctk.CTkLabel(self, text="Select Team")
        self.title_label.grid(row=0, column=0, padx=580/2, pady=10)

        self.red_button = ctk.CTkButton(self, text="Red Team", command=self.redTeam)
        self.red_button.grid(row=1, column=0, padx=5, pady=5)

        self.blue_button = ctk.CTkButton(self, text="Blue Team", command=self.blueTeam)
        self.blue_button.grid(row=2, column=0, padx=5, pady=5)

    def set_detection_json(self):
        self.det_obj = ObjectDetection()
        self.det_obj.start_camera(self.cam) 
        # JsonArduino.set_json_data("Detection", 1)
        # self.json_data = str(JsonArduino.get_json_data())

    def redTeam(self):
        tsh.saveSelectedTeam(self, 1)
        JsonArduino.set_json_data("Team", 1)
        self.grid_forget()
        test_menu = MainMenu(self.master, self, self.det_obj,border_width=2)
        test_menu.grid(row=0, column=0, sticky='nsew')

    def blueTeam(self):
        tsh.saveSelectedTeam(self, 2)
        JsonArduino.set_json_data("Team", 2)
        self.grid_forget()
        test_menu = MainMenu(self.master, self, self.det_obj, border_width=2)
        test_menu.grid(row=0, column=0, sticky='nsew')
