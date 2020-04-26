#!/usr/bin/python3
import numpy as np

class Logic:

    karnovList = [0,1,3,2,6,4,5,7]

    def __init__(self,inputs,outputs,conditions):
        self.inputs = inputs
        self.outputs = outputs
        self.dim = self.calcmd()
        self.conditions = conditions
        self.outputTable = {}
        self.matrix = {}
        self.results = {}
        self.squares= {}
        for output in outputs:
            self.outputTable[output] = np.zeros(2**len(self.inputs),dtype = bool)
            self.matrix[output] = np.zeros(self.dim,dtype = bool)
            self.squares[output] = []
            self.results[output] = []

    def calcmd(self):
        if len(self.inputs)%2 == 0:
            num_rows = 2**(len(self.inputs)/2)
            num_cols = num_rows
        else:
            num_rows = 2**((len(self.inputs)+1)/2)
            num_cols = 2**((len(self.inputs)-1)/2)
        return (int(num_rows),int(num_cols))

    def truthTable(self):
        for output in self.outputs:
            for state in range(0,2**len(self.inputs)):
                for condition in self.conditions[output]:
                    temp = condition
                    for input in self.inputs:
                        index = temp.find(input)
                        if index != -1:
                            binState = format(state,'0'+str(len(self.inputs))+'b')[self.inputs.index(input)]
                            temp = temp[:index]+binState+temp[index+len(input):]
                    temp = "if "+temp+":\n self.outputTable['"+output+"']["+str(state)+"]=1"
                    exec(temp)

    def fillMatrix(self):
        for output in self.outputs:
            for i in range(0,self.dim[0]):
                side = format(self.karnovList[i],'0'+str(self.dim[0]//2)+'b')
                for j in range(0,self.dim[1]):
                    top = format(self.karnovList[j],'0'+str(self.dim[1]//2)+'b')
                    if self.outputTable[output][int(side+top,2)]:
                        self.matrix[output][i][j] = 1

    def calcMatrix(self):
        for output in self.outputs:
            for i in range(0,self.dim[0]):
                for j in range(0,self.dim[1]):
                    if self.matrix[output][i][j] and not self.inSquare(output,i,j):
                        self.findSquare(output,i,j)

    def inSquare(self,output,i,j):
        for square in self.squares[output]:
            if (i >= square[0] and i < square[0]+square[2]) and (j >= square[1] and j < square[1]+square[3]):
                return True
        return False

    def findSquare(self,output,x,y):
        if x == self.dim[0]-1:
            x = -x
            y = -y
        for xw in range(self.dim[0]//2,0,-1):
            for yw in range(self.dim[1]//2,0,-1):
                done = True
                for i in range(x,x+2**xw):
                    for j in range(y,y+2**yw):
                        try:
                            if self.matrix[output][i][j] != 1:
                                done = False
                                break
                        except:
                            done = False
                            break
                if done:
                    self.squares[output].append([abs(x),abs(y),2**xw,2**yw])
                    break
            if done: break

    def calcResult(self):
        for output in self.outputs:
            for square in self.squares[output]:
                result = {}
                if square[0] == self.dim[0]-1: temp = square[0] - square[2] + 1
                else: temp = square[0]
                side =  format(self.karnovList[temp],'0'+str(self.dim[0]//2)+'b')\
                       +format(self.karnovList[square[1]],'0'+str(self.dim[1]//2)+'b')
                k=0
                for input in self.inputs:
                    result[input] = int(side[k])
                    k+=1
                for i in range(temp+1,temp+square[2]):
                    nextside = format(self.karnovList[i],'0'+str(self.dim[0]//2)+'b')
                    index = 0
                    for input in self.inputs[:self.dim[0]//2]:
                        if result[input] != int(nextside[index]):
                            result[input] = None
                        index +=1
                for j in range(square[1]+1,square[1]+square[3]):
                    nextside = format(self.karnovList[j],'0'+str(self.dim[1]//2)+'b')
                    index = 0
                    for input in self.inputs[self.dim[1]//2:]:
                        if result[input] != int(nextside[index]):
                            result[input] = None
                        index +=1
                self.results[output].append(result)

    def showResult(self):
        for output in self.outputs:
            temp = ""
            for index in self.results[output]:
                for key in index:
                    if  index[key] == 1 : temp += key + " + "
                    elif index[key] == 0 : temp += "not(" + key + ") + "
            print(output,end=": ")
            print(temp[:-2])
    def showSquares(self):
        for key in self.squares:
            print(key +":")
            print(self.squares[key])
    def showMatrix(self):
        for key in self.matrix:
            print(key +":")
            print(self.matrix[key])
    def showTable(self):
        for output in self.outputs:
            print(output,end=" ")
        print( )
        for i in range(0,2**len(self.inputs)):
            for output in self.outputTable:
                print(int(self.outputTable[output][i]),end=" ")
            print( )


conditions = {}
inputs = input("Vlezovi {S1 S1 .. Sn}: ").split(" ")
outputs = input("Ilzesi {S1 S1 .. Sn}: ").split(" ")
for output in outputs:
    conditions[output] = []
for output in outputs:
    for i in range(0,int(input("Broj na uslovi za "+output+": "))):
        conditions[output].append(input("Uslov "+str(i)+": "))

chose = input("Chose what to show { TruthTable[t] KarnovMatrix[m] KarnovSquares[s] Result[r] }: ").split(" ")

app = Logic(inputs,outputs,conditions)
app.truthTable()
app.fillMatrix()
app.calcMatrix()

if "t" in chose:
    app.showTable()
if "s" in chose:
    app.showSquares()
if "m" in chose:
    app.showMatrix()
if "r" in chose:
    app.calcResult()
    app.showResult()

#inputs = ["S1","S2","V","M"]
#outputs = ["L","A"]
#conditions = {"L":["(S1 or S2) and not V","M"],"A":["S1 or S2"]}
