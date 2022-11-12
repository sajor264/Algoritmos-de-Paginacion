import random
from Ram import Ram
from Disk import Disk
import time

class Random:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk


    # FUNCTIONS
    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def removeFromDisk(self, page):
        self.getDisk().removePage(page)

    def allocateInDisk(self, page):
        self.getDisk().allocatePage(page)

    def allocate(self, newPage):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            page2Remove = random.choice(self.getRam().getMemory())
            self.removeFromRam(page2Remove)
            # fallo de pagina
            if(newPage in self.getDisk().getMemory()):
                self.removeFromDisk(newPage)
                #time.sleep(5)
            self.allocateInRam(newPage)
            self.allocateInDisk(page2Remove)
        elif newPage not in self.getRam().getMemory():
                self.allocateInRam(newPage)