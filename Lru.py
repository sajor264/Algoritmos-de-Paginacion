from Ram import Ram
from Disk import Disk

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


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setMemoryAccesses(self, memoryAccesses):
        self.__memoryAccesses = memoryAccesses


    # FUNCTIONS
    def addMemoryAccess(self, page):
        tempMem = self.getMemoryAccesses()
        tempMem.append(page)
        self.setMemoryAccesses(tempMem)

    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def allocate(self, newPage):

        if self.getRam().isFull():
            memoryAccesses = list(reversed(self.getMemoryAccesses()))
            page2Remove = self.getRam().getMemory()[0]
            index = memoryAccesses.index(page2Remove)
            marked = [page2Remove, index]
            for page2Remove in self.getRam().getMemory():
                index = memoryAccesses.index(page2Remove)
                if index > marked[1]:
                    marked = [page2Remove, index]
            self.removeFromRam(marked[0])
            self.allocateInRam(newPage)
            self.addMemoryAccess(newPage)
        else:
            self.allocateInRam(newPage)
            self.addMemoryAccess(newPage)