from Ram import Ram
from Disk import Disk

class Optimal:

    def __init__(self, memCalls):
        self.setMemCalls(memCalls)
        self.setRam(Ram())
        self.setDisk(Disk())
        self.setData({})
        self.setExecTime(0)

    
    # GETTERS
    def getMemCalls(self):
        return self.__memCalls

    def getRam(self):
        return self.__ram

    def getDisk(self):
        return self.__disk

    def getExecTime(self):
        return self.__execTime

    def getData(self):
        return self.__data

    # SETTERS
    def setMemCalls(self, memCalls):
        self.__memCalls = memCalls

    def setRam(self, ram):
        self.__ram = ram

    def setDisk(self, disk):
        self.__disk = disk

    def setExecTime(self, execTime):
        self.__execTime = execTime
    
    def setData(self,data):
        self.__data = data
    
    

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

    def removeFromDisk(self, page):
        self.getDisk().removePage(page)

    def allocateInDisk(self, page):
        self.getDisk().allocatePage(page)

    def addExecTime(self, time):
        tempExecTime = self.getExecTime()
        tempExecTime += time
        self.setExecTime(tempExecTime)
    
    def updateDataRam(self, key ,lADDR, time):
        tempDic = self.getData()
        list = tempDic[key]
        list[2] = True
        list[4] = lADDR
        list[5] = -1
        list[6] = time
        tempDic[key] = list
        self.setData(tempDic)

    def updateDataDisk(self, key, mADDR, time):
        tempDic = self.getData()
        list = tempDic[key]
        list[2] = False
        list[4] = -1
        list[5] = mADDR
        list[6] = time
        tempDic[key] = list
        self.setData(tempDic)
    
    def allocateNext(self):
        for page in self.getNextMemCall():
            self.addExecTime(1)
            if self.getRam().isFull() and page not in self.getRam().getMemory():
                if 0 in self.getRam().getMemory():
                    if(page in self.getDisk().getMemory()):
                        self.removeFromDisk(page)
                        #time.sleep(5)
                    tim = self.getExecTime()
                    self.allocateInRam(page)
                    lAddr = self.getRam().getMemory().index(page)
                    self.updateDataRam(page, lAddr, tim)
                else:
                    restOfMemCalls = self.getMemCalls().getQueue()
                    index = -1
                    marked = [-1, index]
                    for page2Remove in self.getRam().getMemory():
                        found = False
                        for restPage in restOfMemCalls:
                            if page2Remove in restPage:
                                index = restOfMemCalls.index(restPage)
                                found = True
                        if index > marked[1]:
                            marked = [page2Remove, index]
                        if not found:
                            marked = [page2Remove, index]
                            break
                    self.removeFromRam(marked[0])
                    if(page in self.getDisk().getMemory()):
                        self.removeFromDisk(page)
                        #time.sleep(5)
                    tim = self.getExecTime()
                    self.allocateInRam(page)
                    lAddr = self.getRam().getMemory().index(page)
                    self.updateDataRam(page, lAddr, tim)
                    # disk
                    self.allocateInDisk(marked[0])
                    timeDisk = self.getExecTime() 
                    pos = self.getDisk().getMemory().index(marked[0])
                    self.updateDataDisk(marked[0], pos, timeDisk) 
                self.addExecTime(5)
            elif page not in self.getRam().getMemory():
                tim = self.getExecTime()
                self.allocateInRam(page)
                lAddr = self.getRam().getMemory().index(page)
                self.updateDataRam(page, lAddr, tim)
                self.addExecTime(5)
            