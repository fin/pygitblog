import lib.generate
import sys
import shutil
import os
import jinja2
import codecs
import git
import stat

from optparse import OptionParser

usage = u'usage: %prog init blogtitle [subtitle] [baseurl]'
parser = OptionParser(usage=usage)

if __name__=='__main__':
    (options, args) = parser.parse_args()

    if len(args)<2:
        parser.print_usage()
        sys.exit(-1)

    if args[0]=='init':
        blogtitle = args[1]
        subtitle = args[2] if len(args)>2 else 'default subtitle'
        baseurl = args[3] if len(args)>3 else 'http://example.com/blog/'

        if len(args)<5:
            print 'settings the base url to example.com/blog - please edit the settings file before going live for the feed template to work!'

        dirname = lib.generate.slugify(blogtitle)

        if not os.path.abspath(os.path.dirname(__file__)) in os.path.abspath(dirname):
            print 'escape attempt!'
            sys.exit(-1)

        shutil.copytree('raw', dirname)

        settingsfile = os.path.join(dirname, 'settings.py')

        settings = codecs.open(settingsfile, 'r', 'utf-8').read()
        settings = jinja2.Template(settings).render(title=blogtitle, subtitle=subtitle, base_url=baseurl)
        codecs.open(settingsfile, 'w', 'utf-8').write(settings)

        git.Repo.init(os.path.abspath(dirname))

        hookfile = os.path.join(dirname, '.git/hooks/post-receive')
    
        open(hookfile,'w').write("""#!/bin/bash
GIT_DIR=$(pwd)
cd ../
python b.py generate
echo `pwd`
            """)
        r = git.Repo(os.path.abspath(dirname))
        r.git.add('*')
        r.git.commit('-a','-m lol')
        r.git.config('receive.denyCurrentBranch', 'ignore')

        os.chmod(hookfile, os.stat(hookfile).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
