"""
Plot the activation values overlayed
on the null distributions for the two
successful task completions.

One figure with two axes. One axis overlays
test scores on the raw "null" distribution,
and the other on the bootstrapped distribution.
"""
import glob
import pandas as pd

import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sea

import pyplotparams


# unique plot parameters
DISTRN_COLOR = 'lightgray'
HZ_WIDTH = 0.1 # of horizontal bar marking mean test values


DERIV_DIR = '../data/derivatives'

# segment files for plotting the raw distribution
seg_fnames = glob.glob(f'{DERIV_DIR}/*/*/*segmentation.tsv')
# bootstrap files for the bootstrapped null distribution
bootstrap_fnames = glob.glob(f'{DERIV_DIR}/*/*/*nulldistribution.tsv')

# load segmentation files, adding subj column
seg_df_list = []
for infn in seg_fnames:
    subj_id = glob.os.path.basename(infn)[:7]
    subj_df = pd.read_csv(infn,sep='\t')
    subj_df['subj'] = subj_id
    seg_df_list.append(subj_df)
seg_df = pd.concat(seg_df_list)

# redo the activation conversion from secs -> proportion
seg_df['activation'] = seg_df['activation_secs'] / 8.

# no need to concat bootstrap files
boot_dfs = { glob.os.path.basename(infn)[:7] : 
                pd.read_csv(infn,sep='\t')
             for infn in bootstrap_fnames }

# get an ordered list of subjects for x-axis
subj_order = seg_df['subj'].sort_values().unique().tolist()


# open figure with both axes
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(12,6),
                              gridspec_kw={'width_ratios':[1,2]})

# draw bootstrapped distributions on first axis...
violin_data = pd.np.hstack([boot_dfs[subj_order[0]],
                            boot_dfs[subj_order[1]]])
viols = ax1.violinplot(violin_data,positions=[0,1],
                       widths=[.5,.5],
                       showextrema=False)
plt.setp(viols['bodies'],
        facecolor=DISTRN_COLOR,
        edgecolor='white')

# ...and raw on second
sea.swarmplot(data=seg_df[seg_df['post_EM']==False],
              x='subj',y='activation',
              color='lightgray',size=6,
              edgecolor='white',linewidth=.2,
              order=subj_order,ax=ax2)


## plot the test values on both axes
(_,s3testvals), (_,s4testvals) = \
    seg_df[seg_df['post_EM']==True].groupby('subj')['activation']
for ax in [ax1,ax2]:
    # two test values per subject
    ax.plot([0,0,1,1],pd.np.ravel([s3testvals,s4testvals]),
        markerfacecolor='k',markeredgecolor='white',
        linestyle='none',markeredgewidth=1,
        marker='o',markersize=10,zorder=99)
    # one mean test value per subject
    ax.hlines(y=s3testvals.mean(),xmin=0-HZ_WIDTH/2,xmax=0+HZ_WIDTH/2,
              linestyle='-',linewidth=1,color='k',zorder=100)
    ax.hlines(y=s4testvals.mean(),xmin=1-HZ_WIDTH/2,xmax=1+HZ_WIDTH/2,
              linestyle='-',linewidth=1,color='k',zorder=100)

# aesthetics
for ax in [ax1,ax2]:
    ax.set_xlim(-.5,1.5)
    ax.set_ylim(0,1)
    ax.set_yticks([0,.2,.4,.6,.8,1])
    ax.set_yticks(pd.np.linspace(0,1,21),minor=True)
    ax.set_xticks([0,1])
    ax.set_xticklabels(subj_order)
    ax.set_xlabel('Participant')
    ax.set_ylabel('Mental command detection')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()

# export
for extension in ['png','svg','eps']:
    out_fname = f'{DERIV_DIR}/activations.{extension}'
    plt.savefig(out_fname)
plt.close()
