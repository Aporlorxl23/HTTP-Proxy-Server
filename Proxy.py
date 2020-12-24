#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, sys, thread

class Proxy:

    def __init__(self,Port):
        self.Ip = '' # Localhost
        self.Port = int(Port) # Set Port Number
        self.BACKLOG = 50 # A maximum of 50 connections will wait in the back
        self.MAX_DATA_RECV = 4096
        self.Attacker_Response = b"<img src=x onerror=alert`Aporlorxl23_HTTP_Proxy_Server`>"
        self.DEBUG = False
        self.Attacker_Mode = False
        self.LOG = [False,"Proxy-Log.txt"]
        self.File = ""

    def Start_Server(self):
        try:
            Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Socket.bind((self.Ip,self.Port))
            Socket.listen(self.BACKLOG)
            if self.LOG[0] == True:
                self.File = open(self.LOG[1],"a")
            while 1:
                Connection, Connection_Addr = Socket.accept()
                thread.start_new_thread(self.Send_Response, (Connection, Connection_Addr))
        except socket.error as Message:
            if Socket:
                Socket.close()
            print("[-] Could Not Open Socket:", Message)
            sys.exit(1)
        except Exception as Error:
            print("[-] Could Not Start Program:", Error)
            sys.exit(1)
    def Send_Response(self,Connection, Connection_Addr):
        try:
            Request = Connection.recv(self.MAX_DATA_RECV)
            if self.LOG[0] == True:
                self.File.write(Request)
            AllData = Request.split()
            try:
                print("[+] Request Method: "+str(AllData[0])+" Url: "+str(AllData[1])+" "+str(AllData[2]))
            except:
                pass
            if self.Attacker_Mode:
                Connection.send(self.Attacker_Response)
            else:
                Data = AllData[1]
                Storeindex = Data.find("://")
                Url = Data[Storeindex+3:]
                Storeindex = Url.find("/")
                Url = Url[:Storeindex]
                Storeindex = Url.find(":")
                Port = 80
                if Storeindex != -1:
                    Port = int(Url[Storeindex+1:])
                if Url.find(":") != -1:
                    Storeindex = Url.find(":")
                    Url = Url[:Storeindex]
                PSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                PSocket.connect((Url, Port))
                PSocket.send(Request)
                while 1:
                    Data = PSocket.recv(self.MAX_DATA_RECV)
                    if (len(Data) > 0):
                        Connection.send(Data)
                        print("[+] Response Sended Browser! "+str(AllData[1]))
                    else:
                        break
        except socket.error as Message:
            if PSocket:
                PSocket.close()
            if self.DEBUG:
                print("[-] Could Not Open Socket:", Message)
            sys.exit(1)
        except Exception as Error:
            print("[-] Could Not Start Program:", Error)
            sys.exit(1)
        finally:
            if self.Attacker_Mode == False:
                PSocket.close()
            Connection.close()
if __name__ == "__main__":
    Proxy = Proxy(sys.argv[1])
    Proxy.Start_Server()
    
#Eren Şimşek <Aporlorxl23>
