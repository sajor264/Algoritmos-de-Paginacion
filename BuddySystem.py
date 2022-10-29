class BuddySystem:

    def __init__(self, memorySize):
        # BLOCK = ['E' for empty or 'P' for process, startPos, blockSize]
        self.setMemory([['E', 0, memorySize]])
        self.setMemorySize(memorySize)
        self.setRefusedProcesses([])
        self.setBlockBrothers({})
    
    # GETTERS
    def getMemory(self):
        return self.__memory

    def getRefusedProcesses(self):
        return self.__refusedProcesses

    def getMemorySize(self):
        return self.__memorySize

    def getBlockBrothers(self):
        return self.__blockBrothers


    # SETTERS
    def setMemory(self, memory):
        self.__memory = memory

    def setRefusedProcesses(self, refusedProcesses):
        self.__refusedProcesses = refusedProcesses

    def setMemorySize(self, memorySize):
        self.__memorySize = memorySize

    def setBlockBrothers(self, blockBrothers):
        self.__blockBrothers = blockBrothers


    # FUNCTIONS
    def allocate(self, processName, processBlockSize):
        if(processName not in self.getRefusedProcesses()):
            isAsigned = False
            processBlockSize = self.getIdealSize(processBlockSize)

            for block in self.getMemory():
                if(block[0] == 'E' and not isAsigned):
                    if(block[2] == processBlockSize):
                        newBlock = []
                        index = self.getMemory().index(block)
                        newBlock.append(processName)
                        newBlock.append(block[1])
                        newBlock.append(processBlockSize)
                        self.insertInMemory(index, newBlock)
                        isAsigned = True
                        break
                    elif(block[2] > processBlockSize):
                        while(not isAsigned):
                            newBlock = []
                            index = self.getMemory().index(block)
                            newBlock.append('E')
                            newBlock.append(block[1])
                            newBlock.append(int(block[2]/2))
                            self.insertInMemory(index, newBlock)
                            block = newBlock
                            if(block[2] == processBlockSize):
                                newBlock = []
                                index = self.getMemory().index(block)
                                newBlock.append(processName)
                                newBlock.append(block[1])
                                newBlock.append(processBlockSize)
                                self.insertInMemory(index, newBlock)
                                isAsigned = True
                        break
            tempMem = list(reversed(self.getMemory()))
            changes = True                            
            while(changes):
                toRemove = []
                changes = False
                for i in range(len(tempMem) - 1):
                    suma = tempMem[i][2] + tempMem[i + 1][2]
                    if(tempMem[i][0] == 'E' and tempMem[i + 1][0] == 'E' and suma == self.getIdealSize(suma)):
                        tempMem[i][1] = tempMem[i + 1][1] 
                        tempMem[i][2] += tempMem[i + 1][2]
                        toRemove.append(tempMem[i + 1])
                        changes = True
                for e in toRemove:
                    tempMem.remove(e)
            self.setMemory(list(reversed(tempMem)))
            if not isAsigned:
                self.killProcess(processName)
                self.addRefusedProcess(processName)
            
    def getIdealSize(self, blockSize):
        potencia = 0
        res = 2 ** potencia
        while(res < blockSize):
            potencia += 1
            res = 2 ** potencia
        return res

    def addRefusedProcess(self, refusedProcess):
        tempList = self.getRefusedProcesses()
        tempList.append(refusedProcess)
        self.setRefusedProcesses(tempList)
    
    def removeFromMemory(self, e):
        tempMem = self.getMemory()
        index = tempMem.index(e)
        changes = True

        tempMem[index][0] = 'E'
        while(changes):
            toRemove = []
            changes = False
            for i in range(len(tempMem) - 1):
                if(tempMem[i][0] == 'E' and tempMem[i + 1][0] == 'E' and self.getBrother(tempMem[i]) == tempMem[i + 1]):
                    tempDic = self.getBlockBrothers()
                    del tempDic[str(tempMem[i])]
                    self.setBlockBrothers(tempDic)
                    tempMem[i + 1][1] = tempMem[i][1] 
                    tempMem[i + 1][2] += tempMem[i][2]
                    toRemove.append(tempMem[i])
                    changes = True
            for e in toRemove:
                tempMem.remove(e)    
        self.setMemory(tempMem)

    def insertInMemory(self, index, e):
        tempBlock = self.getMemory()[index]
        tempMem = self.getMemory()
        tempMem.insert(index, e)
        tempMem.remove(tempBlock)
        if(tempBlock[2] > 0 and (tempBlock[2] - e[2]) > 0):
            newBlock = ['E', e[1] + e[2], tempBlock[2] - e[2]]
            tempMem.insert(index + 1, newBlock)
            tempBrothersDic = self.getBlockBrothers()
            e[0] = 'E'
            tempBrothersDic[str(e)] =  newBlock
            self.setBlockBrothers(tempBrothersDic)
        self.setMemory(tempMem)

    def getMemStatus(self):
        quantity = 0
        freeMem = 0
        for segment in self.getMemory():
            if(segment[0] == 'E'):
                quantity += 1
                freeMem += segment[2]
        return quantity, freeMem

    def killProcess(self, processName):
        currentMemory = self.getMemory()
        toRemove = [block for block in currentMemory if block[0] == processName]
        for block in toRemove:
            self.removeFromMemory(block)

    def removeHeapFromMemory(self, processName, heapSize):
        if(processName not in self.getRefusedProcesses()):
            e = self.searchBlock(processName, heapSize)
            if(e):
                self.removeFromMemory(e)

    def searchBlock(self, processName, heapSize):
        heapSize = self.getIdealSize(heapSize)
        for block in list(reversed(self.getMemory())):
            if(block[0] == processName and block[2] == heapSize):
                return block
        return False

    def finish(self):
        self.setMemory([['E', 0, self.getMemorySize()]])
        self.setBlockBrothers({})
    
    def getBrother(self, block):
        if(str(block) in self.getBlockBrothers()):
            return self.getBlockBrothers()[str(block)]
        else:
            return 0

    def getDataToDraw(self):
        dataArray = []
        process = []
        for x in self.getMemory():
            dataArray.append([0,0,0,x[2]])
            process.append(x[0])
        return dataArray, process