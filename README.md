# dreambci-epoc

Code for a pilot study where an Emotiv EPOC was used to test if a waking-trained brain-computer interface could be controlled during sleep from a lucid dream.

Details available in the manuscript [preprint](https://doi.org/10.31219/osf.io/my3tq).

I only used the video of the Emotiv software to determine success, so this is mostly just plotting scripts.

1. Run `stats-bootstrap.py` once to perform bootstrap analysis on all the successful LD task attempts.
2. Run `plot-activation.py` to plot both successful LD task attempts on a single figure (raw and bootstrapped results on separates axes). This requires `stats-bootstrap.py` to already have been run, since it plots the output.
3. Run `plot-scales.py` to plot the DLQ and LuCiD scale results from each succesful LD task attempt.

### Notes
* `pyplotparams.py` is never called, but used as a configuration file for both plotting files.
* `print_edf_length.py` is just a scrap file I used temporarily.