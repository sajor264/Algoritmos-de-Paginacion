class Process:

    def __init__(self, memQuantity, execTime):
        self.setMemQuantity(memQuantity)
        self.setExecTime(execTime)
        self.setHeap({})


    # GETTERS
    def getMemQuantity(self):
        return self.__memQuantity

    def getExecTime(self):
        return self.__execTime
    
    def getHeap(self):
        return self.__heap


    # SETTERS
    def setMemQuantity(self, memQuantity):
        self.__memQuantity = memQuantity

    def setExecTime(self, execTime):
        self.__execTime = execTime

    def setHeap(self, heap):
        self.__heap = heap

    def addToHeap(self, memQuantity):
        tempDic = self.getHeap()
        tempDic[str(len(tempDic))] = memQuantity
        self.setHeap(tempDic)

    def removeFromHeap(self, heapKey):
        tempDic = self.getHeap()
        del tempDic[heapKey]
        self.setHeap(tempDic)
