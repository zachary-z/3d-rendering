import math

class vec:
    def __init__(self, *args):
        self.array = [arg for arg in args]
    def __neg__(self):
        self.array = [-coord for coord in self.array]
    def __add__(self, other):
        newarray = [self.array[i]+other.array[i] for i in range(len(self.array))]
        return vec(*newarray)
    def __iadd__(self, other):
        self.array = [self.array[i]+other.array[i] for i in range(len(self.array))]
    def __sub__(self, other):
        newarray = [self.array[i]-other.array[i] for i in range(len(self.array))]
        return vec(*newarray)
    def __isub__(self, other):
        self.array = [self.array[i]-other.array[i] for i in range(len(self.array))]
    def __mul__(self, other):
        if type(self) == type(other):
            return sum([self.array[i]*other.array[i] for i in range(len(self.array))])
        else:
            newarray = [self.array[i]*other for i in range(len(self.array))]
            return vec(*newarray)
    def __rmul__(self, other):
        if type(self) == type(other):
            return sum([self.array[i]*other.array[i] for i in range(len(self.array))])
        else:
            newarray = [self.array[i]*other for i in range(len(self.array))]
            return vec(*newarray)
    def __xor__(self, other):
        if len(self.array) == 3 and len(other.array) == 3:
            newarray = [self.array[1]*other.array[2] - self.array[2]*other.array[1],
                        self.array[2]*other.array[0] - self.array[0]*other.array[2],
                        self.array[0]*other.array[1] - self.array[1]*other.array[0]]
            return vec(*newarray)
    def __truediv__(self, other):
        newarray = [self.array[i]/other for i in range(len(self.array))]
        return vec(*newarray)
    def __len__(self):
        return len(self.array)
    def __abs__(self):
        return math.sqrt(sum([value**2 for value in self.array]))
    def __getitem__(self, i):
        return self.array[i]
    def __setitem__(self, i, value):
        self.array[i] = value
    def dist(self, other):
        return abs(self-other)
    def angle(self):
        return math.atan2(self.array[1], self.array[0])
    def normalize(self):
        if abs(self) == 0:
            return self
        return self/abs(self)
