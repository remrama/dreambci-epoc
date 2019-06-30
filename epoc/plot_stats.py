
import numpy as np
import pandas as pd

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()
from matplotlib import rcParams

sea.set_context('poster')
rcParams['axes.labelsize'] = 'large'
rcParams['xtick.labelsize'] = 'large'
rcParams['ytick.labelsize'] = 'large'


in_fname = '../results/chunk_stats-long.csv'


df = pd.read_csv(in_fname)

# convert seconds to "proportion of 8-sec frame"
df['activation'] = df['activation'] / 8.


# fig, ax = plt.subplots(figsize=(10,8))
# ax = sea.swarmplot(data=df,x='subj',y='activation',hue='after_flick',
#     palette={0:'lightgray',1:'black'},size=10)


# run stats on each subj
s1null, s1test, s2null, s2test = [ tup[1] for tup in
    df.groupby(['subj','after_flick']).activation ]


#### before bootstrapping, plot the raw distributions
fig, ax = plt.subplots(figsize=(9,9))

ax = sea.swarmplot(data=df[df.after_flick==False],
    x='subj',y='activation',
    color='lightgray',size=8,
    ax=ax)
ax = sea.swarmplot(data=df[df.after_flick==True],
    x='subj',y='activation',
    color='black',size=14,
    ax=ax)

ax.axhline(0,ls='--',linewidth=.5,color='k')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.ylim(ax.get_ylim()[0],1)
plt.tight_layout()

ex_fname = '../results/plot-raw.eps'
plt.savefig(ex_fname,dpi=300)
plt.close()




# create bootstrapped null distributions for each subject
N_BOOTS = 10000
s1null_bs = np.random.choice(s1null,size=N_BOOTS,replace=True)
s2null_bs = np.random.choice(s2null,size=N_BOOTS,replace=True)


# get a p-value of proportion of null higher than test
pval1 = (s1null_bs > s1test.mean()).mean()
pval2 = (s1null_bs > s2test.mean()).mean()
# also print the spread of null distributions

# also print the mean of the test values


print '\nSubj 1'
print '\tp={:f}'.format(pval1)
print '\ttestval_mean={:f}'.format(s1test.mean())
print '\tnulldistrn_SD={:f}'.format(s1null_bs.std())
print '\tnulldistrn_CI=({:f},{:f})'.format(np.percentile(s1null_bs,5),
                                           np.percentile(s1null_bs,95))
print '\nSubj 2'
print '\tp={:f}'.format(pval2)
print '\ttestval_mean={:f}'.format(s2test.mean())
print '\tnulldistrn_SD={:f}'.format(s2null_bs.std())
print '\tnulldistrn_CI=({:f},{:f})'.format(np.percentile(s2null_bs,5),
                                           np.percentile(s2null_bs,95))



# plot the null distributions
fig, ax = plt.subplots(figsize=(6,7))

viols = ax.violinplot([s1null_bs,s2null_bs],
    positions=[0,1],
    # widths=[.125,.125],
    showextrema=False)
plt.setp(viols['bodies'],facecolor='lightgray',edgecolor='white')

# plot the individual test values
plt.plot([0,0],s1test,
    marker='o',linestyle='none',color='k')
plt.plot([1,1],s2test,
    marker='o',linestyle='none',color='k')
# plot the mean test values
HZ_WIDTH = 0.1
plt.hlines(y=s1test.mean(),xmin=0-HZ_WIDTH/2,xmax=0+HZ_WIDTH/2,
    linestyle='--',linewidth=1,color='k')
plt.hlines(y=s2test.mean(),xmin=1-HZ_WIDTH/2,xmax=1+HZ_WIDTH/2,
    linestyle='--',linewidth=1,color='k')

plt.xlim(-.5,1.5)
plt.ylim(0,1)
plt.yticks(np.linspace(0,1,6))
plt.xticks([0,1],['RAB','XAN'])
plt.ylabel('Mental command detection')
plt.xlabel('Participant')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()


ex_fname = '../results/plot-bootstraps.svg'
plt.savefig(ex_fname,dpi=300)
plt.close()



# # create new dataframe for plotting
# newdf = pd.DataFrame({
#     'subj': np.append(np.repeat(1,N_BOOTS),np.repeat(2,N_BOOTS)),
#     'activation': np.append(s1null_bs,s2null_bs),
#     })

# # # plot with histogram and vertical markers
# # plt.hist(nullvals)
# # _ = [plt.axvline(x) for x in testvals ]

# # swarmplot is too much for the large amount of bootstraps
# fig, ax = plt.subplots(figsize=(9,9))
# ax = sea.violinplot(data=newdf,
#     x='subj',y='activation',
#     color='lightgray',
#     ax=ax)




