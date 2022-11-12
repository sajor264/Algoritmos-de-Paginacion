import random
import time
import numpy as np
import matplotlib.pyplot as plt
import copy
from Queue import Queue
from matplotlib.lines import Line2D
from MmuAlg import MmuAlg
from MmuOpt import MmuOpt
from Optimal import Optimal
from Lru import Lru
from Aging import Aging
from Random import Random
from SecondChance import SecondChance

# KEY: PID, VALUE: PROCESS POINTERS
processesDic = {}
processes2Remove = {}

# KEY: PTR, VALUE: SIZE
pointersDic = {}

#ORDEN DE LAS LLAMADAS A MEMORIA
memCalls = Queue()


def readFile(fileName):
    allProcesses = []

    file = open(fileName, "r")
    for line in file:
        tempList = []
        for e in line.split(','):
            tempList.append(e.lstrip().rstrip())
        allProcesses.append(tempList)
    file.close()

    return allProcesses[1:]


def createProcesses(allProcesses):
    tempMemCalls = []
    for process in allProcesses:
        pointersDic[str(process[1])] = int(process[2])
        tempMemCalls.append(process[1])
        if process[0] in processesDic:
            tempList = processesDic[process[0]]
            tempList.append(process[1])
            processesDic[process[0]] = tempList
        else:
            processesDic[process[0]] = [process[1]]
    tempMemCalls.extend(random.choices(tempMemCalls, k=len(tempMemCalls)))
    random.shuffle(tempMemCalls)
    memCalls.setQueue(tempMemCalls)


def killProcess(ptr, mmuOpt, mmuAlg):
    del pointersDic[ptr]
    key = [i for i in processes2Remove if ptr in processes2Remove[i]]
    key = key[0]
    tempList = processes2Remove[key]
    if len(tempList) == 1:
        mmuAlg.killProcess(processesDic[key])
        mmuOpt.killProcess(processesDic[key])
        del processes2Remove[key]
        del processesDic[key]
    else:
        tempList.remove(ptr)
        processes2Remove[key] = tempList

def finish(mmuOpt, mmuAlg):
    processesDic.clear()
    processes2Remove.clear()
    pointersDic.clear()
    mmuAlg.finish()
    mmuOpt.finish()




if __name__ == '__main__':
    # INPUTS
    fileName = str(input("Nombre del archivo de procesos: "))
    seed = int(input("Semilla: "))
    algorithm = int(input("0) LRU\n1) Second Chance\n2) Aging\n3)Random\nAlgoritmo: "))

    # OBTIENE LOS PROCESOS Y LOS BARAJA
    random.seed(seed)
    allProcesses  = readFile(fileName)
    createProcesses(allProcesses)

    # VARIABLES
    processes2Remove = copy.deepcopy(processesDic)
    finished = False
    memCallsCpy = Queue()
    memCallsCpy.setQueue(list(reversed(memCalls.getQueue())).copy())
    mmuOpt = MmuOpt(memCallsCpy, pointersDic)
    if algorithm == 0:
        mmuAlg = MmuAlg(Lru())
    if algorithm == 1:
        mmuAlg = MmuAlg(SecondChance())
    if algorithm == 2:
        mmuAlg = MmuAlg(Aging())
    if algorithm == 3:
        mmuAlg = MmuAlg(Random())

    while(not finished):
        currentPointer = memCalls.pop()

        #EJECUTAMOS ALGORITMOS
        mmuOpt.execute()
        mmuAlg.execute(currentPointer, pointersDic[currentPointer])

        # VERIFICA SI TERMINO EL PROCESO ACUTAL
        if(not memCalls.isIn(currentPointer)):
            killProcess(currentPointer, mmuOpt, mmuAlg)
        
        # VERIFICA SI TERMINARON TODOS LOS PROCESOS
        if(memCalls.isEmpty()):
            finish(mmuOpt, mmuAlg)
            finished = True

        print("\n\n\n")
        # print(mmuOpt.getAlgorithm().getMemCalls().getQueue())
        # print(mmuAlg.getAlgorithm().getRam().getFreeRam())
        print(len(mmuOpt.getAlgorithm().getDisk().getMemory()))
        print("------------------------------OPTIMO------------------------------")
        print(mmuOpt.getAlgorithm().getRam().getMemory())
        print(mmuOpt.getAlgorithm().getDisk().getMemory())
        print("-----------------------------ALGORITMO-----------------------------")
        print(mmuAlg.getAlgorithm().getRam().getMemory())
        print(mmuAlg.getAlgorithm().getDisk().getMemory())
    
        time.sleep(0.00001)
        
    print("FINISHED")