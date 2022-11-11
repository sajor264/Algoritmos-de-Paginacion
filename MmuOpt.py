from Optimal import Optimal
from Queue import Queue

class MmuOpt:

    def __init__(self, memCalls, pointersDic):
        self.setCurrentId(0)
        self.setTable({})
        self.setPointersDic(pointersDic)
        self.setAlgorithm(Optimal(self.getPageCalls(memCalls)))
    
    # GETTERS
    def getCurrentId(self):
        return self.__id

    def getTable(self):
        return self.__memory
    
    def getAlgorithm(self):
        return self.__algorithm  

    def getPointersDic(self):
        return self.__pointersDic   


    # SETTERS
    def setCurrentId(self, id):
        self.__id = id

    def setTable(self, memory):
        self.__memory = memory

    def setAlgorithm(self, algorithm):
        self.__algorithm = algorithm

    def setPointersDic(self, pointersDic):
        self.__pointersDic = pointersDic


    # FUNCTIONS
    def incrementId(self):
        tempId = self.getCurrentId()
        tempId += 1
        self.setCurrentId(tempId)
        return self.getCurrentId() - 1

    def addInTable(self, key, value):
        tempDic = self.getTable()
        tempDic[key] = value
        self.setTable(tempDic)

    def getPages(self, ptr, bytesSize):
        if ptr not in self.getTable():
            pagesList  = []
            kbSize = bytesSize/1024
            pagesList.append(self.incrementId())
            kbSize -= 4
            while(kbSize > 4):
                pagesList.append(self.incrementId())
                kbSize -= 4
            self.addInTable(ptr, pagesList)
            return pagesList
        else:
            return self.getTable()[ptr]

    def getPageCalls(self, memCalls):
        pageCalls = Queue()
        queue = memCalls
        while(not queue.isEmpty()):
            pointer  = queue.pop()
            pageCalls.queue(self.getPages(pointer, self.getPointersDic()[pointer]))
        return pageCalls

    def execute(self):
        self.getAlgorithm().allocateNext()

    

