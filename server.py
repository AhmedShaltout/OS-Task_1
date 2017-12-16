import rpyc
from rpyc.utils.server import ThreadedServer
from constRPYC import *

class server(rpyc.Service):
    activePeers={}
    files={}

    def exposed_RegisterUser(self, userName, port):
        if port in self.activePeers:
            print str(port) + " tried to register 2 times from the same machine.."
            return "can't register 2 times from the same machine"
        self.activePeers[port] = userName
        print userName + " is successfully registered.."
        return "you are registered successfully.."

    def exposed_AddFile(self, port, file):
        if port in self.activePeers:
            try:
                if file not in self.files[port]:
                    self.files[port].append(file)
                else:
                    return "this file was added before.."
            except:
                self.files[port]= [file]
            return "added successfully.."
        else:
            return "please you need to register first.."

    def exposed_SearchFiles(self,file):
        ports = []
        for port in self.activePeers:
            try:
                if file in self.files[port]:
                    ports.append(port)
            except:
                continue
        return ports
    
    def exposed_editServerData(self, filename, port):
        self.files[port].remove(filename)

if __name__ == "__main__":
    server = ThreadedServer(server, hostname=SV_HOST, port=SV_PORT)
    server.start()


