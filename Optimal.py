from Ram import Ram
from Disk import Disk
import time

class Optimal:

    def __init__(self, memCalls):
        self.setMemCalls(memCalls)
        self.setRam(Ram())
        self.setDisk(Disk())

    
    # GETTERS
    def getMemCalls(self):
        return self.__memCalls

    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk


    # SETTERS
    def setMemCalls(self, memCalls):
        self.__memCalls = memCalls

    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk


    # FUNCTIONS
    def getNextMemCall(self):
        tempQueue = self.getMemCalls()
        element = tempQueue.pop()
        self.setMemCalls(tempQueue)
        return element

    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def removeFromDisk(self, page):
        self.getDisk().removePage(page)

    def allocateInDisk(self, page):
        self.getDisk().allocatePage(page)

    def allocateNext(self):
        for page in self.getNextMemCall():
            if self.getRam().isFull() and page not in self.getRam().getMemory():
                if 0 in self.getRam().getMemory():
                    if(page in self.getDisk().getMemory()):
                        self.removeFromDisk(page)
                        #time.sleep(5)
                    self.allocateInRam(page)
                else:
                    restOfMemCalls = self.getMemCalls().getQueue()
                    index = -1
                    marked = [-1, index]
                    for page2Remove in self.getRam().getMemory():
                        found = False
                        for restPage in restOfMemCalls:
                            if page2Remove in restPage:
                                index = restOfMemCalls.index(restPage)
                                found = True
                        if index > marked[1]:
                            marked = [page2Remove, index]
                        if not found:
                            marked = [page2Remove, index]
                            break
                    self.removeFromRam(marked[0])
                    if(page in self.getDisk().getMemory()):
                        self.removeFromDisk(page)
                        #time.sleep(5)
                    self.allocateInRam(page)
                    self.allocateInDisk(marked[0])
            elif page not in self.getRam().getMemory():
                self.allocateInRam(page)