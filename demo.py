from nbd import *

data = notebook()
data.cells.append(markdown('# My Demo Page\n\n'))

def index(html, resources, name):
    data.cells[-1].source += '* [{}]({})\n'.format(name, name+resources['output_extension'])
    
def report():
    yield 'index', data
    
c.Docs.notebooks = ['nbd.ipynb', 'readme.md', 'nbd.py']
c.Docs.post, c.Docs.report = index, report