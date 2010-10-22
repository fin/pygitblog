import settings
import sys, os


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
        path = os.getcwd()
        os.chdir('generated')
        print 'launching on http://localhost:8889/'
        try:
            BaseHTTPServer.HTTPServer(('localhost',8889,),SimpleHTTPServer.SimpleHTTPRequestHandler).serve_forever()
        except KeyboardInterrupt:
            print '^C received, bye bye!'
        os.chdir(path)
    else:
        print 'unknown command'
