import settings
import sys


import os
DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.realpath(os.path.join(DIR, '..')))

import lib.generate

if __name__=='__main__':
    if len(sys.argv)<2:
        print 'needs option: generate'
    if sys.argv[1]=='generate':
        lib.generate.generate(settings)
    if sys.argv[1]=='post':
        lib.generate.post(settings)
