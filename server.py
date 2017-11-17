import rpyc
from rpyc.utils.server import ThreadedServer
from constRPYC import *

class server(rpyc.Service):
    activePeers={}

    def exposed_Register(self,port,file):
        if(port in self.activePeers):
            self.activePeers[port].append(file)
        else:
            self.activePeers[port]=[file]
        return self.activePeers

    def exposed_SearchFiles(self,file):
        ports = []
        for port in self.activePeers:
            for nameoffile in self.activePeers[port]:
                arr1 = nameoffile.split("/")
                arr1 = arr1[len(arr1) - 1]
                if file==arr1 :
                    ports.append(port)
        return ports

    def exposed_FilePath(self,port,file):
        for nameoffile in self.activePeers[port]:
            arr1 = nameoffile.split("/")
            arr1 = arr1[len(arr1) - 1]
            if arr1==file:
                return nameoffile

if __name__ == "__main__":
    server = ThreadedServer(server, hostname=SV_HOST, port=SV_PORT)
    server.start()


