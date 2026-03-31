class TeamSelectionHandler:
    def __init__(self):

        self.teamSelection = {
                "Team": 0
            }

        self.Team = 0

    def readTeamFile(self):
        file = open("./data/team.txt", "r")

        if not file: 
            return

        while True:
            line = file.readline()
            if not line:
                break

            self.Team = line.strip()

        data = {
            "Team" : self.Team
        }
        
        file.close

        return self.Team

    def saveSelectedTeam(self, Team):
        file = open("./data/team.txt", "w")

        file.write(f"{Team}\n")

        file.close()

class TestDistanceHandler:
    def __init__(self):

        self.data = {
                "vx": 0.0,
                "vy": 0.0,
                "omega": 0.0,
                "acc": 0.0,
                "dis1": 0.0,
                # "dis2": 0.0,
                # "dis3": 0.0,
                # "dis4": 0.0,
                "ang": 0.0,
                "time": 0.0
            }

        self.vx = 0.0
        self.vy = 0.0
        self.omega = 0.0
        self.acc = 0.0
        self.dis1 = 0.0
        # self.dis2 = 0.0
        # self.dis3 = 0.0
        # self.dis4 = 0.0
        self.ang = 0.0
        self.time = 0.0

    def readTestDistanceFile(self):
        file = open("./data/testing_data/distance_test.txt", "r")
        
        if not file: 
            return

        while True:
            line = file.readline()
            if not line:
                break

            self.vx = line.strip()
            self.vy = file.readline().strip()
            self.omega = file.readline().strip()
            self.acc = file.readline().strip()
            self.dis1 = file.readline().strip()
            # self.dis2 = file.readline().strip()
            # self.dis3 = file.readline().strip()
            # self.dis4 = file.readline().strip()
            self.ang = file.readline().strip()
            self.time = file.readline().strip()

        self.data = {
                "vx": self.vx,
                "vy": self.vy,
                "omega": self.omega,
                "acc": self.acc,
                "dis1": self.dis1,
                # "dis2": self.dis2,
                # "dis3": self.dis3,
                # "dis4": self.dis4,
                "ang": self.ang,
                "time": self.time
            }

        file.close()

        return self.vx, self.vy, self.omega, self.acc, self.dis1, self.ang, self.time

    def saveTestDistanceFile(self, vx, vy, omega, acc, dis1, ang, time):
        file = open("./data/testing_data/distance_test.txt", "w")

        file.write(f"{vx}\n{vy}\n{omega}\n{acc}\n{dis1}\n{ang}\n{time}\n")

        file.close()


class ObjectDetectionModeTestHandler:
    def __init__(self):

        self.modeSelection = {
                "Mode": 0,
            }

        self.mode = 0

    def readObjectDetectionModeTestFile(self):
        file = open("./data/testing_data/object_detection_mode_test.txt", "r")
        
        if not file: 
            return

        while True:
            line = file.readline()
            if not line:
                break

            self.mode = line.strip()

        self.modeSelection = {
                "Mode": self.mode,
            }

        file.close()

        return self.mode

    def saveObjectDetectionModeTestFile(self, mode):
        file = open("./data/testing_data/object_detection_mode_test.txt", "w")

        file.write(f"{mode}\n")

        file.close()


class TestPIDHandler:
    def __init__(self):

        self.data = {
                "Kpx": 0.1,
                "Kix": 0.0,
                "Kdx": 0.0,
                "Kpy": 0.1,
                "Kiy": 0.0,
                "Kdy": 0.0,
                "Kpw": 0.1,
                "Kiw": 0.0,
                "Kdw": 0.0
            }

        self.Kpx = 0.1
        self.Kix = 0.0
        self.Kdx = 0.0
        self.Kpy = 0.1
        self.Kiy = 0.0
        self.Kdy = 0.0
        self.Kpw = 0.1
        self.Kiw = 0.0
        self.Kdw = 0.0

    def readPIDTestFile(self):
        file = open("./data/testing_data/pid_test.txt", "r")
        
        if not file: 
            return

        while True:
            line = file.readline()
            if not line:
                break

            self.Kpx = line.strip()
            self.Kix = file.readline().strip()
            self.Kdx = file.readline().strip()
            self.Kpy = file.readline().strip()
            self.Kiy = file.readline().strip()
            self.Kdy = file.readline().strip()
            self.Kpw = file.readline().strip()
            self.Kiw = file.readline().strip()
            self.Kdw = file.readline().strip()


        self.data = {
                "Kpx": self.Kpx,
                "Kix": self.Kix,
                "Kdx": self.Kdx,
                "Kpy": self.Kpy,
                "Kiy": self.Kiy,
                "Kdy": self.Kdy,
                "Kpw": self.Kpw,
                "Kiw": self.Kiw,
                "Kdw": self.Kdw
            }

        file.close()

        return self.Kpx, self.Kix, self.Kdx, self.Kpy, self.Kiy, self.Kdy, self.Kpw, self.Kiw, self.Kdw

    def savePIDTestFile(self, Kpx, Kix, Kdx, Kpy, Kiy, Kdy, Kpw, Kiw, Kdw):
        file = open("./data/testing_data/pid_test.txt", "w")

        file.write(f"{Kpx}\n{Kix}\n{Kdx}\n{Kpy}\n{Kiy}\n{Kdy}\n{Kpw}\n{Kiw}\n{Kdw}\n")

        file.close()
