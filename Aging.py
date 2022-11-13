from Ram import Ram
from Disk import Disk

class Aging:

    def __init__(self):
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setClock({})
        self.setExecTime(0)
    
    # GETTERS
    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk
    
    def getClock(self):
        return self.__clock
    
    def getExecTime(self):
        return self.__execTime

   

    # SETTERS
    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setClock(self, clock):
        self.__clock = clock
    
    def setExecTime(self, execTime):
        self.__execTime = execTime

    # FUNCTIONS
    def addInClock(self, key, value):
        tempDic = self.getClock()
        tempDic[key] = value
        self.setClock(tempDic)

    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def removeFromDisk(self, page):
        self.getDisk().removePage(page)
    
    def allocateInDisk(self, page):
        self.getDisk().allocatePage(page)
    

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
    
    def delRegister(sef, pag):
        dic = sef.getClock()
        del(dic[pag])
        self.setClock(dic)
    
    def allocate(self, newPage):
        if self.getRam().isFull() and newPage not in self.getRam().getMemory():
            if 0 in self.getRam().getMemory():
                if(newPage in self.getDisk().getMemory()):
                    self.removeFromDisk(newPage)
                self.allocateInRam(newPage)
                self.addInClock(newPage, "10000000")
                self.righBits()
            else:
                pagDisk = self.selectPag()
                self.removeFromRam(pagDisk)
                self.allocateInDisk(pagDisk)
                ## disco
                self.allocateInRam(newPage)
                self.addInClock(newPage, "10000000")
                self.righBits()
                
        elif newPage not in self.getRam().getMemory():
            self.allocateInRam(newPage)
            self.addInClock(newPage, "10000000")
            self.righBits()

        elif newPage  in self.getRam().getMemory():
            self.pagInRam(newPage)
            self.righBits()
         