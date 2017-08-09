
# coding: utf-8

# In[100]:


from nbconvert import exporters
from nbformat.v4 import new_code_cell, new_markdown_cell, new_raw_cell as raw, new_notebook
from nbconvert.preprocessors import Preprocessor
from mistune import markdown
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from pathlib import Path
from operator import methodcaller
from fnmatch import fnmatch
from traitlets import Bool


# ## nbconvert `HTML` exporter
# 
# `readers` load different file extensions and return notebooks.

# In[85]:


html = exporters.html.HTMLExporter()


# ## Extension Readers
# 
# The extension readers define valid extensions for nbd & how each path should be read.

# In[97]:


readers = {
    'ipynb': lambda path: __import__('nbformat').reads(path.read_text(), 4),
    'py': lambda path: new_notebook(cells=[new_code_cell(source=path.read_text())]),
    'md': lambda path: new_notebook(cells=[new_markdown_cell(source=path.read_text())]),}
readers['markdown'] = readers['md']
readers['pyi'] = readers['py']


# ## Arguments

# ### Argument Parser

# In[88]:


parser = ArgumentParser()
parser.add_argument('--root', default=Path('.'))
parser.add_argument('--to', default=Path('./docs'))
parser.add_argument('--dir', nargs='*', default=tuple())
parser.add_argument('--ignore', nargs='*', default=('ipynb_checkpoints',))
parser.add_argument('--ext', nargs='*', default=tuple(readers))
parser.add_argument('--deep', action='store_true')
parser.add_argument('--url', default='')
parser.add_argument('--name', default='')
parser.add_argument('--theme', default='')
parser.add_argument('--drop-input', action='store_true')
parser.add_argument('--drop-output', action='store_true')
defaults = parser.parse_args(tuple())


# ## Main Program

# In[83]:


def main(
    root=defaults.root, to=defaults.to, dir=defaults.dir, ignore=defaults.ignore,
    ext=defaults.ext, deep=defaults.deep, args=defaults
):
    """The main nbd function."""
    root, to, *dir = Path(root), Path(to), *map(Path, dir)
    nbs = load(files(root, ext, ignore, dir, deep))
    docs = write(nbs, to, root, args)
    index(docs, nbs, root, to, {
        key: getattr(args, key) for key in ['name', 'url']
        if getattr(args, key)
    }, args.theme)


# ## Public Python Functions

# In[50]:


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


# In[51]:


def parents(file):
    """Create parent directories if they do no exist."""
    [_0.mkdir() for _0 in reversed([
         _1 for _1 in file.parents if not _1.exists()])]


# In[95]:


def writeFile(file, nb, args):
    """Export an html file from a new notebook"""
    # If the parent directories do not exists then create them.
    parents(file)
    nb = html.from_notebook_node(
        Remove(input=args.drop_input, output=args.drop_output).preprocess(nb, {})[0]
    )[0]
    file.write_text(nb)
    return nb


# In[93]:


def write(nbs, to, root, args):
    """Orchestrate the writing of the html version of each document."""
    return {
        key: print(key) or writeFile(key, value, args) 
        for _, value in nbs.items()
        for key in [to/_.relative_to(root).with_suffix(_.suffix+'.html')]}


# In[94]:


def load(nbs):
    """Read each file in the documentation."""
    return {
        file: readers[file.suffix.lstrip('.')](file) for file in nbs}


# #### Open and Close `<div>`s

# In[55]:


div, _div = lambda s: raw("""<div class="{}">""".format(s)), raw("""</div>""")


# ### Notebook Viewer in an IFrame

# In[56]:


iframe = raw("""<div class="row">
<iframe class="embed-responsive-item" src="readme.ipynb.html" name="docs"></iframe>
</div>""")


# ### Documentation Index
# 
# A bootstrap `list-group` to display `html` documents.

# In[118]:


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

def index(docs, nbs, root, to, disqus=None, theme=None):
    """Create the index of notebook items"""
    nb = new_notebook(cells=[iframe, 
                             div("row"), ])
    nb.cells.append(raw(""""""))
    for doc in docs:
        source = root / doc.with_suffix(doc.suffix.rstrip('.html')).relative_to(to)
        
        nb.cells[-1].source += item(doc, to, docs[doc], nbs[source])
    
    disqus and nb.cells.append(
        raw(DISQUS(name=disqus.get('name'), url=disqus.get('url'))))
        
    nb.cells.extend([_div])
    docs[to/'index.html'] = html.from_notebook_node(nb, {})[0].replace(
        """<div class="container" id="notebook-container">""",
        """<div class="container flexxed" id="notebook-container">"""
    )
    
    docs[to/'custom.css'] = (add_theme(theme) if theme else theme) + style
    for key in ('index.html', 'custom.css'): (to / key).write_text(docs[to/key])


# ## Toggle Input and Output Preprocessor
# 
# An nbconvert preprocessor that removes input or output cells.  Literacy re-renders code in the output.  Software projects make forcibly remove output cells to maintain a clean document.

# In[109]:


class Remove(Preprocessor):
    input = Bool(False)
    output = Bool(False)
    
    def preprocess_cell(self, cell, resources, index):
        if self.input or self.output:
            cell = cell.copy()
        
        if hasattr(cell, 'outputs'):
            
            if self.input:
                cell.source = """"""
            
        
            if self.output:
                cell.outputs = []
                
        return cell, resources


# ## Customization
# 
# ### Custom Styling
# 
# The changes in style reflect the most basic modifications to create a side-by-side documentation browser.
# 
# This should probably go in custom.css.

# In[120]:


style = """
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
}

div.flexxed#notebook-container {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    height: 100vh;
    overflow: hidden;
}

div.flexxed#notebook-container .row {
    flex: 0;
    min-width: 33vw;
    max-height: 100%;
    overflow-y: auto;
    padding: 1rem;
}

div.flexxed#notebook-container .row:first-child {
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

div.flexxed#notebook-container .row iframe[name="docs"] {
    flex: 1;
    border: none;
}
"""


# ### Disqus Universal Embed Code
# 
# Disqus Universal embed code

# In[111]:


DISQUS = html.environment.from_string("""<div class="row" id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = "{{url}}";  // Replace PAGE_URL with your page's canonical URL variable
        this.page.identifier = "{{url}}"; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    (function() {  // REQUIRED CONFIGURATION VARIABLE: EDIT THE SHORTNAME BELOW
        var d = document, s = d.createElement('script');

        s.src = 'https://{{name}}.disqus.com/embed.js';  // IMPORTANT: Replace EXAMPLE with your forum shortname!

        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>""").render


# ### Experimental Themes
# 
# Attach free bootswatch theme.

# In[105]:


add_theme = """
@import url(https://bootswatch.com/{}/bootstrap.min.css);
""".format


# In[ ]:


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.root, args.to, args.dir, args.ignore, args.ext, args.deep, args)

