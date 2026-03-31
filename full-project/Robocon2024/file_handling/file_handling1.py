data = {
            "Mode": 0,
            "Retry": 0,
            "Calibrate": 0,
            "Start": 0,
            "Kx": [0.1, 0.0, 0.0],
            "Ky": [0.1, 0.0, 0.0],
            "Kw": [0.1, 0.0, 0.0],
            "Angular_velocity": [0.0, 0.0, 0.0],
            "Velocity": [0.0, 0.0, 0.0],
            "Position": [0.0, 0.0, 0.0]
        }

Mode = 0
Retry = 0
Calibrate = 0
Start = 0
Kx = [0.0, 0.0, 0.0]
Ky = [0.0, 0.0, 0.0]
Kw = [0.0, 0.0, 0.0]
Angular_velocity = [0.0, 0.0, 0.0]
Velocity = [0.0, 0.0, 0.0]
Position = [0.0, 0.0, 0.0]

def readFile():

    file = open("data.txt", "r")
    if not file:
        return

    while True:
        line = file.readline()
        if not line:
            break

        Mode = line.strip()
        Retry = file.readline().strip()
        Calibrate = file.readline().strip()
        Start = file.readline().strip()
        Kx = file.readline().strip()
        Ky = file.readline().strip()
        Kw = file.readline().strip()
        Angular_velocity = file.readline().strip()
        Velocity = file.readline().strip()
        Position = file.readline().strip()

    data = {
            "Mode": Mode,
            "Retry": Retry,
            "Calibrate": Calibrate,
            "Start": Start,
            "Kx": Kx,
            "Ky": Ky,
            "Kw": Kw,
            "Angular_velocity": Angular_velocity,
            "Velocity": Velocity,
            "Position": Position
        }

    print(data)

    file.close()


def saveFile(Mode, Retry, Calibrate, Start, Kx, Ky, Kw, Angular_velocity, Velocity, Position):
    file = open("data.txt", "w")

    file.write(f"{Mode}\n{Retry}\n{Calibrate}\n{Start}\n{Kx}\n{Ky}\n{Kw}\n{Angular_velocity}\n{Velocity}\n{Position}\n")

    file.close()

# saveFile(Mode, Retry, Calibrate, Start, Kx, Ky, Kw, [0.0, 0.0, 6.0], Velocity, Position)
readFile()