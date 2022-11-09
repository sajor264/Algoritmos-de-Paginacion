from Mmu import Mmu

class Optimal:

    def __init__(self, memCalls):
        self.setMemCalls(memCalls)
        self.setMmu(Mmu())
        self.setHardDrive([])
        self.setAllocatedMemory([])
        self.setMemoryAccesses([])
    
    # GETTERS
    def getMemCalls(self):
        return self.__memCalls

    def getMmu(self):
        return self.__mmu

    def getHardDrive(self):
        return self.__hardDrive

    def getAllocatedMemory(self):
        return self.__allocatedMemory

    def getMemoryAccesses(self):
        return self.__memoryAccesses


    # SETTERS
    def setMemCalls(self, memCalls):
        self.__memCalls = memCalls

    def setMmu(self, mmu):
        self.__mmu = mmu

    def setHardDrive(self, hardDrive):
        self.__hardDrive = hardDrive

    def setAllocatedMemory(self, allocatedMemory):
        self.__allocatedMemory = allocatedMemory

    def setMemoryAccesses(self, memoryAccesses):
        self.__memoryAccesses = memoryAccesses


    # FUNCTIONS
    def allocateNext(self):