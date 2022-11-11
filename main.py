import random
import time
import numpy as np
import matplotlib.pyplot as plt
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

# KEY: PTR, VALUE: SIZE
pointersDic = {}

#ORDEN DE LAS LLAMADAS A MEMORIA
memCalls = Queue()

# colors=[]
# for i in range(100):
#     r = lambda: random.randint(15,255)
#     color='#%02X%02X%02X' % (r(),r(),r())
#     while color in colors:
#         color='#%02X%02X%02X' % (r(),r(),r())
#     colors.append(color)
# colors.append('#%02X%02X%02X' % (0,0,0))

# def draw(choice):
#     if(choice != 2):
#         dataArray, process = firstFit.getDataToDraw()
#         dataBest, processBest =  bestFit.getDataToDraw()
#         dataWorst, processWorst =  worstFit.getDataToDraw()
#         dataBuddy, processBuddy =  buddySystem.getDataToDraw()

#         dataArray.extend(dataBest) 
#         dataArray.extend(dataWorst) 
#         dataArray.extend(dataBuddy) 
         
#         process.extend(processBest) 
#         process.extend(processWorst) 
#         process.extend(processBuddy) 

#         data = np.array(dataArray)
#         tcks = np.arange(20)
#         X = np.arange(data.shape[1])
#         for i in range(data.shape[0]):
#             if process[i] == 'E':
#                 color = colors[100]
#             else:
#                 color = colors[int(process[i])]
#             bot = np.sum(data[:i], axis = 0)
#             plt.bar(X, data[i],bottom = bot,color = color)
        
#         quantityFirst, freeMemFirst = firstFit.getMemStatus()
#         quantityBest, freeMemBest = bestFit.getMemStatus()
#         quantityWorst, freeMemWorst = worstFit.getMemStatus()
#         quantityBuddy, freeMemBuddy = buddySystem.getMemStatus()        
#         textFirst = plt.gcf().text(0.08, 0.91, "Algoritmo: First Fit \nMemoria disponible: " + str(freeMemFirst) + "\nSegmentos disponibles: "+str(quantityFirst) +"\nProcesos rechazados: "+ str(len(firstFit.getRefusedProcesses())) , fontsize=10)
#         textBest = plt.gcf().text(0.2, 0.91, "Algoritmo: Best Fit \nMemoria disponible: " + str(freeMemBest) + "\nSegmentos disponibles: "+str(quantityBest) +"\nProcesos rechazados: "+ str(len(bestFit.getRefusedProcesses())) , fontsize=10)
#         textWorst = plt.gcf().text(0.32, 0.91, "Algoritmo: Worst Fit \nMemoria disponible: " + str(freeMemWorst) + "\nSegmentos disponibles: "+str(quantityWorst) +"\nProcesos rechazados: "+ str(len(worstFit.getRefusedProcesses())) , fontsize=10)
#         textBuddy = plt.gcf().text(0.45, 0.91, "Algoritmo: Buddy System \nMemoria disponible: " + str(freeMemBuddy) + "\nSegmentos disponibles: "+str(quantityBuddy) +"\nProcesos rechazados: "+ str(len(buddySystem.getRefusedProcesses())) , fontsize=10)

#         plt.pause(0.1)
#         textFirst.remove()
#         textBest.remove()
#         textWorst.remove()
#         textBuddy.remove()


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
    tempMemCalls.extend(random.choices(tempMemCalls, k=len(tempMemCalls)*100))
    random.shuffle(tempMemCalls)
    memCalls.setQueue(tempMemCalls)


def killProcess(ptr):
    del pointersDic[ptr]
    key = [i for i in processesDic if ptr in processesDic[i]]
    key = key[0]
    tempList = processesDic[key]
    if len(processesDic[key]) == 1:
        del processesDic[key]
    else:
        tempList = processesDic[key]
        tempList.remove(ptr)
        processesDic[key] = tempList


if __name__ == '__main__':
    # INPUTS
    fileName = str(input("Nombre del archivo de procesos: "))
    seed = int(input("Semilla: "))
    algorithm = int(input("0) LRU\n1) Second Chance\n2) Aging\n3)Random\nAlgoritmo: "))

    # OBTIENE LOS PROCESOS Y LOS BARAJA
    allProcesses  = readFile(fileName)
    createProcesses(allProcesses)

    # VARIABLES
    random.seed(seed)
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
   
    # custom_lines1 = [Line2D([0], [0], color=colors[x], lw=4) for x in range(25)]
    # custom_lines2 = [Line2D([0], [0], color=colors[x], lw=4) for x in range(25,50)]
    # custom_lines3 = [Line2D([0], [0], color=colors[x], lw=4) for x in range(50,75)]
    # custom_lines4 = [Line2D([0], [0], color=colors[x], lw=4) for x in range(75,100)]
    
    # fig, ax = plt.subplots()
    # legend1 = plt.legend(custom_lines1, ["P"+str(x) for x in range(25)],loc='upper left', bbox_to_anchor=(1, 1))
    # legend2 = plt.legend(custom_lines2, ["P"+str(x) for x in range(25,50)],loc='upper left', bbox_to_anchor=(1.1, 1))
    # legend3 = plt.legend(custom_lines3, ["P"+str(x) for x in range(50,75)],loc='upper left', bbox_to_anchor=(1.2, 1))
    # legend4 = plt.legend(custom_lines4, ["P"+str(x) for x in range(75,100)],loc='upper left', bbox_to_anchor=(1.3, 1))
    # legendRam = plt.legend([Line2D([0], [0], color=colors[100], lw=4)], ["RAM"],loc='lower left', bbox_to_anchor=(1, 1))
    
    # #plt.figure()
    # ax.add_artist(legend1)
    # ax.add_artist(legend2)
    # ax.add_artist(legend3)
    # ax.add_artist(legend4)
    # ax.add_artist(legendRam)
    
    # plt.subplots_adjust(left=0.05,right=0.57, bottom=0.21)
    # plt.get_current_fig_manager().full_screen_toggle() 

    while(not finished):
        currentPointer = memCalls.pop()

        #EJECUTAMOS ALGORITMOS
        mmuOpt.execute()
        mmuAlg.execute(currentPointer, pointersDic[currentPointer])

        print(mmuOpt.getAlgorithm().getRam().getMemory())
        print(mmuOpt.getAlgorithm().getDisk().getMemory())
        print("------------------------------------------------------")
        print(mmuAlg.getAlgorithm().getRam().getMemory())
        print(mmuAlg.getAlgorithm().getDisk().getMemory())
        print("------------------------------------------------------")
        print("------------------------------------------------------")
        print("------------------------------------------------------")

        # VERIFICA SI TERMINO EL PROCESO ACUTAL
        if(not memCalls.isIn(currentPointer)):
            killProcess(currentPointer)
        
        # VERIFICA SI TERMINARON TODOS LOS PROCESOS
        if(memCalls.isEmpty()):
            finished = True
    
        # draw(choice)
        time.sleep(1)
        
    # plt.show()
    print("FINISHED")