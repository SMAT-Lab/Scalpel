#!/usr/bin/env python
# coding: utf-8
# In[12]:
from IPython.display import Image
from IPython.core.display import HTML
from IPython.display import HTML
HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
''')
# In[9]:
Image(filename = "img/ass10_ex08_00.png")