from Ram import Ram

class Aging:

    def __init__(self):
        self.setRam(Ram())
    
    # GETTERS
    def getRam(self):
        return self.__ram


    # SETTERS
    def setRam(self, ram):
        self.__ram = ram


    # FUNCTIONS
    def removeFromRam(self, page):
        self.getRam().removePage(page)

    def allocateInRam(self, page):
        self.getRam().allocatePage(page)

    def allocate(self, newPage):
        if self.getRam().isFull():
            # Falta implementar algoritmo
            self.allocateInRam(newPage)
        else:
            self.allocateInRam(newPage)