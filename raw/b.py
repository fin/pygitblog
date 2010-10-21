import settings
import sys


import lib.generate

if __name__=='__main__':
    if len(sys.argv)<2:
        print 'needs option: generate'
    if sys.argv[1]=='generate':
        lib.generate.generate(settings)
    if sys.argv[1]=='post':
        lib.generate.post(settings)
