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
                    self.getAlgorithm().delPag(page)
                if page in self.getAlgorithm().getDisk().getMemory():
                    self.getAlgorithm().getDisk().removePage(page)
                self.rmvState(page)
            self.removeFromTable(pointer)
        self.getAlgorithm().addExecTime(10)

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
        self.setState(tempDic)

    def updateStateDisk(self, key, mADDR, time):
        tempDic = self.getState()
        list = tempDic[key]
        list[2] = False
        list[3] = -1
        list[4] = mADDR
        list[5] = time
        tempDic[key] = list
        self.setState(tempDic)
    
    def rmvState(self, key):
        tempDic = self.getState()
        del(tempDic[key])
        self.setState(tempDic)
    
         
    def getPages(self, ptr, bytesSize):
        if ptr not in self.getTable():
            pagesList  = []
            kbSize = bytesSize/1024
            pag = self.incrementId()
            data = [pag, ptr, False, -1, -1, -1, False]
            self.addState(pag, data)
            pagesList.append(pag )
            kbSize -= 4
            while(kbSize > 4):
                pag = self.incrementId()
                data = [pag, ptr, False, -1, -1, -1, False]
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
                time = algoritmo.getExecTime()
                algoritmo.allocate(page)
                lAddr = algoritmo.getRam().getMemory().index(page)
                data = [page, ptr, True, lAddr, -1 ,time, False]
                self.addState(page, data)
            elif algoritmo.getRam().isFull() and page not in algoritmo.getRam().getMemory():
                if 0 in algoritmo.getRam().getMemory():
                    time = algoritmo.getExecTime()
                    algoritmo.allocate(page)
                    lAddr = algoritmo.getRam().getMemory().index(page)
                    data = [page, ptr, True, lAddr, -1 ,time, False]
                    self.addState(page, data)
                else:
                    time = algoritmo.getExecTime()
                    algoritmo.allocate(page)
                    lAddr = algoritmo.getRam().getMemory().index(page)
                    data = [page, ptr, True, lAddr, -1 ,time, False]
                    self.addState(page, data)
                    # page in disk
                    disk = algoritmo.getDisk().getMemory()
                    timeDisk = algoritmo.getExecTime()
                    pos = algoritmo.getDisk().getMemory().index(disk[-1])
                    self.updateStateDisk(disk[-1], pos, timeDisk) 
            else:
                time = algoritmo.getExecTime()
                algoritmo.allocate(page)
                lAddr = algoritmo.getRam().getMemory().index(page)
                data = [page, ptr, True, lAddr, -1 , time, False]
                self.addState(page, data)    
        
      

    

