
# coding: utf-8

# # A Pure Configuration Approach to Docs

# Rely on `nbformat` for the schema.

# ## Helpers
# 
# Helpers to create new notebooks and cells

# In[1]:


from nbd import *
c = globals().get('c', __import__('traitlets').config.Config())


# ## Data Object
# 
# ### Using a template notebook

# In[2]:


with open('template.ipynb') as f:
    data = reads(f.read(), 4)
last = data.cells.pop(-1)


# The next steps will configure a report.

# ## Creating custom reports
# 
# `nbd` requires a generator function that returns the `filename, notebook`; the `notebook` is written to the file name.

# In[3]:


def report():
    data.cells.append(markdown("""### [Schema](schema.html)"""))
    data.cells.append(last)
    yield 'index', data
    yield 'uml', notebook(cells=[
        markdown("""# UML diagram"""),
        markdown("""![classes_nbd.png](classes_nbd.png)""")])


# ## A simple index.

# In[4]:


from nbd import index
c.FilesWriter.build_directory = 'docs'
c.Docs.update(
    report=report,
    post=index(data),
    notebooks=[
        'nbd.ipynb',
        'config.ipynb',
        'config.py',
        'template.ipynb',
        'readme.md', 'flake8.txt'])

