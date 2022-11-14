from Ram import Ram
from Disk import Disk

class SecondChance:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setClock({})
        self.setVictim(0)
        self.setExecTime(0)
        self.setThrashingTime(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getClock(self):
        return self.__clock

    def getVictim(self):
        return self.__victim

    def getExecTime(self):
        return self.__execTime

    def getThrashingTime(self):
        return self.__thrashingTime


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setClock(self, clock):
        self.__clock = clock

    def setVictim(self, victim):
        self.__victim = victim

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

    def updateClock(self, key, value):
        tempClock = self.getClock()
        tempClock[key] = value
        self.setClock(tempClock)

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
        return self.getClock()

    def allocate(self, newPage):
        if self.getRam().isFull():
            if newPage not in self.getRam().getMemory():
                if 0 in self.getRam().getMemory():
                    if(newPage in self.getDisk().getMemory()):
                        self.removeFromDisk(newPage)
                        #time.sleep(5)
                    self.allocateInRam(newPage)
                    self.updateClock(newPage, 1)
                else:
                    tempRam = self.getRam().getMemory()
                    victim = self.getVictim()
                    replaced = False
                    index = victim
                    while not replaced:
                        if self.getClock()[tempRam[index]] == 0:
                            page2Remove = tempRam[index]
                            self.updateClock(newPage, 1)
                            replaced = True
                        else:
                            self.updateClock(tempRam[index], 0)
                        index += 1
                        if(index == len(tempRam)):
                            index = 0
                    self.setVictim(index)
                    self.removeFromRam(page2Remove)
                    if(newPage in self.getDisk().getMemory()):
                        self.removeFromDisk(newPage)
                        #time.sleep(5)
                    self.allocateInRam(newPage)
                    self.allocateInDisk(page2Remove)
            else:
                self.updateClock(newPage, 1)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage)
            self.updateClock(newPage, 1)