import random
import time
import copy
from Queue import Queue
from MmuAlg import MmuAlg
from MmuOpt import MmuOpt
from Optimal import Optimal
from Lru import Lru
from Aging import Aging
from Random import Random
from SecondChance import SecondChance
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# KEY: PID, VALUE: PROCESS POINTERS
processesDic = {}
processes2Remove = {}
# KEY: PTR, VALUE: SIZE
pointersDic = {}
#ORDEN DE LAS LLAMADAS A MEMORIA
memCalls = Queue()

colors=["#FFFFFF"]
for i in range(1,30):
    r = lambda: random.randint(15,255)
    color='#%02X%02X%02X' % (r(),r(),r())
    while color in colors:
        color='#%02X%02X%02X' % (r(),r(),r())
    colors.append(color)
    

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
    tempMemCalls.extend(random.choices(tempMemCalls, k=len(tempMemCalls)*10))
    random.shuffle(tempMemCalls)
    memCalls.setQueue(tempMemCalls)

def getData(mmuAlg):
    data = []
    process = []
    loaded = []
    unloaded = []
    dic = mmuAlg.getState()
    for pag in dic: 
        list = dic[pag] 
        if list[1] not in process:
            process.append(list[1])
        
        if list[2] == True:
            loaded.append(pag)
        else:
            unloaded.append(pag)
    
    data.append(len( process))
    data.append(mmuAlg.getAlgorithm().getExecTime())
    data.append(len(loaded)*4)
    data.append(len(loaded)*4*100/400)
    data.append(len(unloaded)*4)
    data.append(len(unloaded)*4*100/1000)
    data.append(len(loaded))
    data.append(len(unloaded))
    return data

def getIDP(ptr):
    for IDP in processesDic:
        if ptr in processesDic[IDP]:
            return IDP
    return 0

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

def updateOptSlider(val):
    print(val)

def updateAlgSlider(val):
    print(val)


if __name__ == '__main__':
    # INPUTS
    #fileName = str(input("Nombre del archivo de procesos: "))
    seed = int(input("Semilla: "))
    algorithm = int(input("0) LRU\n1) Second Chance\n2) Aging\n3)Random\nAlgoritmo: "))
    # OBTIENE LOS PROCESOS Y LOS BARAJA
    random.seed(seed)
    allProcesses  = readFile('procesos.txt')
    createProcesses(allProcesses)
    # VARIABLES
    processes2Remove = copy.deepcopy(processesDic)
    finished = False
    memCallsCpy = Queue()
    memCallsCpy.setQueue(list(reversed(memCalls.getQueue())).copy())
    mmuOpt = MmuOpt(memCallsCpy, pointersDic, processesDic)
    if algorithm == 0:
        mmuAlg = MmuAlg(Lru())
    if algorithm == 1:
        mmuAlg = MmuAlg(SecondChance())
    if algorithm == 2:
        mmuAlg = MmuAlg(Aging())
    if algorithm == 3:
        mmuAlg = MmuAlg(Random())

    #SET GRAPH

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    plt.get_current_fig_manager().resize(2000,2000)
    plt.subplots_adjust(left=0.01,right=0.99)

    

    fig.patch.set_visible(False)
    ax1.axis('off')
    ax1.axis('tight')
    ax2.axis('off')
    ax2.axis('tight')
    ax3.axis('off')
    ax3.axis('tight')
    ax4.axis('off')
    ax4.axis('tight')

    columnsMMU = ('PAGE ID', 'PID', 'LOADED', 'L-ADDR', 'M-ADDR', 'D-ADDR','LOADED-T','MARK')
    columnsData = ["Processes","Sim-Time","RAM KB", "RAM %","V-RAM-KB","V-RAM %","P LOADED","P UNLOADED","Thrashing S","Thrashing %","Frag"]
    mmuColors = ['#a2cc00','#445f95','#a41e69','#e9ab70','#e393b8','#e8e52b']

    ramColors = [[mmuColors[random.randint(0,5)] for x in range(150)]]
    plt.pause(0.1)

    plt.gcf().text(0.23, 0.93, "RAM - OPT", fontsize=10)
    plt.gcf().text(0.75, 0.93, "RAM - ALG", fontsize=10)

    plt.gcf().text(0.23, 0.55, "MMU - OPT", fontsize=10)
    plt.gcf().text(0.75, 0.55, "MMU - ALG", fontsize=10)

    plt.gcf().text(0.23, 0.76, "Datos - OPT", fontsize=10)
    plt.gcf().text(0.75, 0.76, "Datos - ALG", fontsize=10)
    

    axOpt = plt.axes([0.01, 0.0, 0.4, 0.05])
    axAlg = plt.axes([0.56, 0.0, 0.4, 0.05])
    sldrOpt = Slider(axOpt, '', 0.0, 1.0, 0.0)
    sldrAlg = Slider(axAlg, '', 0.0, 1.0, 0.0)
    sldrOpt.on_changed(updateOptSlider)
    sldrAlg.on_changed(updateAlgSlider)


    while(not finished):
        currentPointer = memCalls.pop()
        #EJECUTAMOS ALGORITMOS
        mmuOpt.execute()
        mmuAlg.execute(currentPointer, pointersDic[currentPointer],getIDP(currentPointer))
        ramOptColors = [colors[int(mmuOpt.getState().get(x)[1])] for x in mmuOpt.getAlgorithm().getRam().getMemory()]
        ramAlgColors = [colors[0 if x==0 else int(mmuAlg.getState().get(x)[1])] for x in mmuAlg.getAlgorithm().getRam().getMemory()]

        #GRAFICA TABLAS DE  RAMs
        ramOptTable = ax1.table(loc='top',cellColours=[ramOptColors])
        ramAlgTable = ax2.table(loc='top',cellColours=[ramAlgColors])

        #GRAFICA TABLAS DE  MMUs
        mmuLimitData = 25
        if (len(mmuOpt.getState())<25):
            mmuLimitData = len(mmuOpt.getState())  
        cellsOptText = [mmuOpt.getState().get(x) for x in range(1,mmuLimitData+1)]
        cellOptColours = [[colors[int(mmuOpt.getState().get(x)[1])] for i in range(8)] for x in range(1,mmuLimitData+1)]
        mmuOptTable = ax1.table(cellText=cellsOptText, colLabels=columnsMMU, loc='bottom',cellColours=cellOptColours)
        mmuOptTable.auto_set_font_size(False)
        mmuOptTable.set_fontsize(8)


        mmuLimitData = 25
        if (len(mmuAlg.getState())<25):
            mmuLimitData = len(mmuAlg.getState())  
        cellsAlgText = [mmuAlg.getState().get(x) for x in range(1,mmuLimitData+1)]
        cellAlgColours = [[colors[int(mmuAlg.getState().get(x)[1])] for i in range(8)] for x in range(1,mmuLimitData+1)]
        mmuAlgTable = ax2.table(cellText=cellsAlgText, colLabels=columnsMMU, loc='bottom',cellColours=cellAlgColours)
        mmuAlgTable.auto_set_font_size(False)
        mmuAlgTable.set_fontsize(8)


        #GRAFICA TABLAS DE DATOS
        dataOptText = [getData(mmuOpt)]
        dataOptTable = ax1.table(cellText=dataOptText, colLabels=columnsData, loc='center')
        dataOptTable.auto_set_font_size(False)
        dataOptTable.set_fontsize(8)

        dataAlgText = [getData(mmuAlg)]
        dataAlgTable = ax2.table(cellText=dataAlgText, colLabels=columnsData, loc='center')
        dataAlgTable.auto_set_font_size(False)
        dataAlgTable.set_fontsize(8)



        plt.pause(0.1)
        #BORRA LA ULTIMAS FIGURAS
        ramOptTable.remove()
        ramAlgTable.remove()
        mmuOptTable.remove()
        mmuAlgTable.remove()
        dataOptTable.remove()    
        dataAlgTable.remove()    

        # VERIFICA SI TERMINO EL PROCESO ACUTAL
        if(not memCalls.isIn(currentPointer)):
            killProcess(currentPointer, mmuOpt, mmuAlg)
        # VERIFICA SI TERMINARON TODOS LOS PROCESOS
        if(memCalls.isEmpty()):
            finish(mmuOpt, mmuAlg)
            finished = True
        #time.sleep(1)
    plt.show()
    print("FINISHED")