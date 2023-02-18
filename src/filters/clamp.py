class Clamp:
    def __init__(self, min_, max_):
        self.__min = min_
        self.__max = max_
    
    def __call__(self, value):
        return max(min(value, self.__max), self.__min)