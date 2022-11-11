from Ram import Ram
from Disk import Disk
import time
from itertools import cycle, islice

class SecondChance:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setClock([])
        self.setVictim(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getClock(self):
        return self.__clock

    def getVictim(self):
        return self.__victim


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setClock(self, clock):
        self.__clock = clock

    def setVictim(self, victim):
        self.__victim = victim


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

    def allocate(self, newPage):
        if self.getRam().isFull():
            if newPage not in self.getRam().getMemory():
                victim = self.getVictim()
                replaced = False
                clock = self.getClock()
                index = victim
                while not replaced:
                    if clock[index][1] == 0:
                        page2Remove = clock[index][0]
                        clock[index][0] = newPage
                        clock[index][1] = 1
                        replaced = True
                    else:
                        clock[index][1] = 0
                    index += 1
                    if(index == len(clock)):
                        index = 0
                self.setVictim(index)
                self.setClock(clock)
                self.removeFromRam(page2Remove)
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    time.sleep(5)
                self.allocateInRam(newPage)
                self.allocateInDisk(page2Remove)
            else:
                changed = False
                clock = self.getClock()
                index = 0
                while(not changed):
                    if clock[index][0] == newPage:
                        clock[index][1] = 1
                        changed = True
                    index += 1
                self.setClock(clock)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage)
            self.addInClock(newPage)