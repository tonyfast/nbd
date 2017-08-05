
# coding: utf-8

# In[1]:


from nbconvert import exporters
from nbformat.v4 import new_code_cell, new_markdown_cell, new_raw_cell as raw, new_notebook
from mistune import markdown
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from pathlib import Path
from operator import methodcaller
from fnmatch import fnmatch


# ## nbconvert `HTML` exporter
# 
# `readers` load different file extensions and return notebooks.

# In[2]:


html = exporters.html.HTMLExporter()


# ## Extension Readers

# In[3]:


readers = {
    'ipynb': lambda path: __import__('nbformat').reads(path.read_text(), 4),
    'py': lambda path: new_notebook(cells=[new_code_cell(source=path.read_text())]),
    'md': lambda path: new_notebook(cells=[new_markdown_cell(source=path.read_text())]),}
readers['markdown'] = readers['md']
readers['pyi'] = readers['py']


# ## Arguments

# ### Argument Parser

# In[4]:


parser = ArgumentParser()
parser.add_argument('--root', default=Path('.'))
parser.add_argument('--to', default=Path('./docs'))
parser.add_argument('--dir', nargs='*', default=tuple())
parser.add_argument('--ignore', nargs='*', default=('ipynb_checkpoints',))
parser.add_argument('--ext', nargs='*', default=tuple(readers))
parser.add_argument('--deep', action='store_true')
defaults = parser.parse_args(tuple())


# ## Main Program

# In[5]:


def main(
    root=defaults.root, to=defaults.to, dir=defaults.dir, ignore=defaults.ignore,
    ext=defaults.ext, deep=defaults.deep
):
    """The main nbd function."""
    root, to, *dir = Path(root), Path(to), *map(Path, dir)
    nbs = load(files(root, ext, ignore, dir, deep))
    docs = write(nbs, to, root)
    index(docs, nbs, root, to)


# ## Public Python Functions

# In[6]:


def files(root, exts, ignores, dir, deep=False):
    """Create an object of Paths to """
    return {
        path: path for dir in map(Path, [root, *dir])
        for ext in exts for path in methodcaller(
            '{}glob'.format(deep and 'r' or ''), '.'.join(('*', ext))
        )(dir) 
        if not any(fnmatch(str(path), ignore) for ignore in ignores)  
        and not any(ignore in str(path) for ignore in ignores)
    }


# In[7]:


def parents(file):
    """Create parent directories if they do no exist."""
    [_0.mkdir() for _0 in reversed([
         _1 for _1 in file.parents if not _1.exists()])]


# In[8]:


def writeFile(file, nb):
    """Export an html file from a new notebook"""
    # If the parent directories do not exists then create them.
    parents(file)
    nb = html.from_notebook_node(nb)[0]
    file.write_text(nb)
    return nb


# In[9]:


def write(nbs, to, root):
    """Orchestrate the writing of the html version of each document."""
    return {
        key: print(key) or writeFile(key, value) 
        for _, value in nbs.items()
        for key in [to/_.relative_to(root).with_suffix(_.suffix+'.html')]}


# In[10]:


def load(nbs):
    """Read each file in the documentation."""
    return {
        file: readers[file.suffix.lstrip('.')](file) for file in nbs}


# #### Open and Close `<div>`s

# In[11]:


div, _div = lambda s: raw("""<div class="{}">""".format(s)), raw("""</div>""")


# ### Documentation Index
# 
# A bootstrap `list-group` to display `html` documents.

# In[12]:


iframe = raw("""<div class="row">
<iframe class="embed-responsive-item" src="readme.ipynb.html" name="docs"></iframe>
</div>""")


# In[40]:


def item(target, to, html, nb):
    """An item in the index"""
    link = target.relative_to(to)
    name = link.with_suffix(link.suffix.rstrip('.html'))
    
    soup = BeautifulSoup(html, 'lxml')
    output = """<div class="panel panel-default">
  <div class="panel-heading"><a href="{}" target="docs"><h3 class="list-group-item-heading">{}</h3></a></div>
  """.format(str(link), str(name))
    
    if name.suffix.startswith('.ipynb'):
        output += """<div class="panel-body">{}</div>""".format(markdown(
            nb.cells and nb.cells[0].source or ""))
    
    output += """<ul class='list-group'>"""
    for item in soup.select('h1,h2,h3'):
        output+= """<li class="list-group-item">
    <h{i}><a href="{}#{}" target="docs">{}</a></h{i}></li>""".format(
            str(link), item.attrs['id'], item.text, i=2+int(item.name[-1]))
    return output + """</ul></div>""" 

def index(docs, nbs, root, to):
    """Create the index of notebook items"""
    nb = new_notebook(cells=[iframe, div("row"), raw("""""")])
    for doc in docs:
        source = root / doc.with_suffix(doc.suffix.rstrip('.html')).relative_to(to)
        
        nb.cells[-1].source += item(doc, to, docs[doc], nbs[source])
    nb.cells.extend([_div, style])
    docs[to/'index.html'] = html.from_notebook_node(nb)[0]
    (to/'index.html').write_text(docs[to/'index.html'])
    print(to/'index.html')


# ### Custom Styling
# 
# The changes in style reflect the most basic modifications to create a side-by-side documentation browser.

# In[41]:


style = raw("""
<style>
    body {
        padding: 0 !important;
    }
    body > #notebook {
        margin: 0;
        padding: 0;
    }
    #notebook-container {
        width: 100%;
        padding: 0;
        box-shadow: none;
        display: flex;
        flex-direction: row;
        align-items: stretch;
        height: 100vh;
        overflow: hidden;
    }
    #notebook-container .row {
        flex: 0;
        min-width: 33vw;
        max-height: 100%;
        overflow-y: auto;
        padding: 1rem;
    }
    
    #notebook-container .row:first-child {
        flex: 1;
        display: flex;
        flex-direction: row;
    }
    #notebook-container .panel {
        box-shadow: none;
    }
    #notebook-container .panel-heading {
        overflow-wrap: break-word;
        background: none;
    }
    #notebook-container .row iframe[name="docs"] {
        flex: 1;
        border: none;
    }
</style>
""")


# In[ ]:


if __name__ == '__main__':
        args = parser.parse_args()
        main(args.root, args.to, args.dir, args.ignore, args.ext, args.deep)


# ### Interactive mode
# 
# Enable the code cell to run `nbd` in interactive mode.
#     

#     main()
