# plot_g09_irc
This script reads in a Gaussian09 output file from an IRC calculation and plots the IRC (correct order), as well as extracts the geometries (xyz) in the correct order.

Requirements:
```
cclib
numpy
matplotlib.pyplot
seaborn
```
Run:
```
./plot_irc.py <gaussian log file> <order>
```
The *<order>* is either *react-prod* or *prod-react*.
