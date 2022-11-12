from Lru import Lru
from Aging import Aging
from Random import Random
from SecondChance import SecondChance

class MmuAlg:

    def __init__(self, algorithm):
        self.setCurrentId(1)
        self.setState({})
        self.setTable({})
        self.setAlgorithm(algorithm)
    
    # GETTERS
    def getCurrentId(self):
        return self.__id

    def getTable(self):
        return self.__memory
    
    def getAlgorithm(self):
        return self.__algorithm  

    def getState(self):
        return self.__state  


    # SETTERS
    def setCurrentId(self, id):
        self.__id = id

    def setTable(self, memory):
        self.__memory = memory

    def setAlgorithm(self, algorithm):
        self.__algorithm = algorithm
    
    def setState(self, state):
        self.__state = state


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

    def removeFromTable(self, key):
        tempDic = self.getTable()
        del tempDic[key]
        self.setTable(tempDic)

    def killProcess(self, pointerList):
        for pointer in pointerList:
            for page in self.getTable()[pointer]:
                if page in self.getAlgorithm().getRam().getMemory():
                    self.getAlgorithm().getRam().removePage(page)
                if page in self.getAlgorithm().getDisk().getMemory():
                    self.getAlgorithm().getDisk().removePage(page)
            self.removeFromTable(pointer)

    def finish(self):
        tempRam = self.getAlgorithm().getRam().getMemory()
        tempTable = self.getTable()
        for page in tempRam:
            page = 0
        self.getAlgorithm().getRam().setMemory(tempRam)
        self.getAlgorithm().getDisk().setMemory([])
        self.setTable(tempTable)
    
    def addState(self, key ,value):
        tempDic = self.getState()
        tempDic[key] = value
        self.setTable(tempDic)
    
    def updateStateDisk(self, key, mADDR):
        tempDic = self.getState()
        list = tempDic[key]
        list[2] = False
        list[4] = -1
        list[5] = mADDR
        tempDic[key] = list
        self.setTable(tempDic)
         
    def getPages(self, ptr, bytesSize):
        if ptr not in self.getTable():
            pagesList  = []
            kbSize = bytesSize/1024
            pag = self.incrementId()
            data = [pag, ptr, False, pag, -1, -1, False]
            self.addState(pag, data)
            pagesList.append(pag )
            kbSize -= 4
            while(kbSize > 4):
                pag = self.incrementId()
                data = [pag, ptr, False, pag, -1, -1, False]
                self.addState(pag, data)
                pagesList.append(pag)
                kbSize -= 4
            self.addInTable(ptr, pagesList)
            return pagesList
        else:
            return self.getTable()[ptr]
    
    def execute(self, ptr, bytesSize):
        # data [PageID, PTR, LOADED, L-ADDR, M-ADDR, LOADED-T, MARK]
        algoritmo = self.getAlgorithm()
        pagesList  = self.getPages(ptr, bytesSize)
        for page in pagesList:
            if page in algoritmo.getRam().getMemory():
                algoritmo.allocate(page)
                lAddr = algoritmo.getRam().getMemory().index(page)
                data = [page, ptr, True, page, lAddr, -1, False]
                self.addState(page, data)
            else:
                algoritmo.allocate(page)
                lAddr = algoritmo.getRam().getMemory().index(page)
                data = [page, ptr, True, page, lAddr, -1, False]
                self.addState(page, data)
                disk = algoritmo.getDisk().getMemory()
                if len(disk) != 0:
                    pos = algoritmo.getDisk().getMemory().index(disk[-1])
                    self.updateStateDisk(disk[-1], pos)
           
            
        
      

    

