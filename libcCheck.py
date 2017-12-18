import ctypes
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

def main():
    pathList = '/lib/x86_64-linux-gnu/libc.so.6'#exce_cmd('locate libc.so')
    libc = ctypes.cdll.LoadLibrary(pathList)
    cprint = libc.printf
    cprint.argtypes = [ctypes.c_char_p]
    cprint("hi ! \n\n")

    cmemcpy = libc.memcpy
    cmemcpy.argtypes = [ctypes.c_char_p , ctypes.c_char_p, ctypes.c_int]
    str1 = "hereandhere"
    str2 = "nothing"
    cmemcpy(str1, str2, 5)
    cprint(str1)
    cprint("  ")
    cprint(str2)
    print '\n', str1, str2

    clog = libc.abs
    clog.argtypes = [ctypes.c_double]
    clog.restype = ctypes.c_double
    res = clog(-9.23)
    cprint.argtypes = [ctypes.c_char_p,ctypes.c_double]
    cprint("%.6f",res) # why output is not correct ?!
    print '\n', res

    cint = ctypes.c_int(63)
    ptr = ctypes.POINTER(ctypes.c_int)
    print cint.value
    print ptr

    f = ctypes.c_float()
    s = ctypes.create_string_buffer('\000' * 32)
    csacnf = libc.sscanf
    csacnf("1 3.14 Hello", "%f %s", ctypes.byref(f), s)

    print s.value

def exce_cmd(flags):
    print flags
    Lflags = flags.split()
    log = ''
    err= ''
    retcode = 0
    try:
        p = Popen(Lflags, stdout= PIPE , stdin=PIPE)
        log, err = p.communicate()
        retcode = p.returncode
    except subprocess.CalledProcessError:
        exit(1)
    else:
        if retcode:
            print 'command exited with non-zerod code !'
            exit(1)
    finally:
        print log
    return log


if __name__ == '__main__':
    main()


