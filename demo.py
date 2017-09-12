from nbd import *
# use nbd's super basic index

from nbd import index

# Store data in a notebook object
data = notebook(cells=[
    markdown('''# My Demo Page \n\nCheck out the complete [`nbd` documentation](../index.html).''')])

def report(): yield 'index', data
    
c.Docs.notebooks = ['nbd.ipynb', 'readme.md', 'nbd.py']
c.FilesWriter.build_directory = 'docs/demo'
c.Docs.post, c.Docs.report = __import__('nbd').index(data), report