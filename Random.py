import random
from Mmu import Mmu
from Ram import Ram

class Random:

    def __init__(self):
        self.setMmu(Mmu())
        self.setRam(Ram())
    
    # GETTERS
    def getMmu(self):
        return self.__mmu

    def getRam(self):
        return self.__ram


    # SETTERS
    def setMmu(self, mmu):
        self.__mmu = mmu

    def setRam(self, ram):
        self.__ram = ram


    # FUNCTIONS
    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def allocate(self, newPage):
        if self.getRam().isFull():
            page2Remove = random.choice(self.getRam())
            self.removeFromRam(page2Remove)
            self.allocateInRam(newPage)
        else:
            self.allocateInRam(newPage)