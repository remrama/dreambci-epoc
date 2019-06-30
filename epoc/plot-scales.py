"""
(Horizontal) barplots for DLQ and LuCiD scales.

One 2x3 figure, 2 scale rows and 3 subject columns.
Note 3 subjects is more than the 2 of main
activation plot because one subject did the
task but computer didn't record the EPOC results :|
"""
import glob
import json

import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt; plt.ion()

import pyplotparams


# unique plot parameters
SCALE_ORDER = ['DLQ','LuCiD']
SUBJECT_ORDER = ['sub-001','sub-003','sub-004']
SCALE_COLORS = dict(DLQ='silver',LuCiD='silver')


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

plt.tight_layout()

# export
for extension in ['png','svg','eps']:
    out_fname = f'{DERIV_DIR}/scales.{extension}'
    plt.savefig(out_fname)
plt.close()