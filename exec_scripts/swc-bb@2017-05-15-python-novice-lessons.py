#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
data = np.loadtxt('../../data/inflammation-01.csv', delimiter=',')
data
# In[2]:
import pandas as pd
# In[3]:
df = pd.read_csv('../../data/inflammation-01.csv')
df.head()
# In[4]:
df = pd.read_csv('../../data/inflammation-01.csv', header=None, prefix='day')
df.index.name = 'patients'
df.head()
# In[5]:
df.describe()
# In[6]:
df.T.describe()
# In[7]:
df['day1']
# In[8]:
df.loc[1]
# In[9]:
df.loc[1:3, 'day5':'day10']
# In[10]:
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# In[11]:
df.loc[1].plot(title='patient 1 inflammation')
# In[12]:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# In[13]:
df = pd.read_csv(
    "http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/united-states-TAVG-Trend.txt",
    delim_whitespace=True,
    comment='%',
    header=None,
    parse_dates=[[0,1]],
    index_col=(0),
    usecols=(0, 1, 2, 3, 8, 9),
    names=("year", "month", "anomaly", "uncertainty", "10-year-anomaly", "10-year-uncertainty")
)
df.index.name = "date"
# In[14]:
df.head()
# In[15]:
df.sample(10)
# In[16]:
fig, ax = plt.subplots(figsize=(10, 6))
df["anomaly"].plot(ax=ax, alpha=0.1, linewidth=2)
df["10-year-anomaly"].plot(ax=ax, linewidth=2)
upper = df["10-year-anomaly"] + df["10-year-uncertainty"]
lower = df["10-year-anomaly"] - df["10-year-uncertainty"]
ax.fill_between(lower.index, lower, upper, alpha=0.3)
ax.set_ylabel("temp anomaly relative 1951-1980 [$^\circ C$]")
# In[17]:
df.describe()
# In[18]:
df.mean()
# In[19]:
df["anomaly"].hist(bins=20);
plt.xlabel("anomaly")
plt.figure()
# In[20]:
df_1850_1900 = df["anomaly"].loc["1850":"1900"]
df_1950_2000 = df["anomaly"].loc["1950":"2000"]
df_1850_1900.hist(bins=20, alpha=0.3)
df_1950_2000.hist(bins=20, alpha=0.3)
plt.legend(["1850-1900", "1950-2000"])
plt.xlabel("anomaly");
# In[21]:
df["10-year-anomaly-pandas"] = df['anomaly'].rolling(10 * 12, center=True).mean()
# In[22]:
plt.figure(figsize=(10, 6))
df["10-year-anomaly"].plot()
df["10-year-anomaly-pandas"].plot()
# In[23]:
get_ipython().run_cell_magic('writefile', 'anomalies.py', '\nimport numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n\nbase_url = "http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/"\n\n\ndef plot_anomaly(country_name):\n    """Plot the anomaly for the given country."""\n    \n    file_url = base_url + country_name + "-TAVG-Trend.txt"\n    \n    col_names = ("year", "month", "anomaly", "uncertainty",\n                 "10-year-anomaly", "10-year-uncertainty")\n    \n    df = pd.read_csv(file_url,\n                     delim_whitespace=True,\n                     comment=\'%\',\n                     header=None,\n                     parse_dates=[[0,1]],\n                     index_col=(0),\n                     usecols=(0, 1, 2, 3, 8, 9),\n                     names=col_names)\n\n    df.index.name = "date"\n    \n    fig, ax = plt.subplots(figsize=(10, 6))\n    \n    ax.set_title(country_name)\n\n    df["anomaly"].plot(ax=ax, alpha=0.1, linewidth=2)\n    df["10-year-anomaly"].plot(ax=ax, linewidth=2)\n\n    upper = df["10-year-anomaly"] + df["10-year-uncertainty"]\n    lower = df["10-year-anomaly"] - df["10-year-uncertainty"]\n\n    ax.fill_between(lower.index, lower, upper, alpha=0.3)\n\n    ax.set_ylabel("temp anomaly relative 1951-1980 [$^\\circ C$]")\n    \n    return fig, ax\n    ')
# In[24]:
import anomalies
# In[25]:
anomalies.plot_anomaly('belgium')
# In[26]:
get_ipython().run_cell_magic('writefile', 'show_anomalies', '#!/usr/bin/env python3\n\nimport argparse\n\nimport anomalies\n\n\nparser = argparse.ArgumentParser(\n    description="A small script to plot temperature anomaly by country name."\n)\nparser.add_argument("country_name", nargs=\'+\', help="name of the country / region")\n#parser.add_argument("-o", "--output", help="output filename")\nparser.add_argument("--dpi", help="image resolution", type=int)\n\nargs = parser.parse_args()\n\nfor country_name in args.country_name:\n    \n    #if args.output is None:\n    #    out_filename = country_name + \'.png\'\n    #else:\n    #    out_filename = args.output\n    out_filename = country_name + \'.png\'\n    \n    print("creating {}".format(out_filename))\n\n    fig, ax = anomalies.plot_anomaly(country_name)\n\n    if args.dpi is not None:\n        fig.savefig(out_filename, dpi=args.dpi)\n    else:\n        fig.savefig(out_filename)')
# In[27]:
get_ipython().system('chmod +x show_anomalies')
# In[28]:
get_ipython().system('./show_anomalies germany belgium --dpi=300')
# In[29]:
get_ipython().system('ls')
# In[30]:
import os
from urllib.request import urlretrieve
base_url = "http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/"
file_suffix = '-TAVG-Trend.txt'
data_dir = 'project_data'
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
def download_data(country_name):
    """Download anomaly data."""
    file_prefix = country_name.replace(' ', '-')
    filename = file_prefix + file_suffix
    file_url = base_url + filename
    filepath = os.path.join(data_dir, filename)
    urlretrieve(file_url, filename=filepath)
    return filepath
# In[31]:
download_regions = ['germany', 'belgium']
for region in download_regions:
    download_data(region)
# In[32]:
get_ipython().system('ls project_data/')
# In[33]:
get_ipython().run_cell_magic('writefile', 'show_available_data', '#!/usr/bin/env python3\n\nimport requests\nfrom lxml import html\nfrom urllib.request import unquote\n\nbase_url = "http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/"\n\nfilename_suffix = \'-TAVG-Trend.txt\'\n\npage = requests.get(base_url)\ntree = html.fromstring(page.content)\n\nfile_links = tree.xpath("//a[contains(@href,\'.txt\')]/@href")\nregion_names = [unquote(link.replace(filename_suffix, \'\').replace(\'-\', \' \'))\n                for link in file_links]\n\nfor name, link in zip(region_names, file_links):\n    print("{}: {}".format(name, link))')
# In[34]:
get_ipython().system('chmod +x show_available_data')
# In[35]:
get_ipython().system('./show_available_data')