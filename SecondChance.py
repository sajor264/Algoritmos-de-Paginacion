from Ram import Ram
from Disk import Disk
import time
from itertools import cycle, islice

class SecondChance:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setClock([])
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getClock(self):
        return self.__clock


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setClock(self, clock):
        self.__clock = clock


    # FUNCTIONS
    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def removeFromDisk(self, page):
        self.getDisk().removePage(page)

    def allocateInDisk(self, page):
        self.getDisk().allocatePage(page)

    def addInClock(self, page):
        tempList = self.getClock()
        tempList.append([page, 1])
        self.setClock(tempList)

    def removeFromClock(self, page):
        tempList = self.getClock()
        tempList.remove([page, 0])
        self.setClock(tempList)

    def allocate(self, newPage):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():

            if(newPage in self.getDisk().getMemory()):
                self.removeFromDisk(newPage)
                time.sleep(5)
            self.allocateInRam(newPage)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage)