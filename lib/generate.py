import os
import os.path
import re
import itertools
import codecs

import sys

from jinja2 import Environment, FileSystemLoader
import markdown2
import datetime

OUTPATH='generated'
POSTPATH='posts'
TPLPATH='templates'
STATICPATH='static'
POST_PATTERN=r'(?P<Y>....)-(?P<m>..)-(?P<d>..)-(?P<_>.*)$'

env = Environment(loader=FileSystemLoader(TPLPATH))
env.filters['markdown']=markdown2.markdown

post_tpls = []
index_tpls = []

posts = []

def slugify(string):
    """ http://djangosnippets.org/snippets/168/ """
    string = re.sub('\s+', '_', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()


class FinObj(object):
    """ object with strong ability to communicate and reflect.
    
        uses __unicode__ for outside communication and provides a default-reflecting implementation.
    """
    def __unicode__(self):
        """ __unicode__ is a pattern i love about django. don't judge me. """
        result = u'%s' % self.__class__.__name__
        for x in dir(self):
            if x.startswith('_') or callable(getattr(self, x)):
                continue
            result += u';%s=%s' % (x, getattr(self, x, None))
        return result
    def __str__(self):
        return self.__unicode__()
    def __repr__(self):
        return self.__unicode__()


class Post(FinObj):
    """ a post, with all the data extractable from the filename & the file itself.

        filename data is in .values, post-extracted data is title and content
        url is generated from the first post template in the list
    """

    def __init__(self,filename):
        self.filename = filename
        self.values = re.match(POST_PATTERN, filename).groupdict()

    @property
    def url(self):
        return post_tpls[0].expand_url(self)

    def _open(self):
        return open(os.path.join(POSTPATH, self.filename))

    @property
    def title(self):
        return self._open().readline().strip()

    @property
    def content(self):
        fd = self._open()
        fd.readline()
        fd.readline()
        return fd.read()

    @property
    def date(self):
        return datetime.date(int(self.values.get('Y',0), 10), int(self.values.get('m',0), 10), int(self.values.get('d', 0), 10))


class Template(FinObj):
    """ a template for an output file
    """
    def __init__(self, filename):
        self.filename = filename
        try:
            self.tpl = env.get_template(filename)
        except Exception, e:
            self.tpl = None
            print filename, e
        self.patterns = re.findall('%(.)', self.filename)

    def expand(self, post):
        outfile = self.filename
        for key, value in post.values.iteritems():
            outfile = outfile.replace('%%%s' % key, value)
        outfile = outfile.replace('__','/')
        return outfile

    def expand_url(self, post):
        fn = self.expand(post)
        try:
            fn = fn.substr(0,fn.index('$'))
        except:
            pass
        return fn

    def expand_filename(self, post):
        return self.expand(post).replace('$','')

    @classmethod
    def get_in(cls, d):
        for f in os.listdir(os.path.join(TPLPATH,d)):
            fn = os.path.join(d,f)
            try:
                yield cls(fn)
            except Exception, e:
                print e
                pass

def path_components(path):
    result = []
    parent = path
    while parent:
        x = os.path.split(parent)
        result.append(os.path.join(x[0],x[1]))
        parent = x[0]
    return list(result.__reversed__())

def create_parent_dirs(parent, path):
    for x in path_components(path)[:-1]:
        try:
            os.mkdir(os.path.join(parent, x))
        except Exception, e:
            if e.errno!=17: # file exists
                print e




def write_create_parents(filename, content):
    create_parent_dirs(OUTPATH, filename)
    fd = codecs.open(os.path.join(OUTPATH, filename),'w', 'utf-8')
    fd.write(content)
    fd.close()



def generate(settings):
    env.globals['settings']=settings
    env.globals['now']=datetime.datetime.now()


    for x in Template.get_in('./posts'):
        post_tpls.append(x)
    for x in Template.get_in('./indexes'):
        x.filename = x.filename.replace('./indexes', '.')
        index_tpls.append(x)

    try:
        os.mkdir(OUTPATH)
    except Exception, e:
        if not e.errno==17: # file exists
            print OUTPATH, e
        pass


    for f in os.listdir(POSTPATH):
        posts.append(Post(f))

    for post in posts:
        for posttpl in post_tpls:
            outfile = posttpl.expand_filename(post)
            write_create_parents(outfile, posttpl.tpl.render(post=post))

    for index_tpl in index_tpls:
        grouper = lambda post: '___'.join([post.values[x] for x in index_tpl.patterns])
        for k,g in itertools.groupby(posts, grouper):
            g = tuple(g)
            write_create_parents(index_tpl.expand_filename(g[0]), index_tpl.tpl.render(posts=g))

    os.copytree(STATICPATH, OUTPATH)

if __name__=='__main__':
    generate({'BASE_URL': 'test', 'TITLE': 'test', 'SUBTITLE': 'test'})
