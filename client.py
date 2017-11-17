import rpyc
from constRPYC import *
from threading import Thread
from rpyc.utils.server import ThreadedServer

class Client(rpyc.Service):
    def exposed_UploadFile(self,file):
        data = []
        file = open(file, 'r')
        if file:
            for line in file:
                data.append(line)
            file.close()
        return data

    def exposed_DownloadFile(self,newFileName,data):
        file = open(newFileName, 'ab')
        for line in data :
            file.write(line)
        file.close()
        
def startClient(connHost,connPort):
    cl = ThreadedServer(Client, hostname=connHost, port=connPort)
    client_server_thread = Thread(target=cl.start)
    client_server_thread.daemon = True
    client_server_thread.start()

    mainMenu = {
        '1': "Register on the SERVER.",
        '2': "Find And Download File.",
        '3': "Exit."
    }
    conn = rpyc.connect(SV_HOST, SV_PORT)
    while True:
        options = mainMenu.keys()
        for entry in options:
            print entry, mainMenu[entry]

        decision = raw_input("What to do next?\n")
        if decision == '1':
            File = raw_input("What file to add?\n")
            conn.root.exposed_Register(connPort, File)
        elif decision == '2':
            NameOfFile = raw_input("What file to search for?\n")
            PORTOfSearchedFile = conn.root.exposed_SearchFiles(NameOfFile)
            if len(PORTOfSearchedFile) > 1:
                print 'from which port?'
                i = 0
                for port in PORTOfSearchedFile:
                    print str(i) + '- ' +str(port)
                    i = i + 1
                deci = input()
                selectedPort = PORTOfSearchedFile[deci]
            else:
                selectedPort = PORTOfSearchedFile[0]
                
            FilePath = conn.root.exposed_FilePath(selectedPort, NameOfFile)
            conn2 = rpyc.connect(SV_HOST, selectedPort)
            data = conn2.root.exposed_UploadFile(FilePath)
            fileName = raw_input("save as?\n")
            conn2.root.exposed_DownloadFile(fileName, data)
        elif decision == '3':
            quit()
        else:
            print 'make right choice'
            break