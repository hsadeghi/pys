import os
import urllib2
import re
import sys
import  subprocess
from subprocess import Popen, PIPE, check_output
import signal
from os import listdir
from os.path import join, isfile, isdir
import shutil

RGPath = 'RandG'
prefixRnd = "randData_"
cwd = os.getcwd()
#optPath = ''

def main():
    envVarDic = {'opt': 'OPT5', 'clang++': 'CLANG5', 'llc': 'LLC5'}
    llvmPaths = {}
    #clean()

    for (key, val) in envVarDic.items():
        llvmPaths[key] = findBinaryPath(key, val)
        if not llvmPaths[key]:
            print key+' 5.0 not found !'
            return
    RandGeneratorPath = join(cwd, RGPath)
    if not isdir(RandGeneratorPath):
        print 'can not find random input data folder !', RandGeneratorPath
        return
    for filename in listdir(cwd):
        if filename.endswith('.cpp'):
            bench = filename.split('.')[0]
            rndDatacpp = prefixRnd + bench + '.cpp'
            rndDataPath = join(RandGeneratorPath, rndDatacpp)
            if not isfile(rndDataPath):
                continue
            rndExe = prefixRnd + bench + '.exe'
            if not exce_cmd(llvmPaths['clang++'] +' -std=c++11 '+rndDataPath +' -o '+ rndExe):
                return
            dataRnd = prefixRnd + bench + '.bin'
            dataRndPath = join(RGPath ,dataRnd )
            if not exce_cmd('./'+rndExe + '  '+ dataRndPath):
                continue

            nonOptBC = bench + '.bc'
            optO3bc = bench+'O3.bc'
            optPlusO3bc = bench + 'O3Plus.bc'
            objO3 = bench+'O3.o'
            objplusO3 = bench+'O3Plus.o'
            exeO3 = bench+'O3.exe'
            exeplusO3 = bench+'O3Plus.exe'
            bench = bench+'.cpp'
            resO3 = exeO3+'.res'
            resPlus = exeplusO3+'.res'

            oldFiles =[nonOptBC , optO3bc, optPlusO3bc, objO3, objplusO3, exeO3, exeplusO3, resO3, resPlus]
            delete_oldFiles(oldFiles)

            if not exce_cmd(llvmPaths['clang++'] +' -std=c++11 -c -emit-llvm '+bench+' -o '+nonOptBC): continue
            if not exce_cmd(llvmPaths['opt'] +' -O3 '+nonOptBC+' -o '+optO3bc): continue

            if isfile(join(cwd, optPlusO3bc)): exce_cmd('rm  ' + optPlusO3bc)

            if not exce_cmd(llvmPaths['opt'] +' -mem2reg  -loop-simplify -lcssa -loop-rotate -loop-simplify -indOpt '
                                    + nonOptBC + ' -o ' + optPlusO3bc): continue

            if not exce_cmd(llvmPaths['opt'] +' -O3 ' + optPlusO3bc + ' -o ' + optPlusO3bc): continue
            if not exce_cmd(llvmPaths['llc'] +' -filetype=obj '+optO3bc + ' -o '+ objO3): continue
            if not exce_cmd(llvmPaths['llc'] +' -filetype=obj '+optPlusO3bc + ' -o '+ objplusO3): continue

            if not exce_cmd(llvmPaths['clang++'] +' -std=c++11  '+objO3 +' -o  '+ exeO3): continue
            #

            if not exce_cmd(llvmPaths['clang++'] +' -std=c++11  ' + objplusO3 + ' -o  ' + exeplusO3): continue

            if not exce_cmd('./'+exeO3 + '  '+dataRndPath ): continue
            if not exce_cmd('./'+exeplusO3 + '  '+dataRndPath): continue

            if not isfile(resO3): continue
            if not isfile(resPlus): continue
            fo3 = open(resO3, 'r')
            fplus = open(resPlus, 'r')

            res = fo3.read().split()
            cnt = int(res[0])
            rPlus = fplus.read().split()

            for i in range(0, cnt):
                if int(res[i]) != int(rPlus[i]):
                    print "extra transforn has caused invalid result for benchmark ", bench ,"!!!\n "
                    return

            print "result OK for bechmark ", bench, "\n"
            exeTimeO3 = 0
            exeTimePlus = 0
            for i in range(cnt, len(res)):
                #print res[i]
                if(res[i].startswith('execution')):
                    #print res[i], rPlus[i]
                    exeTimeO3 =float(re.findall('(\d+)', res[i])[0])
                    exeTimePlus = float(re.findall('(\d+)', rPlus[i])[0])
                    break

            print "preformance for ", bench,  (exeTimeO3)/exeTimePlus, '\n'


    return

def findBinaryPath(llvmModule, envVar):
    #envVar = envVarDic[llvmModule]
    path2 = os.environ.get(envVar)
    searchPaths = []
    #print 'env res ', path2
    if path2: searchPaths.append(path2)
    p = Popen(('which '+llvmModule).split(), stdout=PIPE, stdin=PIPE)
    pth = p.communicate()[0]
    #print 'which res', pth
    if pth: searchPaths.append(pth)

    for srchPath in searchPaths:

            cmd = (pth + ' --version ').split()
            vrCheck = Popen(cmd, stdout= PIPE , stdin=PIPE)
            out = vrCheck.communicate()[0]
            vrs = re.findall('.*\sversion\s+([\d\.]+)[\s\w]+', out)
            if not vrs: continue
            if vrs[0] == '5.0.0':
                print llvmModule,'5.0 found ', pth
                return pth.strip('\n')
    return ''




def delete_oldFiles(oldFiles):
    for oldf in oldFiles:
        if isfile(join(cwd, oldf)):
            # print 'removing oldfile ', oldf
            rmcmd = ('rm  ' + join(cwd, oldf)).split()
            p = Popen(rmcmd,stdout= PIPE , stdin=PIPE )

def exce_cmd(flags):
    print flags
    Lflags = flags.split()
    p = Popen(Lflags, stdout= PIPE , stdin=PIPE)
    log, err = p.communicate()
    print log
    if p.returncode:
        print 'command exited with non-zerod code !'
        return 0
    return 1

def exce_cmd2(flags):
    print flags, '\n'
    Lflags = flags.split()
    log= ''
    try:
        log = check_output(Lflags, stderr=PIPE)
    except subprocess.CalledProcessError:
        print log
        print 'command exited with non-zerod code !'
        return 0

    print log
    return 1


def clean():
    for filename in listdir(os.getcwd()):
        if filename.endswith('.ll') or filename.endswith('.ll'):
            print 'removing '+ filename
            os.remove(filename)

if __name__ == '__main__':
    main()