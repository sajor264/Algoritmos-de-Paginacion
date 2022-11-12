from Ram import Ram
from Disk import Disk
import time

class Lru:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setMemoryAccesses([])
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk
    
    def getMemoryAccesses(self):
        return self.__memoryAccesses

    def getMarked(self):
        return self.__marked


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setMemoryAccesses(self, memoryAccesses):
        self.__memoryAccesses = memoryAccesses

    def setMarked(self, marked):
        self.__marked = marked


    # FUNCTIONS
    def addMemoryAccess(self, page):
        tempMem = self.getMemoryAccesses()
        tempMem.append(page)
        self.setMemoryAccesses(tempMem)

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
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    #time.sleep(5)
                self.allocateInRam(newPage)
            else:
                memoryAccesses = list(reversed(self.getMemoryAccesses()))
                page2Remove = self.getRam().getMemory()[0]
                index = memoryAccesses.index(page2Remove)
                marked = [page2Remove, index]
                for page2Remove in self.getRam().getMemory():
                    index = memoryAccesses.index(page2Remove)
                    if index > marked[1]:
                        marked = [page2Remove, index]
                self.setMarked(marked[0])
                self.removeFromRam(marked[0])
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                    #time.sleep(5)
                self.allocateInRam(newPage)
                self.allocateInDisk(marked[0])
                self.addMemoryAccess(newPage)
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage)
            self.addMemoryAccess(newPage)