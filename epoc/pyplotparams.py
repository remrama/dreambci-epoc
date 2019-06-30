"""
Import at top of any plot scripts to change
defaults and be consistent across plots.
"""
import matplotlib

# change default parameters
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Arial'
matplotlib.rcParams['axes.labelsize'] = 'x-large'
matplotlib.rcParams['xtick.labelsize'] = 'large'
matplotlib.rcParams['ytick.labelsize'] = 'large'
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['legend.fontsize'] = 'small'
matplotlib.rcParams['legend.title_fontsize'] = 'medium'
matplotlib.rcParams['savefig.dpi'] = 300
# matplotlib.rcParams['svg.fonttype']