from Ram import Ram
from Disk import Disk

class Lru:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setMemoryAccesses([])
        self.setExecTime(0)
        self.setThrashingTime(0)
        self.setMarked(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk
    
    def getMemoryAccesses(self):
        return self.__memoryAccesses

    def getMarked(self):
        return self.__marked

    def getExecTime(self):
        return self.__execTime

    def getThrashingTime(self):
        return self.__thrashingTime


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setMemoryAccesses(self, memoryAccesses):
        self.__memoryAccesses = memoryAccesses

    def setMarked(self, marked):
        self.__marked = marked

    def setExecTime(self, execTime):
        self.__execTime = execTime

    def setRunningTime(self, runningTime):
        self.__runningTime = runningTime

    def setThrashingTime(self, thrashingTime):
        self.__thrashingTime = thrashingTime


    # FUNCTIONS
    def addMemoryAccess(self, page):
        tempMem = self.getMemoryAccesses()
        tempMem.insert(0, page)
        self.setMemoryAccesses(tempMem)

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
        dic = {}
        for pag in self.getRam().getMemory():
            if(self.getMarked() != pag):
                dic[pag] = 0
        dic[self.getMarked()]=1
        return dic

    def allocate(self, newPage):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                self.allocateInRam(newPage)
                self.addMemoryAccess(newPage)
            else:
                memoryAccesses = self.getMemoryAccesses()
                page2Remove = self.getRam().getMemory()[0]
                index = -1
                marked = [-1, index]
                for page2Remove in self.getRam().getMemory():
                    index = memoryAccesses.index(page2Remove)
                    if index > marked[1]:
                        marked = [page2Remove, index]
                self.setMarked(marked[0])
                self.removeFromRam(marked[0]) 
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                self.allocateInRam(newPage)
                self.allocateInDisk(marked[0])
                self.addMemoryAccess(newPage)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage)
            self.addMemoryAccess(newPage)