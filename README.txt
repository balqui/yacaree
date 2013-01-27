Readme file for yacaree version 1.2.1 - January 27, 2011

JL Balcazar - UPC

Thanks for downloading yacaree: yet another closure-based
association rules exploration environment.

Use it to explore association rules and partial implications
on transactional datasets; yacaree will attempt on its own
to tune internal parameters to try and offer you as useful
output as possible.

You may wish to check as well the Java version of yacaree 1.1 
included in the KNIME Open Source Data Mining Suite: see STARK
under Community Contributions in the KNIME Labs.

Disclaimer: whereas each line of code has been written in good will, 
absolutely no guarantees, whether explicit or implicit, are made 
about this software, and, if you download and run it, the authors 
claim to have no responsibility whatsoever on the outcome of the run.

This version has not yet been ported to Python 3.*.

The tarball does not require any installation, as it only uses 
libraries that come with all standard distributions of Python. 
Uncompressing provides all necessary source code plus a data 
folder with examples of datasets. Some files come originally 
from the ML repository in UCI, Irvine, US, and have been translated 
through simple scripts into transactional form (votes, cmc, mushroom, 
and adult - for this dataset, the training set file only). File
markbask is a slight variation of one used to be distributed as 
example with the Clementine software, with the advantage that 
there are in it clear sorts of buyers. File papersTr is a somewhat 
cleaned file (stopword and punctuation removal) from the abstracts 
of the e-prints research report server of the Pascal Network of 
Excellence, covering up to 2006. File NOW (Neogene of the Old World, 
based on the public release 030717) is a transactional version 
of a part of an archeological mammal fossile dataset, available 
at: http://www.helsinki.fi/science/now/

To run yacaree, you need a transactional dataset encoded as follows: 
each transaction comes in a line by itself, and consists of items 
separated by spaces. There should be no transaction identifiers. 
Items are arbitrary strings of printable characters but they cannot 
contain blank spaces, as these act as item separators.

Use your Python installation to run the main source yacaree.py 
and then a GUI should open. Once the computation finishes, 
the info in the console (plus a bit of timing) and the output 
rules will be found in the respective log and rules files; 
their names start with the same name as the dataset, and include 
in the name the date and the time of the run, so that they will 
appear ordered if several runs are made on the same dataset.
The exploration of some datasets may take several minutes.

Opening with an IDE or text editor the file statics.py allows you
to modify some parameters. For the changes to take effect, you must
save the modified file and make sure that Python reloads it (this
may be nontrivial but closing all Python windows and opening yacaree 
again should work; PythonWin has a "reload" button that usually 
works too).

If your run threw a Python exception reporting "Memory error", 
then you are likely to need to reduce the pend_mem_limit from 
the current value (near 1GB) to a value in accordance with the 
availability in your platform. Alternatively, you can increase 
confthr (the confidence threshold) or initialboost (the highest 
confidence boost threshold employed), or absoluteboost (the lowest 
confidence boost threshold allowed), or genabsupp in case you 
definitely want rules having less than 5 supporting transactions. 
Feel free to experiment with these and other parameters, as 
"yacaree" means Yet Another Closure-based Association Rule 
Experimentation Environment.

Enjoy!


Major differences of version 1.2.1 with version 1.1 are as follows:

a/ Full implications, of confidence 1, are processed and chosen
according to their confidence boost together with partial implications.

b/ A choice is made whether to ask for only 50 rules as before, or
for all rules that pass the thresholds.

c/ Some small details have been adjusted; in particular, the way 
version 1.2.0alpha approximated the support ratio at the negative
border has been reverted to that in version 1.1.


Major differences of version 1.1 with version 1.0 are as follows:

a/ The iPred algorithm is used to construct the lattice, instead
of the border algorithm (see the discussion in Balcazar and 
Tirnauca 2011); it is clearly faster although the savings are not 
too impressive. It also saves a bit of work at the time of pushing
the confidence boost constraint through support ratios.

b/ The closure miner has been deeply refactored. A new variant of 
special-purpose heap has been employed, and the tests that control 
its size have been reduced a bit and accelerated.

Some minor additional changes include:

c/ The absolute confidence threshold is now at 0.65.

d/ Rule lift and other quantities are reported (and a tiny typo fixed).

e/ Confidence boost decreases will be always noticeable, even if slight.

f/ Some minor details (such as method names inconsistent with standard
Python coding policies, or a slightly better reporting along the way) 
were further adjusted.

