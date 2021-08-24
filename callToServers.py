import threading
import time
import argparse



class CallToServers:
    def __init__(self, server, callback = None):
        self.server = server
        self._stopScraping = threading.Event()
        self.callback = callback 
        self.serverStatus = None
        
        if self.callback:
            threading.Thread(target=self._updater, args=(self.callback, self._stopScraping)).start()
            
            
    def stopScraping(self):
        self._stopScraping.set()
        
    
        
    def CallToServer(self,):
        return {'name':self.server,
                'status':self.serverStatus,
                }
    
    def checkForUpdate(self, callback):
        #perform req to the server and check for service
        self.serverStatus = response_from_server
        if callback:
            callback(self.CallToServer())
        else:
            self.stopScraping
        
    def _updater(self, callback, isScraping):
        while not isScraping.is_set():
            self.checkForUpdate(callback)
            time.sleep(300) #sleep for 5mins before making next request to the server
            

def serverStatusDetails(ServerStatus):
    name = ServerStatus['name']
    status = ServerStatus['status']
    print(f'Name -> {name},  Status -> {status}')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter the server to send reqest')
    parser.add_argument('--name', help='Name of the server', choices=['nginx', 'mongodb'], required=True)
    args = parser.parse_args()
    
    cs = CallToServers(args.name, serverStatusDetails)