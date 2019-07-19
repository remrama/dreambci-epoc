"""
Print the length of an EPOC+ TestBench file.
"""
from mne.io import read_raw_edf

SUBJ = 'sub-003'
SESS = 'ses-002'
stamp = '20151115T134018'

datadir = '../data'
fname = f'{datadir}/{SUBJ}/{SESS}/{SUBJ}_{SESS}_testbench-{stamp}.edf'

edf = read_raw_edf(fname)

true_len = edf.times[-1]
predicted_len = edf.times.shape[0] * (1/edf.info['sfreq'])

assert abs(true_len-predicted_len) < 0.5

print('=======================')
print(f'EDF file is {true_len:.1f} seconds ({true_len/60:.1f} min) long.')