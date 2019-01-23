"""Usage: record.py -t # [-h]
            -t #: Time in seconds to be recorded (default: 2)
              -h: Print this help message
     -o filename: Write output to filename.raw and filename.dat (default: record16)
  RESULT:
   Records t seconds from your default sound card.
   With a sample rate of 22050 Hz in format S16LE (16 bit int little endian)  
"""
import sys
import time
import getopt
import alsaaudio
from math import *
from getopt import *

if __name__ == '__main__':
  opt=getopt(sys.argv[1:], "t:o:h")

  RATE = 44100#22050
  out_filename='record16'
  tr=2.
  for o in opt[0]:
     if o[0]=='-t': tr=float(o[1])
     if o[0]=='-o': out_filename=o[1]
     if o[0]=='-h': print __doc__; sys.exit(0)


  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
  inp.setchannels(1)
  inp.setrate(RATE)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(160)


  iwav = ""

  t0 = time.time()
  while time.time()-t0<tr:
    l, data = inp.read()
    #print len(data)
    if l:
      iwav += data
    time.sleep(.001)

  fiwav = open(out_filename+".raw", "w")
  fiwav.write(iwav)
  fiwav.close()

  fidat = open(out_filename+".dat", "w")
  for i in range(0, len(iwav) / 2):
    lb = ord(iwav[2*i])
    hb = ord(iwav[2*i+1])
    f = (hb << 8) | lb
    if hb > 127:
      f -= 65536
    print >> fidat, f
  fidat.close()

