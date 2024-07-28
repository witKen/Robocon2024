import customtkinter as ctk
from robot.communication.json_arudino import JsonArduino
from application.screen.testing_screen import TestMenuScreen 
from file_handling.file_handling import TeamSelectionHandler as tsh

class MainMenu(ctk.CTkFrame, JsonArduino):
    def __init__(self, master, team_selection_screen, det_obj,**kwargs):
        super().__init__(master, **kwargs)
        
        self.det_obj = det_obj

        self.master = master
        self.team_selection_screen = team_selection_screen

        self.team = tsh.readTeamFile(self)

        if self.team == "1":
            self.label_1 = ctk.CTkLabel(self, text="Robot Controller Red Team")
            self.label_1.grid(row=0, column=0, padx=560/2, pady=5)
        elif self.team == "2":
            self.label_1 = ctk.CTkLabel(self, text="Robot Controller Blue Team")
            self.label_1.grid(row=0, column=0, padx=560/2, pady=5)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_button_event)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.stop_button = ctk.CTkButton(self, text="Configuration", command=self.configuration_button_event)
        self.stop_button.grid(row=2, column=0, padx=10, pady=10)

        self.spin_button = ctk.CTkButton(self, text="Test", command=self.test_button_event)
        self.spin_button.grid(row=3, column=0, padx=10, pady=10)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.grid(row=4, column=0, padx=5, pady=5)
        
        self.json_data = ""

        self.det_obj.update_team()

    def back(self):
        print("back click")
        self.grid_forget()
        self.team_selection_screen.grid()

        
    def start_button_event(self):
        print("start_button click")

    def configuration_button_event(self):
        print("stop_button click")
        
    def test_button_event(self):
        self.grid_forget()
        test_menu = TestMenuScreen(self.master, self, self.det_obj,border_width=2)
        test_menu.grid(row=0, column=0, sticky='nsew')

