import random
from Ram import Ram
from Disk import Disk

class Random:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setExecTime(0)
        self.setThrashingTime(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getExecTime(self):
        return self.__execTime

    def getThrashingTime(self):
        return self.__thrashingTime


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setExecTime(self, execTime):
        self.__execTime = execTime

    def setThrashingTime(self, thrashingTime):
        self.__thrashingTime = thrashingTime


    # FUNCTIONS
    def removeFromRam(self, page):
        self.addExecTime(1)
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.addExecTime(1)
        self.getRam().allocatePage(page)

    def removeFromDisk(self, page):
        self.addExecTime(5)
        self.addThrashingTime(5)
        self.getDisk().removePage(page)

    def allocateInDisk(self, page):
        self.addExecTime(5)
        self.addThrashingTime(5)
        self.getDisk().allocatePage(page)

    def addExecTime(self, time):
        tempExecTime = self.getExecTime()
        tempExecTime += time
        self.setExecTime(tempExecTime)

    def addThrashingTime(self, time):
        tempTime = self.getThrashingTime()
        tempTime += time
        self.setThrashingTime(tempTime)
    
    def delPag(self, page):
        None
    
    def getMarke(self):
        return False

    def allocate(self, newPage):
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
        elif newPage not in self.getRam().getMemory():
                self.allocateInRam(newPage)