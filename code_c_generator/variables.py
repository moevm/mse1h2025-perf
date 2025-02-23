from cfile.core import Variable


class StaticArray(Variable):
    def __init__(self, name, data_type, size=0):
        super().__init__(name, data_type, array=size)

    def __getitem__(self, index):
        return Variable(f"{self.name}[{index}]", self.data_type)


class Pointer(Variable):
    def __init__(self, name, data_type):
        super().__init__(name, data_type, pointer=True)
        self.mem_size = 0
        self.need_to_free_mem = False

    def __getitem__(self, index):
        return Variable(f"{self.name}[{index}]", self.data_type)
    
    def __str__(self):
        return self.name
    
