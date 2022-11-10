from Mmu import Mmu
from Ram import Ram

class Lru:

    def __init__(self):
        self.setMmu(Mmu())
        self.setRam(Ram())
        self.setMemoryAccesses([])
    
    # GETTERS
    def getMmu(self):
        return self.__mmu

    def getRam(self):
        return self.__ram
    
    def getMemoryAccesses(self):
        return self.__memoryAccesses


    # SETTERS
    def setMmu(self, mmu):
        self.__mmu = mmu

    def setRam(self, ram):
        self.__ram = ram

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