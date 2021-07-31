#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
# Suppress all warnings just to keep the notebook nice and clean. 
# This must happen after all imports since numpy actually adds its
# RankWarning class back in.
import warnings
warnings.filterwarnings("ignore")
# Setup the look and feel of the notebook
sns.set_context("notebook", 
                font_scale=1.5, 
                rc={"lines.linewidth": 2.5})
sns.set_style('whitegrid')
sns.set_palette('deep')
# Create a couple of colors to use throughout the notebook
red = sns.xkcd_rgb['vermillion']
blue = sns.xkcd_rgb['dark sky blue']
from IPython.display import display
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
# In[2]:
def factorial(n):
    """Calculates the factorial of `n`
    """
    vals = list(range(1, n + 1))
    if len(vals) <= 0:
        return 1
    prod = 1
    for val in vals:
        prod *= val
        
    return prod
    
    
def n_choose_k(n, k):
    """Calculates the binomial coefficient
    """
    return factorial(n) / (factorial(k) * factorial(n - k))
def binom_prob(n, k, p):
    """Returns the probability of see `k` heads in `n` coin tosses
    
    Arguments:
    
    n - number of trials
    k - number of trials in which an event took place
    p - probability of an event happening
    
    """
    return n_choose_k(n, k) * p**k * (1 - p)**(n - k)
# In[3]:
# Calculate the probability for every possible outcome of tossing 
# a fair coin 30 times.
probabilities = [binom_prob(30, k, 0.5) for k in range(1, 31)]
# Plot the probability distribution using the probabilities list 
# we created above.
plt.step(range(1, 31), probabilities, where='mid', color=blue)
plt.xlabel('number of heads')
plt.ylabel('probability')
plt.plot((22, 22), (0, 0.1599), color=red);
plt.annotate('0.8%', 
             xytext=(25, 0.08), 
             xy=(22, 0.08), 
             multialignment='right',
             va='center',
             color=red,
             size='large',
             arrowprops={'arrowstyle': '<|-', 
                         'lw': 2, 
                         'color': red, 
                         'shrinkA': 10});
# In[4]:
print("Probability of flipping 22 heads: %0.1f%%" % (binom_prob(30, 22, 0.5) * 100))
# In[5]:
def p_value(n, k, p):
    """Returns the p-value for the given the given set 
    """
    return sum(binom_prob(n, i, p) for i in range(k, n+1))
print("P-value: %0.1f%%" % (p_value(30, 22, 0.5) * 100))
# In[6]:
M = 0
n = 50000
for i in range(n):
    trials = np.random.randint(2, size=30)
    if (trials.sum() >= 22):
        M += 1
p = M / n
print("Simulated P-value: %0.1f%%" % (p * 100))
# In[7]:
import pandas as pd
df = pd.DataFrame({'star':  [1, 1, 1, 1, 1, 1, 1, 1] + 
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'score': [84, 72, 57, 46, 63, 76, 99, 91] +
                            [81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69]})
df
# In[8]:
star_bellied_mean = df[df.star == 1].score.mean()
plain_bellied_mean = df[df.star == 0].score.mean()
print("Star-bellied Sneetches Mean: %2.1f" % star_bellied_mean)
print("Plain-bellied Sneetches Mean: %2.1f" % plain_bellied_mean)
print("Difference: %2.1f" % (star_bellied_mean - plain_bellied_mean))
# In[9]:
df['label'] = df['star']
num_simulations = 10000
differences = []
for i in range(num_simulations):
    np.random.shuffle(df['label'])
    star_bellied_mean = df[df.label == 1].score.mean()
    plain_bellied_mean = df[df.label == 0].score.mean()
    differences.append(star_bellied_mean - plain_bellied_mean)
# In[10]:
p_value = sum(diff >= 6.6 for diff in differences) / num_simulations
print("p-value: %2.2f" % p_value)
# In[11]:
plt.hist(differences, bins=50, color=blue)
plt.xlabel('score difference')
plt.ylabel('number')
plt.plot((6.6, 6.6), (0, 700), color=red);
plt.annotate('%2.f%%' % (p_value * 100), 
             xytext=(15, 350), 
             xy=(6.6, 350), 
             multialignment='right',
             va='center',
             color=red,
             size='large',
             arrowprops={'arrowstyle': '<|-', 
                         'lw': 2, 
                         'color': red, 
                         'shrinkA': 10});
# In[12]:
df = pd.DataFrame({'heights': [48, 24, 51, 12, 21, 
                               41, 25, 23, 32, 61, 
                               19, 24, 29, 21, 23, 
                               13, 32, 18, 42, 18]})
# In[13]:
sample = df.sample(20, replace=True)
display(sample)
print("Mean: %2.2f" % sample.heights.mean())
print("Standard Error: %2.2f" % (sample.heights.std() / np.sqrt(len(sample))))
# In[14]:
xbar = []
for i in range(10000):
    sample = df.sample(20, replace=True)
    xbar.append(sample.heights.mean())
    
print("Mean: %2.1f" % np.mean(xbar))
print("Standard Error: %2.1f" % np.std(xbar))
# In[15]:
df = pd.DataFrame({
    'temp': [22, 36, 36, 38, 44, 45, 47,
             43, 44, 45, 47, 49,
             52, 53, 53, 53, 54, 55, 55, 55, 56, 57, 58, 59,
             60, 61, 61.5, 61.7, 61.7, 61.7, 61.8, 62, 62, 63.4, 64.6,
             65, 65.6, 65.6, 66.4, 66.9, 67, 67, 67.4, 67.5, 68, 69, 
             70, 71, 71, 71.5, 72, 72, 72, 72.7, 73, 73, 73, 73.3, 74, 75, 75, 
             77, 77, 77, 77.4, 77.9, 78, 78, 79,
             80, 82, 83, 84, 85, 85, 86, 87, 88,
             90, 90, 91, 93, 95, 97,
             102, 104],
    'sales': [660, 433, 475, 492, 302, 345, 337,
              479, 456, 440, 423, 269,
              331, 197, 283, 351, 470, 252, 278, 350, 253, 253, 343, 280,
              200, 194, 188, 171, 204, 266, 275, 171, 282, 218, 226, 
              187, 184, 192, 167, 136, 149, 168, 218, 298, 199, 268,
              235, 157, 196, 203, 148, 157, 213, 173, 145, 184, 226, 204, 250, 102, 176,
              97, 138, 226, 35, 190, 221, 95, 211,
              110, 150, 152, 37, 76, 56, 51, 27, 82,
              100, 123, 145, 51, 156, 99,
              147, 54]
})
# In[16]:
# Grab a reference to fig and axes object so we can reuse them
fig, ax = plt.subplots()
# Plot the Thneed sales data
ax.scatter(df.temp, df.sales)
ax.set_xlim(xmin=20, xmax=110)
ax.set_ylim(ymin=0, ymax=700)
ax.set_xlabel('temperature (F)')
ax.set_ylabel('thneed sales (daily)');
# In[17]:
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets)**2).mean())
# In[18]:
# 1D Polynomial Fit
d1_model = np.poly1d(np.polyfit(df.temp, df.sales, 1))
d1_predictions = d1_model(range(111))
ax.plot(range(111), d1_predictions, 
        color=blue, alpha=0.7)
# 2D Polynomial Fit
d2_model = np.poly1d(np.polyfit(df.temp, df.sales, 2))
d2_predictions = d2_model(range(111))
ax.plot(range(111), d2_predictions, 
        color=red, alpha=0.5)
ax.annotate('RMS error = %2.1f' % rmse(d1_model(df.temp), df.sales),
             xy=(75, 650),
             fontsize=20,
             color=blue,
             backgroundcolor='w')
ax.annotate('RMS error = %2.1f' % rmse(d2_model(df.temp), df.sales),
             xy=(75, 580),
             fontsize=20,
             color=red,
             backgroundcolor='w')
display(fig);
# In[19]:
rmses = []
for deg in range(15):
    model = np.poly1d(np.polyfit(df.temp, df.sales, deg))
    predictions = model(df.temp)
    rmses.append(rmse(predictions, df.sales))
    
plt.plot(range(15), rmses)
plt.ylim(45, 70)
plt.xlabel('number of terms in fit')
plt.ylabel('rms error')
plt.annotate('$y = a + bx$', 
             xytext=(14.2, 70), 
             xy=(1, rmses[1]), 
             multialignment='right',
             va='center',
             arrowprops={'arrowstyle': '-|>',
                         'lw': 1,
                         'shrinkA': 10,
                         'shrinkB': 3})
plt.annotate('$y = a + bx + cx^2$', 
             xytext=(14.2, 64), 
             xy=(2, rmses[2]), 
             multialignment='right',
             va='top',
             arrowprops={'arrowstyle': '-|>',
                         'lw': 1,
                         'shrinkA': 35,
                         'shrinkB': 3})
plt.annotate('$y = a + bx + cx^2 + dx^3$', 
             xytext=(14.2, 58), 
             xy=(3, rmses[3]), 
             multialignment='right',
             va='top',
             arrowprops={'arrowstyle': '-|>',
                         'lw': 1,
                         'shrinkA': 12,
                         'shrinkB': 3});
# In[20]:
# Remove everything but the datapoints
ax.lines.clear()
ax.texts.clear()
# Changing the y-axis limits to match the figure in the slides
ax.set_ylim(0, 1000)
# 14 Dimensional Model
model = np.poly1d(np.polyfit(df.temp, df.sales, 14))
ax.plot(range(20, 110), model(range(20, 110)),
         color=sns.xkcd_rgb['sky blue'])
display(fig)
# In[21]:
df_a = df.sample(n=len(df)//2)
df_b = df.drop(df_a.index)
# In[22]:
plt.scatter(df_a.temp, df_a.sales, color='red')
plt.scatter(df_b.temp, df_b.sales, color='blue')
plt.xlim(0, 110)
plt.ylim(0, 700)
plt.xlabel('temprature (F)')
plt.ylabel('thneed sales (daily)');
# In[23]:
# Create a 2-degree model for each subset of data
m1 = np.poly1d(np.polyfit(df_a.temp, df_a.sales, 2))
m2 = np.poly1d(np.polyfit(df_b.temp, df_b.sales, 2))
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, 
                               sharex=False, sharey=True,
                               figsize=(12, 5))
x_min, x_max = 20, 110
y_min, y_max = 0, 700
x = range(x_min, x_max + 1)
# Plot the df_a group
ax1.scatter(df_a.temp, df_a.sales, color='red')
ax1.set_xlim(xmin=x_min, xmax=x_max)
ax1.set_ylim(ymin=y_min, ymax=y_max)
ax1.set_xlabel('temprature (F)')
ax1.set_ylabel('thneed sales (daily)')
ax1.plot(x, m1(x),
         color=sns.xkcd_rgb['sky blue'],
         alpha=0.7)
# Plot the df_b group
ax2.scatter(df_b.temp, df_b.sales, color='blue')
ax2.set_xlim(xmin=x_min, xmax=x_max)
ax2.set_ylim(ymin=y_min, ymax=y_max)
ax2.set_xlabel('temprature (F)')
ax2.plot(x, m2(x),
         color=sns.xkcd_rgb['rose'], 
         alpha=0.5);
# In[24]:
print("RMS = %2.1f" % rmse(m1(df_b.temp), df_b.sales))
print("RMS = %2.1f" % rmse(m2(df_a.temp), df_a.sales))
print("RMS estimate = %2.1f" % np.mean([rmse(m1(df_b.temp), df_b.sales),
                                        rmse(m2(df_a.temp), df_a.sales)]))
# In[25]:
rmses = []
cross_validated_rmses = []
for deg in range(15):
    # df_a the model on the whole dataset and calculate its
    # RMSE on the same set of data
    model = np.poly1d(np.polyfit(df.temp, df.sales, deg))
    predictions = model(df.temp)
    rmses.append(rmse(predictions, df.sales))
    
    # Use cross-validation to create the model and df_a it
    m1 = np.poly1d(np.polyfit(df_a.temp, df_a.sales, deg))
    m2 = np.poly1d(np.polyfit(df_b.temp, df_b.sales, deg))
    
    p1 = m1(df_b.temp)
    p2 = m2(df_a.temp)
    
    cross_validated_rmses.append(np.mean([rmse(p1, df_b.sales), 
                                          rmse(p2, df_a.sales)]))
    
plt.plot(range(15), rmses, color=blue, 
         label='RMS')
plt.plot(range(15), cross_validated_rmses, color=red, 
         label='cross validated RMS')
plt.ylim(45, 70)
plt.xlabel('number of terms in fit')
plt.ylabel('rms error')
plt.legend(frameon=True)
plt.annotate('Best model minimizes the\ncross-validated error.', 
             xytext=(7, 60), 
             xy=(2, cross_validated_rmses[2]), 
             multialignment='center',
             va='top',
             color='blue',
             size=25,
             backgroundcolor='w',
             arrowprops={'arrowstyle': '-|>',
                         'lw': 3,
                         'shrinkA': 12,
                         'shrinkB': 3,
                         'color': 'blue'});