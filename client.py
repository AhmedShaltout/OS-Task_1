import rpyc
from constRPYC import *
from threading import Thread
import socket
from rpyc.utils.server import ThreadedServer
import os.path

class Client(rpyc.Service):
    def exposed_UploadFile(self,file):
        data = []
        try:
            file = open(file, 'rb')
            if file:
                for line in file:
                    data.append(line)
                file.close()
        except:
            data = None
        return data
        
def startClient(connHost,connPort):
    cl = ThreadedServer(Client, hostname=connHost, port=connPort)
    client_server_thread = Thread(target=cl.start)
    client_server_thread.daemon = True
    client_server_thread.start()
    clientMenu(connPort)       

def clientMenu(connPort):
    try:
        conn = rpyc.connect(SV_HOST, SV_PORT)
    except socket.error as e:
        if e.errno == 98:
            print "cann't open 2 instants of the same client.."
        else:
            print "unexpected error occured..\n" 
    while True:
        try:
            options = mainMenu.keys()
            for entry in options:
                print entry, mainMenu[entry]
            decision = raw_input("What to do next?\n")
            if decision == '1':
                name = raw_input("Enter your name..")
                print conn.root.exposed_RegisterUser(name, connPort)
            elif decision == '2':
                file = raw_input("what file to add?")
                if os.path.isfile(file):
                    print conn.root.exposed_AddFile(connPort, file)
                else:
                    print "file doesn't"
            elif decision == '3':
                fileName = raw_input("What file to search for?")
                ports = conn.root.exposed_SearchFiles(fileName)
                if len(ports) == 0:
                    print "file not found..\n"
                else:
                    can = []
                    for port in ports:
                        try:
                            fakeConn = rpyc.connect(SV_HOST,port)
                            fakeConn.close()
                            can.append(port)
                        except Exception:
                            continue
                    ports = None
                    if len(can) > 0:
                        while True:
                            print "which peer to download from?"
                            i = 0
                            for port in can:
                                print str(i) +"- "+ str(port)
                                i = i + 1
                            deci = input()
                            try:
                                selectedPort = can[deci]
                                break
                            except:
                                print "select between the givin ports please..\n"
                        getFileConnection = rpyc.connect(SV_HOST, selectedPort)
                        saveAs = raw_input("Save as? ")
                        data = getFileConnection.root.exposed_UploadFile(fileName)
                        if not data:
                            print "it seems that the user deleted the file.. editing the server.."
                            conn.root.exposed_editServerData(fileName,selectedPort)
                        else:
                            file = open(saveAs, 'wb')
                            for line in data :
                                file.write(line)
                            file.close()
                    else:
                        print "file is here but the owner is offline now.."
            elif decision == '4':
                conn.close()
                quit()
            else:
                print "make a correct desision\n"
        except:
            conn.close()
            quit()

