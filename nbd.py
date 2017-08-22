
# coding: utf-8

# Looking for opinions on:
# 
# * load which dynamically chooses an loader that turns a file into the notebook format
# * the `from_export` method on the ExportBase which ingests data produced by from notebook node.

# In[1]:


from traitlets.utils.importstring import import_item
from pathlib import Path
import nbconvert.nbconvertapp
import traitlets, io
import nbformat
from mimetypes import MimeTypes
from nbformat.v4 import new_code_cell, new_markdown_cell, new_raw_cell as raw, new_notebook, new_output
from nbformat import NotebookNode


# In[2]:


mimetypes = MimeTypes(['documentation.types'])


#         %%file documentation.types
#         application/vnd.jupyter ipynb
#         text/markdown md markdown
#         text/x-python pyi

# In[3]:


class Loader(traitlets.config.Configurable):
    mimetype = traitlets.Enum([str for object in mimetypes.types_map for str in object.values()]).tag(config=True)
    loader = traitlets.Any().tag(config=True)
    def __call__(self, stream, resources=None, **kw):
        return self.loader(stream)


# In[4]:


class ReduceExport(traitlets.config.Configurable):
    filename = traitlets.Unicode().tag(config=True)
    enabled = traitlets.Bool(True).tag(config=True)
    nb = traitlets.Instance('nbformat.NotebookNode').tag(config=True) # notebooknode
    
    @traitlets.default('nb')
    def _default_nb(self): return nbformat.v4.new_notebook()
    
    @traitlets.default('exporter')
    def _default_exporter(self): return nbconvert.exporters.html.HTMLExporter()

    def from_render(self, output, resources, **kw): return output, resources


# In[5]:


def load_notebook(str): return nbformat.reads(str, 4)
def load_markdown(str): return new_notebook(cells=[new_markdown_cell(str)])
def load_code(str): return new_notebook(cells=[new_code_cell(str)])


# In[6]:


class StaticExporter(nbconvert.exporters.html.HTMLExporter):
    _current_mimetype = None

    loaders = traitlets.List([
        Loader(mimetype='application/vnd.jupyter', loader=load_notebook),
        Loader(mimetype='text/x-python', loader=load_code),
        Loader(mimetype='text/markdown', loader=load_markdown),]).tag(config=True)
 
    post_render = traitlets.List([]).tag(config=True)
    
    def from_filename(self, notebook_filename, resources=None, **kw):
        type = mimetypes.guess_type(notebook_filename)[0]
        for loader in self.loaders:
            if loader.mimetype == type:
                return self.from_notebook_node(
                    loader(
                        Path(notebook_filename).read_text()
                    ),resources, **kw)
                        
    def from_notebook_node(self, nb, resources=None, **kw):
        output, resources = super().from_notebook_node(nb, resources)
        for post_render in self.post_render: 
            post_render.enabled and post_render.from_render(output, resources)
        return output, resources
    
    def init_notebooks(self, value):
        for i, value in super().init_notebooks() or enumerate(self.post_render):
            if type(value) is str:
                value[i] = import_item(post_render)


# In[ ]:


class NbdApp(nbconvert.nbconvertapp.NbConvertApp):
    def convert_notebooks(self):
        for render in super().convert_notebooks() or self.exporter.post_render:
            render.enabled and nbconvert.nbconvertapp.NbConvertApp.convert_single_notebook(
                self, render.filename, io.StringIO(nbformat.writes(render.nb)))
            
    def init_single_notebook_resources(self, notebook_filename):
        resources = super().init_single_notebook_resources(notebook_filename)
        resources['name'] = resources['unique_key'] = notebook_filename
        return resources
            
NbdApp.export_format.default_value = 'nbd.StaticExporter'


# In[7]:


main = launch_new_instance = NbdApp.launch_instance

