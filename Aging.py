from Ram import Ram
from Disk import Disk

class Aging:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setClock({})
        self.setExecTime(0)
        self.setThrashingTime(0)
        self.setState({})
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk
    
    def getClock(self):
        return self.__clock
    
    def getExecTime(self):
        return self.__execTime

    def getThrashingTime(self):
        return self.__thrashingTime

    def getState(self):
        return self.__state

    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setClock(self, clock):
        self.__clock = clock
    
    def setExecTime(self, execTime):
        self.__execTime = execTime

    def setThrashingTime(self, thrashingTime):
        self.__thrashingTime = thrashingTime

    def setState(self, state):
        self.__state = state

    # FUNCTIONS
    def addState(self,key,value):
        tempDic = self.getState()
        tempDic[key] = value
        self.setState(tempDic)
    
    def rmvState(self, key):
        tempDic = self.getState()
        del(tempDic[key])
        self.setState(tempDic)

    def addInClock(self, key, value):
        tempDic = self.getClock()
        tempDic[key] = value
        self.setClock(tempDic)

    def removeFromRam(self, page):
        self.addExecTime(1)
        self.getRam().removePage(page)

    def allocateInRam(self, page, pid):
        self.addExecTime(1)
        self.getRam().allocatePage(page)
        data = [page, pid, True, page, self.getRam().getMemory().index(page), -1, self.getExecTime(), False]
        self.addState(page, data)

    def removeFromDisk(self, page):
        self.addExecTime(5)
        self.addThrashingTime(5)
        self.getDisk().removePage(page)
    
    def allocateInDisk(self, page, pid):
        self.addExecTime(5)
        self.addThrashingTime(5)
        self.getDisk().allocatePage(page)
        data = [page, pid, False, page, -1, self.getDisk().getMemory().index(page), self.getExecTime(), False]
        self.addState(page, data)
    
    def righBits(self): 
        tempDic = self.getClock()
        for var in tempDic:
            bits = tempDic[var] 
            tempDic[var] = "0"+ bits[:7]
        self.setClock(tempDic)

    def delPag(self, page):
        tempDic = self.getClock()
        del(tempDic[page])
        self.setClock(tempDic)

    def pagInRam(self, page):
        tempDic = self.getClock()
        bits = tempDic[page] 
        del(tempDic[page])
        tempDic[page] = "1"+ bits[:7]
        self.setClock(tempDic)
    
    def addExecTime(self, time):
        tempExecTime = self.getExecTime()
        tempExecTime += time
        self.setExecTime(tempExecTime)
    
    def addThrashingTime(self, time):
        tempTime = self.getThrashingTime()
        tempTime += time
        self.setThrashingTime(tempTime)
    
    def binario_a_decimal(self, numero_binario):
	    numero_decimal = 0 
	    for posicion, digito_string in enumerate(numero_binario[::-1]):
		    numero_decimal += int(digito_string) * 2 ** posicion
	    return numero_decimal

    def selectPag(self):
        tempDic = self.getClock()
        pagAging = 0
        varPag = 9999999999
        for var in tempDic:
            bits = tempDic[var]
            varPagCur = self.binario_a_decimal(bits)
            if varPagCur <= varPag:
                varPag = varPagCur
                pagAging = var
        del(tempDic[pagAging])
        self.setClock(tempDic)
        return pagAging
    
    def delRegister(self, pag):
        dic = self.getClock()
        del(dic[pag])
        self.setClock(dic)
    
    def allocate(self, newPage, pid):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                self.allocateInRam(newPage, pid)
                self.addInClock(newPage, "10000000")
                self.righBits()
            else:
                pagDisk = self.selectPag()
                self.removeFromRam(pagDisk)
                self.allocateInDisk(pagDisk, pid)
                ## disco
                self.allocateInRam(newPage, pid)
                self.addInClock(newPage, "10000000")
                self.righBits()      
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage, pid)
            self.addInClock(newPage, "10000000")
            self.righBits()

        elif newPage  in self.getRam().getMemory():
            self.pagInRam(newPage)
            self.righBits()
         