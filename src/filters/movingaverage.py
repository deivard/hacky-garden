class MovingAverage:
    def __init__(self, window_size: int = 10) -> None:
        self.__window_size = window_size
        self.__window = []
    
    def __call__(self, value):
        if len(self.__window) == self.__window_size:
            self.__window.pop(0)
        self.__window.append(value)
        average = sum(self.__window) / len(self.__window)
        
        return average

    def reset(self):
        self.__window = []
