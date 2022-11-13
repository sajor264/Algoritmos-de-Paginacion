import random
from Ram import Ram
from Disk import Disk

class Random:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setExecTime(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getExecTime(self):
        return self.__execTime


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setExecTime(self, execTime):
        self.__execTime = execTime


    # FUNCTIONS
    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def removeFromDisk(self, page):
        self.getDisk().removePage(page)

    def allocateInDisk(self, page):
        self.getDisk().allocatePage(page)

    def addExecTime(self, time):
        tempExecTime = self.getExecTime()
        tempExecTime += time
        self.setExecTime(tempExecTime)
    
    def delPag(self, page):
        None
    
    def getMarke(self):
        return False

    def allocate(self, newPage):
        self.addExecTime(1)
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    #time.sleep(5)
                self.allocateInRam(newPage)
            else:
                page2Remove = random.choice(self.getRam().getMemory())
                self.removeFromRam(page2Remove)
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    #time.sleep(5)
                self.allocateInRam(newPage)
                self.allocateInDisk(page2Remove)
            self.addExecTime(5)
        elif newPage not in self.getRam().getMemory():
                self.allocateInRam(newPage)
                self.addExecTime(5)