# plot_g09_irc
This script reads in a Gaussian09 output file from an IRC calculation and plots the IRC (correct order), as well as extracts the geometries (xyz) in the correct order.\

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
The <emph><order></emph> is either <emph>react-prod</emp> or <emph>prod-react</emph>
