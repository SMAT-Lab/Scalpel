#!/usr/bin/env python
# coding: utf-8
# In[8]:
soma = 0
for i in range(101):
    if i % 2 == 0:
        soma = soma + i
    
print('A soma dos números pares entre 0 e 100 é', soma)
# In[1]:
get_ipython().run_cell_magic('html', '', '<style>\n.rendered_html h1 {\n    background-color: #555;\n    color: white;\n    padding: .5em;\n    // border-bottom: 2px solid #000;\n    // padding-bottom: .6em;\n    margin-bottom: 1em;\n}\n\n.rendered_html h1 code {\n    color: #EBB7C5;\n    background-color: rgba(0,0,0,0);\n}\n\n.rendered_html h2 {\n    border-bottom: 1px solid #333;\n    padding-bottom: .6em;\n}\n                                      \n.rendered_html h3 {\n    color: #034f84;\n}\n\n.rendered_html code  {\n    padding: 2px 4px;\n    font-size: 90%;\n    color: #c7254e;\n    background-color: #f9f2f4;\n    border-radius: 4px;\n}\n\n.rendered_html pre code {\n    padding: 0px;\n    font-size: 90%;\n    color: #c7254e;\n    background-color: rgba(0, 0, 0, 0);\n}\n\nkbd {\n    border-radius: 3px;  \n    padding: 2px, 3px;\n}\n\nbody {\n    counter-reset: h1counter excounter;\n}\nh1:before {\n    content: counter(h1counter) ".\\0000a0\\0000a0";\n    counter-increment: h1counter;\n}\nspan.exec:before {\n    content: counter(excounter);\n    counter-increment: excounter;\n}\n\n\n</style>  \n<script>\nlocation.hash = "#homesweethome";\n</script>')