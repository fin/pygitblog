import settings
import sys


import lib.generate
import SimpleHTTPServer, BaseHTTPServer

if __name__=='__main__':
    if len(sys.argv)<2:
        print 'needs option: generate'
    if sys.argv[1]=='generate':
        lib.generate.generate(settings)
    elif sys.argv[1]=='post':
        lib.generate.post(settings)
    elif sys.argv[1]=='test':
        lib.generate.generate(settings)
        print 'launching on http://localhost:8889/'
        try:
            BaseHTTPServer.HTTPServer(('localhost',8889,),SimpleHTTPServer.SimpleHTTPRequestHandler).serve_forever()
        except KeyboardInterrupt:
            print '^C received, bye bye!'
    else:
        print 'unknown command'
