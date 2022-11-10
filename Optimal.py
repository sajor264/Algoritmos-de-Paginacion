from Mmu import Mmu
from Ram import Ram

class Optimal:

    def __init__(self, memCalls):
        self.setMemCalls(memCalls)
        self.setMmu(Mmu())
        self.setRam(Ram())
    
    # GETTERS
    def getMemCalls(self):
        return self.__memCalls

    def getMmu(self):
        return self.__mmu

    def getRam(self):
        return self.__ram


    # SETTERS
    def setMemCalls(self, memCalls):
        self.__memCalls = memCalls

    def setMmu(self, mmu):
        self.__mmu = mmu

    def setRam(self, ram):
        self.__ram = ram


    # FUNCTIONS
    def getNextMemCall(self):
        tempQueue = self.getMemCalls()
        element = tempQueue.pop()
        self.setMemCalls(tempQueue)
        return element

    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def allocateNext(self):
        if self.getRam().isFull():
            restOfMemCalls = self.getMemCalls().getQueue()
            page2Remove = self.getRam().getMemory()[0]
            index = restOfMemCalls.index(page2Remove)
            marked = [page2Remove, index]
            for page2Remove in self.getRam().getMemory():
                index = restOfMemCalls.index(page2Remove)
                if index > marked[1]:
                    marked = [page2Remove, index]
            self.removeFromRam(marked[0])
            self.allocateInRam(self.getNextMemCall())
        else:
            self.allocateInRam(self.getNextMemCall())