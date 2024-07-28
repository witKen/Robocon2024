import customtkinter as ctk
from file_handling.file_handling import TeamSelectionHandler as tsh
from application.screen.main_menu import MainMenu
from robot.communication.json_arudino import JsonArduino

class TeamSelectionScreen(ctk.CTkFrame):
    def __init__(self, master, det_obj, **kwargs):
        super().__init__(master, **kwargs)

        self.title_label = ctk.CTkLabel(self, text="Select Team")
        self.title_label.grid(row=0, column=0, padx=580/2, pady=10)

        self.red_button = ctk.CTkButton(self, text="Red Team", command=self.redTeam)
        self.red_button.grid(row=1, column=0, padx=5, pady=5)

        self.blue_button = ctk.CTkButton(self, text="Blue Team", command=self.blueTeam)
        self.blue_button.grid(row=2, column=0, padx=5, pady=5)

        self.det_obj = det_obj

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
