__author__ = 'hadi'

import numpy as np
import os
import re
import matplotlib
import matplotlib.pyplot as plt
from os.path import isfile,isdir,join
from subprocess import Popen, PIPE
from scipy.interpolate import interp1d
from collections import defaultdict
import operator

# Max delay assigned to packets which has not been delivered at all, this would causes a huge penalty while comparing publishers performance
MaxDelay = 1000
Threshold = 1000

def main():

    # very basic input interface ...
    while True:
        PcapFilePath = raw_input('Please enter pcap file path : ') #  'feed_arbitrage.pcap' #
        if isfile(PcapFilePath):
            break
        print 'Not a valid path !'

    # assuming tcpdump has been installed on your system, generally it needs to be checked before executing next line ...
    (log, err) = exce_cmd('tcpdump -qns 0 -X -r '+ PcapFilePath )
    log = log.splitlines()

    # extracting timing data from the log in a 3D array: [SeqNo][PublisherID][ArrivalTime]
    Delays = ExtracData(log)

    #Statistics and graphs ...
    AnalysisAndPlot(Delays)

    return

# simple procedure for invoking linux bash commands
def exce_cmd(flags):
    Lflags = flags.split()
    try:
        p = Popen(Lflags, stdout= PIPE , stdin=PIPE)
    except OSError as e:
        print e
    return p.communicate()

#  Extracting timing information, this procedure does not assume the log is sorted by time, though it makes it
#  slower yet it is more robust ...
def ExtracData(log):

    Delays = defaultdict(list) #[[MaxDelay for i in range(4)] for j in range(1000)]
    for cnt in range(len(log)):
        line = log[cnt]
        if re.match('\d\d:\d\d:(\d\d\.\d+)\s+', line):
            time = float(re.findall('\d\d:\d\d:(\d\d\.\d+)\s+', line)[0])
            if re.match('[0-9,:,\.,\s]+IP\s+\d+\.\d+\.\d+\.(\d+)\.', line):
                PublisherIndex = int(re.findall('[0-9,:,\.,\s]+IP\s+\d+\.\d+\.\d+\.(\d+)\.', line)[0]) - 1

                while not re.match('.*\s+(\d+)\.Price:', log[cnt]):
                    cnt+=1
                SeqNo = int(re.findall('.*\s+(\d+)\.Price:', log[cnt])[0]) -1
                if  not Delays.get(SeqNo, 0):
                    Delays.update({SeqNo:[MaxDelay for i in range(4)]})
                Delays[SeqNo][PublisherIndex] = time

    return [v for k,v in Delays.items()]


def AnalysisAndPlot(Delays):

    LostPackets = [0 for i in range(4)]
    for row in Delays:
        for j in range(len(row)):
            if row[j] == MaxDelay:
                LostPackets[j] +=1

    Normalized = [[x - min(row) for x in row] for row in Delays]
    # scaling data in order to round it before computing frequency
    C = [[np.ceil(100*x[i]) for x in Normalized] for i in range(4) ]
    Sorted =  [x.sort() for x in C]

    Penalty = {}
    for i in range(len(C)):
        R = C[i]
        print '\nPublisher ', str(i+1), '  average packet delay(hundredths of second):', np.mean(R), ' standard deviation of delays:' , np.std(R), ' number of omitted packets:' , str(LostPackets[i])
        if np.mean(R) > Threshold:
            print ' \t\t Publisher', str(i+1), 'was considered as outlier and hence was eliminated from the candidates (perhaps due to many packet losts ) '
            continue
        # computing y=Frequency(delay) in order to visualize and estimate area under curve
        y = np.bincount(R)
        zz = np.nonzero(y)[0]
        Conted = zip(zz, y)
        xx,yy = zip(*Conted)

        #xx= xx[1:]
        #yy=yy[1:]
        Penalty.update({i:estimatePenalty(Conted)})
        f = interp1d(xx, yy)
        xnew = np.linspace(min(xx), max(xx), num=500, endpoint=True)
        plt.plot(xnew,f(xnew), label = 'Publisher '+str(i+1) )
    Sorted_penalty = sorted(Penalty.items(), key=operator.itemgetter(1))

    select = 2
    for (key, val) in Sorted_penalty:
        if select:
            print '\nCalculated penalty for Publisher', str(key+1), ' : ', str(val), '  selected '
            select -=1
        else:
            print '\nCalculated penalty for Publisher', str(key + 1), ' : ', str(val)

    plt.xlabel('Packet Dealy (hundredths of second)')
    plt.ylabel('Number of packets')
    plt.legend(loc='upper right')
    plt.show()

#  a basic penalty function which computes area under curve function y=Frequency(delay)
def estimatePenalty(xy):
    Integral = 0
    for x,y in xy:
        Integral += x*y
    return Integral/100


if __name__ == "__main__":
    main()
