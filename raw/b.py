import settings
import sys


import os
import django
DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.dirname(os.path.join(DIR, '..')))

import lib.generate

if __name__=='__main__':

    if len(sys.argv)<2:
        print 'needs option: generate'
    if sys.argv[1]=='generate':
        lib.generate.generate(settings)
