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
        tempFreeRam -= 4
        self.setFreeRam(tempFreeRam)
        tempMem = self.getMemory()
        if len(tempMem) < 100:
            tempMem.append(page)
        else:
            index = tempMem.index(0)
            tempMem.remove(0)
            tempMem.insert(index, page)
        self.setMemory(tempMem)
    
    def removePage(self, page):
        tempFreeRam = self.getFreeRam()
        tempMem = self.getMemory()
        tempFreeRam += 4
        index = tempMem.index(page)
        tempMem.remove(page)
        tempMem.insert(index, 0)
        self.setFreeRam(tempFreeRam)
        self.setMemory(tempMem)
