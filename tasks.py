import PyCRC
from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRC32 import CRC32
from PyCRC.CRCCCITT import CRCCCITT

class CrcTask:
    def __init__(self, filename, start, end):
        # filename: Absolute path to save file
        # start: Beginning of offset range
        # end: End of offset range
        self.filename = filename
        self.start = start
        self.end = end
        self.complete = False
        self.result = None

def add_crctasks(jobq, filename, start, end):
    tasks = []
    for n in range(start, end):
        jobq.put(CrcTask(filename, n, end))
        print("%s: %d to %d" % (filename, n, end))
    print jobq.qsize()

def make_nums(N):
    """ 
    Create N large numbers to factorize.
    """
    nums = [999999999999]
    for i in xrange(N):
        nums.append(nums[-1] + 2)
    return nums

#TODO: We want to use only a shared string as input?
def calcChecksum(crctask):
    savefile = "/Users/spanky/Dropbox/ctf/gamecube/memorycards/bak.raw"
    save = open(savefile, 'rb').read()

    start = crctask.start
    end = crctask.end
    #MAX = len(save)/100

    #for n in range(0, len(save)):
    #for n in range(0, 26477):
    for n in range(start, end):
        print("Checking offset [%d/%d] (%f percent)" % (n, len(save), float(n)/float(end)*100))
        input = save[0:n]
        crc = CRCCCITT().calculate(input)
        #print(crc)
    return 'blah'

if __name__ == "__main__":
    make_crctasks("/tmp/barf.txt", 0, 255)
    print("Hello world")
