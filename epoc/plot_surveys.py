"""
Barplots for DLQ and LuCiD scales.

Outputs two versions
1. horizontal bars of two subjects (sep DLQ and LuCiD)
2. regular plots of all three subjects (all individual plots)
"""


import yaml
from glob import glob
import matplotlib #; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scale_axislabels import DLQ, LuCiD


YTICKLABELS = dict(DLQ=DLQ,LuCiD=LuCiD)


fnames = sorted(glob('../data/*/*/*questionnaire.yaml'))

SURVEYS = ['DLQ','LuCiD']


class Subject(object):
    def __init__(self,subj_id):
        self.id = subj_id
        self.fname = FNAMES[subj_id]
        with open(self.fname) as f:
            self.data = yaml.load(f)#,Loader=yaml.FullLoader)


# horizontal barplots
for survey_id in SURVEYS:
    fig, axes = plt.subplots(1,2,figsize=(4,6))
    for subj_id, ax in zip(HORZ_SUBJ_ORDER,axes):
        subj = Subject(subj_id)
        x = subj.data[survey_id]
        y = range(len(x))
        ax.barh(y,x,color='silver')
        ax.invert_yaxis()
        ax.set_xticks(range(max(x)+1))
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        if ax == axes[0]:
            ax.spines['left'].set_visible(False)
            ax.invert_xaxis()
        elif ax == axes[1]:
            ax.spines['right'].set_visible(False)
    for extension in ['.svg','.png']:
        fname = '../results/'+survey_id+extension
        plt.savefig(fname,dpi=300,bbox_inches='tight')
    plt.close()

    
# individual barplots
for survey_id in SURVEYS:
    for fn in fnames:
        # load questionnaire
        with open(fname) as f:
            data = yaml.load(f,Loader=yaml.FullLoader)

        subj = Subject(subj_id)
        self.id = subj_id
        self.fname = FNAMES[subj_id]
        fig, ax = plt.subplots(figsize=(5,5))
        x = subj.data[survey_id]
        y = range(len(x))
        ax.barh(y,x,color='silver')
        ax.invert_yaxis()
        ax.set_xticks(range(max(x)+1))
        ax.set_yticks(y)
        ax.set_yticklabels([ 'Q'+str(i+1) for i in y ])
        # ax.set_yticklabels(YTICKLABELS[survey_id])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        for extension in ['.svg','.png']:
            # fname = f'../results/{subj_id}-{survey_id}{extension}'
            fname = '../results/'+subj_id+'-'+survey_id+extension
            plt.savefig(fname,dpi=300,bbox_inches='tight')
        plt.tight_layout()
        plt.close()