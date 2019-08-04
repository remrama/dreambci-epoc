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


DATA_DIR  = '../data'
DERIV_DIR = '../data/derivatives'

fnames = glob.glob(f'{DATA_DIR}/*/*/*wakesurvey.json')

# unique plot parameters
SCALE_ORDER = ['DLQ','LuCiD']
SUBJECT_ORDER = ['sub-001','sub-003','sub-004']
DLQ_COLOR = 'silver'
LuCiD_CMAP = 'Pastel2'

# put scale questions on yaxis for DLQ but LuCiD's are too long
# (also these are shorthand for the DLQ probes)
YTICKLABELS = {
    'DLQ': [
        'I was aware that I was dreaming.',
        'I was aware that my physical body was asleep.',
        'I was aware that my dream characters weren\'t real.',
        'I chose one action instead of another.',
        'I was aware that dream objects were not real.',
        'I changed dream events the way I wanted.',
        'I recalled facts from waking life.',
        'I changed dream characters the way I wanted.',
        'I broke physical laws of waking reality.',
        'I changed the dream scene the way I wanted.',
        'I thought about possibilities of what I could do.',
        'I remembered intentions of what I wanted to do.'
    ],
    'LuCiD': [
        'I was aware that was I was experiencing was not real.',
        'I remembered my intention to do certain things.',
        'I was aware the my dream self was not my waking self.',
        'I was able to control other dream characters.',
        'I thought about other dream characters.',
        'I was able to perform supernatural actions.',
        'The emotions I experienced were the same as they would be during wakefulness.',
        'I was aware that my dream body did not correspond to my waking body.',
        'I was certain my dream experiences had no consequences on the real world.',
        'I was able to control the dream environment.',
        'I saw myself from the outside.',
        'I thought about my own actions.',
        'I felt that I had forgotten something important.',
        'I was able to change or move objects unlike in waking.',
        'I was not myself but a completely different person.',
        'I often asked myself whether I was dreaming.',
        'The thoughts I had were the same as I would have during wakefuless.',
        'I had the feeling that I could remember my waking life.',
        'I was aware that other dream characters were not real.',
        'Most things could have also happened during wakefulness.',
        'I watched the dream from the outside, as if on a screen.',
        'I often thought about the things I was experiencing.',
        'I was able to influence the storyline of my dreams.',
        'I was able to remember certain plans for the future.',
        'I felt euphoric/upbeat.',
        'I had strong negative feelings.',
        'I had strong positive feelings.',
        'I felt very anxious.'
    ]
}

# make a color scheme for the LuCiD factors
LuCiD_ORDER = ['insight','control','thought','realism','memory',
               'dissociation','neg_emotion','pos_emotion']
LuCiD_COLORS = OrderedDict( # ordered for legend
    [ (factor, plt.get_cmap(LuCiD_CMAP).colors[i])
        for i, factor in enumerate(LuCiD_ORDER) ])
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
        # pad the zeros a bit to emphasize
        responses = [ .05 if r==0 else r for r in responses ]
        barwidth = .8
        ax.barh(xvals,responses,color=SCALE_COLORS[scale],
                height=barwidth,linewidth=.5,edgecolor='k')

        # aesthetics
        ax.set_yticks(xvals) # because barhorizontal
        # if scale == 'DLQ':
        #     yticklabels = DLQ_YTICKS
        # else:
        #     yticklabels = [ f'{scale}-{i+1:02d}' for i in xvals ]
        yticklabel_fontsize = 'xx-small' if scale=='LuCiD' else 'small'
        if axcol == 0:
            ax.set_yticklabels(YTICKLABELS[scale],fontsize=yticklabel_fontsize)
        else:
            ax.set_yticklabels([])
        ax.invert_yaxis()
        ax.set_xticks(range(max(responses)+1))
        # ax.set_xlim(-.05,max(responses)+.05)
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