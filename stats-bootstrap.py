"""
Run stats on the two participants
who have video recorded for performing
the task in the lucid dream.

Loops over each subject to perform
analysis individually for each.

Uses segmentation files which were
manually made from the video.

Export bootstrap distributions as
tsv files for plotting.
"""
import glob
import json
import pandas as pd


N_RESAMPLES = 10000

DERIV_DIR = '../data/derivatives'
fnames = glob.glob(f'{DERIV_DIR}/*/*/*segmentation.tsv')


# loop over successful task sessions
for infn in fnames:

    # load data
    df = pd.read_csv(infn,sep='\t')

    # convert seconds to "proportion of 8-sec frame"
    df['activation'] = df['activation_secs'] / 8.

    # resample from the segments that did not follow LRLR eye movements
    bootstraps = df.query('post_EM==False'
        )['activation'].sample(N_RESAMPLES,replace=True
        ).rename('null_activation')

    # export null distribution for plotting
    bootstrap_outfn = infn.replace('_segmentation','_nulldistribution')
    bootstraps.to_csv(bootstrap_outfn,index=False,header=True,sep='\t')

    # get the mean of 2 post-EM segments
    test_scores = df.loc[df['post_EM'],'activation'].tolist()
    mean_test_score = pd.np.mean(test_scores)

    # get a p-value of proportion of null higher than test
    pval = pd.np.append((bootstraps > mean_test_score),True).mean()

    # get 95% confidence interval for null distribution
    null_ci = bootstraps.quantile([.025,.975]).tolist()

    # get the timestamp (of .MOV file) where LRLR eye movement occurs
    lrlr_timestamp = df.loc[df['post_EM'].idxmax(),'segment_start']
    
    # extract identifying info
    subject, session, run = glob.os.path.basename(infn).split('_')[:3]

    # create results payload
    results = {
        'subject'              : subject,
        'session'              : session,
        'run'                  : run,
        'lrlr_timestamp'       : lrlr_timestamp,
        'test_scores'          : test_scores,
        'mean_test_score'      : mean_test_score,
        'null_distribution_ci' : null_ci,
        'pvalue'               : pval
    }

    # export results
    results_outfn = infn.replace('_segmentation.tsv','_results.json')
    with open(results_outfn,'w') as outfile:
        json.dump(results,outfile,ensure_ascii=False,indent=4)