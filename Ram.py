class Ram:

    def __init__(self):
        self.setFreeRam(400)
        self.setMemory([])
    
    # GETTERS
    def getFreeRam(self):
        return self.__maxSize

    def getMemory(self):
        return self.__memory


    # SETTERS
    def setFreeRam(self, maxSize):
        self.__maxSize = maxSize

    def setMemory(self, memory):
        self.__memory = memory


    # FUNCTIONS
    def isFull(self):
        return self.getFreeRam() <= 0

    def allocatePage(self, page):
        tempFreeRam = self.getFreeRam()
        tempMem = self.getMemory()
        tempFreeRam -= 4
        tempMem.append(page)
        self.setFreeRam(tempFreeRam)
        self.setMemory(tempMem)
    
    def removePage(self, page):
        tempFreeRam = self.getFreeRam()
        tempMem = self.getMemory()
        tempFreeRam += 4
        tempMem.remove(page)
        self.setFreeRam(tempFreeRam)
        self.setMemory(tempMem)
