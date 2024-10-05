class Signal():
    def __init__(self, signal, color = "red", label = "signal", visability=True):
        self.__color = color
        self.__label = label
        self.__signal = signal
        self.__visability = visability
        
    @property
    def color(self):
        return self.__color
    
    @property
    def label(self):
        return self.__label
    
    @property
    def signal(self):
        return self.__signal
    
    @property
    def visability(self):
        return self.__visability
    
    @signal.setter
    def signal(self, value):
        if value.isinstance(list):
            self.__signal = value
        else:
            raise Exception("the signal must be a list")
        
    @color.setter
    def color(self, value): ## this function could be modified accourding to the gui
        if value.isinstance(str):
            self.__color = value
        else :
            raise Exception("the color must be a string")  
        
    @label.setter
    def label(self, value): 
        if value.isinstance(str):
            self.__label = value
        else :
            raise Exception("the label must be a string")  
        
    @visability.setter
    def visability(self, value): 
        if value.isinstance(bool):
            self.__visability = value
        else :
            raise Exception("the visability must be a boolean")  
    
    
        