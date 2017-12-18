
import sys

print sys.path
sys.path.append('/home/hadi/PycharmProjects')
print sys.path
import myM
import modu
from myM import func


class dog:
    #myName = ''
    #myAge = 0
    def __init__(self, strName = '', intAge = 0):
        self.myName = strName
        self.myAge = intAge

    def PrintInf(self):
        print 'Dog info, name: ',self.myName, '\tage: ', self.myAge

class animal:
    def __init__(self, strType=''):
        if strType: self.type = strType
        else: self.type = 'unknwon'

    def printType(self):
        print self.type

class parsingDog(dog, animal):

    def __init__(self, strName = '', intAge = 0, strTy = ''):
        dog.__init__(self,strName, intAge)
        animal.__init__(self, strTy)
        self.cnt = 0

    def pars(self):
        self.cnt+=1
        print self.myName, 'is parsing for the ',self.cnt, 'time'

def main():
    func()
    modu.func2()
    d1 = dog('cici')
    d1.PrintInf()

    d2= parsingDog('mini', 8)
    d2.PrintInf()
    d2.printType()
    d2.type = raw_input("animal type : ")
    d2.printType()
    stepval = int(raw_input('loop cnt : '))
    endval = myM.endval
    try:
        endval = endval/stepval
    except(TypeError, ZeroDivisionError):
        print '[exepction] div-zero error occurred '
    else:
        endval+=1
    finally:
        if not stepval: return

    for i in range(0,endval):
        d2.pars()
    #else: # how it could be useful to have else here ?!
    #    print 'no loop execution'


if __name__ == "__main__":
    main()