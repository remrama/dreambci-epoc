"""
(Horizontal) barplots for DLQ and LuCiD scales.

One 2x3 figure, 2 scale rows and 3 subject columns.
Note 3 subjects is more than the 2 of main
activation plot because one subject did the
task but computer didn't record the EPOC results :|
"""
import glob
import json
from collections import OrderedDict

import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt; plt.ion()
from matplotlib.patches import Patch

import pyplotparams


# override plot yticksize bc so many on LuCiD plots
matplotlib.rcParams['ytick.labelsize'] = 'small'

# unique plot parameters
SCALE_ORDER = ['DLQ','LuCiD']
SUBJECT_ORDER = ['sub-001','sub-003','sub-004']
DLQ_COLOR = 'silver'

# make a color scheme for the LuCiD factors
LuCiD_COLORS = OrderedDict([ # ordered for legend
    ('insight',       'cornflowerblue'),
    ('control',       'powderblue'),
    ('thought',       'plum'),
    ('realism',       'sandybrown'),
    ('memory',        'gold'),
    ('dissociation',  'palevioletred'),
    ('neg_emotion',   'lightcoral'),
    ('pos_emotion',   'lightgreen')
])
LuCiD_FACTORS = {
    'insight':       [1,3,8,9,16,19],
    'control':       [4,6,10,14,23],
    'thought':       [5,12,22],
    'realism':       [7,17,20],
    'memory':        [2,13,18,24],
    'dissociation':  [11,15,21],
    'neg_emotion':   [26,28],
    'pos_emotion':   [25,27]
}
# clean up this shitshow by making a
# list of 27 colors, one for each LuCiD probe
LuCiD_colorcodes = []
for i in range(27):
    quest_num = i+1
    for factor, question_numbers in LuCiD_FACTORS.items():
        if quest_num in question_numbers:
            LuCiD_colorcodes.append(LuCiD_COLORS[factor])
# and finally a dict to choose from during plotting
SCALE_COLORS = dict(DLQ=DLQ_COLOR,LuCiD=LuCiD_colorcodes)


DATA_DIR  = glob.os.path.expanduser('~/DBp/proj/bcilu/EPOC/data')
DERIV_DIR = glob.os.path.expanduser('~/DBp/proj/bcilu/EPOC/derivatives')

fnames = glob.glob(f'{DATA_DIR}/*/*/*wakesurvey.json')

# load data into a nest dict { subj: {scale: values} }
data = {}
for infn in fnames:
    with open(infn) as infile:
        jd = json.load(infile)
    data[jd['participant']] = dict(DLQ=jd['DLQ'],LuCiD=jd['LuCiD'])


# open figure
fig, axes = plt.subplots(2,3,figsize=(12,6))

# loop over subjects and scales
for subj, scale_dict in data.items():
    axcol = SUBJECT_ORDER.index(subj)
    for scale, responses in scale_dict.items():
        axrow = SCALE_ORDER.index(scale)
        ax = axes[axrow,axcol]

        # draw bars
        xvals = range(len(responses))
        ax.barh(xvals,responses,color=SCALE_COLORS[scale])

        # aesthetics
        ax.invert_yaxis()
        ax.set_yticks(xvals) # because barhorizontal
        ax.set_yticklabels([ f'{scale}-{i+1:02d}' for i in xvals ],
                           rotation=25)
        ax.set_xticks(range(max(responses)+1))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.grid(True,axis='x',which='major',linestyle='--',linewidth=.25,color='k',alpha=1)
        if axrow == 0:
            ax.set_title(subj)

# legend
legend_handles = [ Patch(facecolor=color,label=factor)
                   for factor, color in LuCiD_COLORS.items() ]
plt.legend(handles=legend_handles,title='LuCiD factors',
           loc='upper left',frameon=False,bbox_to_anchor=(1,1))

plt.tight_layout()

# export
for extension in ['png','svg','eps']:
    out_fname = f'{DERIV_DIR}/scales.{extension}'
    plt.savefig(out_fname)
plt.close()