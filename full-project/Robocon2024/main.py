import customtkinter as ctk
from application.screen.team_selection import TeamSelectionScreen
import threading as th
import time
import robot.communication.serialarduino as com
from file_handling.file_handling import TestPIDHandler as tph
from robot.communication.json_arudino import JsonArduino

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CADT01 Robot R2")
        self.geometry(f"{700}x{580}")

        ctk.set_widget_scaling(100/100)

        self.thread = None
        self.Kpx, self.Kix, self.Kdx, self.Kpy, self.Kiy, self.Kdy, self.Kpw, self.Kiw, self.Kdw = tph.readPIDTestFile(self)
        Kx = [self.Kpx, self.Kix, self.Kdx]
        ky = [self.Kpy, self.Kiy, self.Kdy]
        kw = [self.Kpw, self.Kiw, self.Kdw]
        JsonArduino.set_json_data("Kx", Kx)
        JsonArduino.set_json_data("Ky", ky)
        JsonArduino.set_json_data("Kw", kw)
        self.teamSelectionScreen = TeamSelectionScreen(self, border_width=2)
        self.teamSelectionScreen.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')

        self.thread_flag = True  # Flag to control the thread

        # Start the thread
        self.thread = th.Thread(target=self.thread_function, daemon=True)
        self.thread.start()

        self.check_thread_flag()  # Start checking the thread flag periodically

    def thread_function(self):
        com.ar_read_from_port(com.arser)
        print("Thread ended")

    def check_thread_flag(self):
        if not self.thread_flag:
            self.destroy()
        else:
            self.after(100, self.check_thread_flag)  # Check again after 100 milliseconds

    def on_window_close(self):
        # Set the flag to False to stop the thread
        self.thread_flag = False
        self.thread.join(1)  # Wait for the thread to finish
        self.destroy()  # Close the window

if __name__ == "__main__":
    app = App()
    app.mainloop()