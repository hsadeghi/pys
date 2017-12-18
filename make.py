import os
import urllib2
import re
import sys
from subprocess import Popen, PIPE
import signal
from os import listdir
from os.path import join, isfile, isdir
import shutil

def main():

    clean()
    for filename in listdir(os.getcwd()):
        if filename.endswith('cpp'):
            outname = filename.split('.')[0]+'.bc'
            print 'clang++ -c -emit-llvm '+filename+' -o '+outname
            exce_cmd('clang++ -c -emit-llvm '+filename+' -o '+outname)
            outopt = filename.split('.')[0]+'O3.bc'
            print 'opt -O3 '+outname+' -o '+outopt
            exce_cmd('opt -O3 '+outname+' -o '+outopt)
            outOptll =outopt.split('.')[0]+'.ll'
            print 'llvm-dis '+outopt+' -o '+outOptll
            exce_cmd('llvm-dis '+outopt+' -o '+outOptll)
            outll = filename.split('.')[0]+'.ll'
            print 'llvm-dis '+outname+' -o '+outll
            exce_cmd('llvm-dis '+outname+' -o '+outll )
    return

def exce_cmd(flags):
    Lflags = flags.split()
    p = Popen(Lflags, stdout= PIPE , stdin=PIPE)
    (log, err)  = p.communicate()
    if err:
        print err
    else:
        print log

    return


def clean():
    for filename in listdir(os.getcwd()):
        if filename.endswith('.ll') or filename.endswith('.ll'):
            print 'removing '+ filename
            os.remove(filename)

if __name__ == '__main__':
    main()
