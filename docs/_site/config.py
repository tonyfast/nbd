
# coding: utf-8

# # A Pure Configuration Approach to Docs

# Rely on `nbformat` for the schema.

# ## Helpers
# 
# Helpers to create new notebooks and cells

# In[1]:


from nbd import *


# ## Data Object
# 
# ### Using a template notebook

# In[2]:


with open('template.ipynb') as f:
    data = reads(f.read(), 4)
last = data.cells.pop(-1)


# ## The config object
# 
# A config file modifies the application parameters.  The snippet below provides a dummy configuration `object` for development.  This value is provided in a running `jupyter` context.

# In[3]:


try: c
except NameError: c = __import__('traitlets').config.Config()


# The next steps will configure a report.

# ## Creating custom reports
# 
# `nbd` requires a generator function that returns the `filename, notebook`; the `notebook` is written to the file name.

# In[4]:


def report():
    data.cells.append(markdown("""### [Schema](schema.html)"""))
    data.cells.append(last)
    yield 'index', data
    yield 'schema', notebook(cells=[markdown("""![classes_nbd.png](classes_nbd.png)""")])


# ## A simple index.

# In[5]:


from nbd import index
c.FilesWriter.build_directory = 'docs'
c.Docs.update(
    report=report,
    post=index(data, "h1,h2"),
    notebooks=[
        'nbd.ipynb',
        'config.ipynb',
        'config.py',
        'template.ipynb',
        'readme.md', 'flake8.txt'])

