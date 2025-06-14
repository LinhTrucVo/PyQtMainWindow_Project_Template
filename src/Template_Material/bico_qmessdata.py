class Bico_QMessData:
    def __init__(self, *args):
        if(len(args) == 2):
            self._src = ""
            self._dst = ""
            self._mess = args[0]
            self._data = args[1]
        elif(len(args) == 4):
            self._src = args[0]
            self._dst = args[1]
            self._mess = args[2]
            self._data = args[3]
        else:
            self._src = ""
            self._dst = ""
            self._mess = ""
            self._data = ""
    
    def src(self):
        return self._src
    def setSrc(self, src):
        self._src = src

    def dst(self):
        return self._dst
    def setDst(self, dst):
        self._dst = dst

    def mess(self):
        return self._mess
    def setMess(self, mess):
        self._mess = mess
        
    def data(self):
        return self._data
    def setData(self, data):
        self._data = data

    def __str__(self):
        return "Bico_QMessData{src: " + self.src() + ", dst: " + self.dst() + ", mess: " + self.mess() + ", data: " + str(self.data()) + "}"
