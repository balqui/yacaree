
Readme file for yacaree version 1.1 - November 4, 2011 - JL Balcazar - Uni Cantabria

Thanks for downloading yacaree. Current version 1.1 is offered under 
the MIT X11 open source license, sometimes called MIT License, that 
can be easily found in e.g. Wikipedia. Disclaimer: whereas each line
of code has been written in good will, absolutely no guarantees, 
whether explicit or implicit, are made about this software, and, 
if you download and run it, the authors claim to have no responsibility 
whatsoever on the outcome of the run.

Major differences with version 1.0 are as follows:

a/ The iPred algorithm is used to construct the lattice, instead
of the border algorithm (see the discussion in Balcazar and 
Tirnauca 2011); it is clearly faster although the savings are not 
too impressive. It also saves a bit of work at the time of pushing
the confidence boost constraint through support ratios.

b/ The closure miner has been deeply refactored. A new variant of 
special-purpose heap has been employed, and the tests that control 
its size have been reduced a bit and accelerated.

Some minor additional changes include:

c/ The absolute confidence threshold is now at 0.6 to see how well this goes.

d/ Rule lift and other quantities are reported (and a tiny typo fixed).

e/ Confidence boost decreases will be always noticeable, even if slight.

f/ Some minor details (such as method names inconsistent with standard
Python coding policies, or a slightly better reporting along the way) 
were adjusted.

You may wish to check whether a version of yacaree is included in the
KNIME Open Source Data Mining Suite. We are working at it and will be
ready soon.


Readme file for yacaree version 1.0 - July 29, 2010 - JL Balcazar - Uni Cantabria

Thanks for downloading yacaree. Current version 1.0 is offered under 
the MIT X11 open source license, sometimes called MIT License, that 
can be easily found in e.g. Wikipedia. Disclaimer: whereas each line
of code has been written in good will, absolutely no guarantees, 
whether explicit or implicit, are made about this software, and, 
if you download and run it, the author claims to have no responsibility 
whatsoever on the outcome of the run.

Version 1.0 of yacaree requires Python version 2.6; it may run 
under Python 2.7. Future versions of yacaree will be compatible 
with Python 3.* but the present one is not.

The tarball does not require any installation, as it only uses libraries
that come with all standard distributions of Python. As it uses the Tkinter
library for the GUI, occassional incompatibilities might arise with 
certain Tkinter-based Python IDEs, although the author of yacaree has
not suffered ever any.

Uncompressing provides all necessary source code plus a data folder with
examples of datasets. To run yacaree, you need a transactional dataset
encoded as follows: each transaction comes in a line by itself, and
consists of items separated by spaces. There should be no transaction 
identifiers. Items are arbitrary strings of printable characters but
they cannot contain blank spaces, as these act as item separators.

The tarball includes some examples. Some files come originally from 
the ML repository in UCI, Irvine, US, and have been translated through 
simple scripts into transactional form (votes, cmc, mushroom, and 
adult - for this dataset, the training set file only). Note that
mushroom does not bring actual real-world observations but hypothetical
ones, as indicated in the accompanying documentation in UCI. File
markbask is a slight variation of one used to be distributed as example 
with the Clementine software, with the advantage that there are in it
clear sorts of buyers. File papersTr is a somewhat cleaned file 
(stopword and punctuation removal) from the abstracts of the e-prints 
research report server of the Pascal Network of Excellence, covering 
up to 2006. File NOW (Neogene of the Old World, based on the public 
release 030717) is a transactional version of a part of an archeological 
mammal fossile dataset, available from: http://www.helsinki.fi/science/now/

The exploration of NOW and markbask takes just seconds, adultrain and 
papersTr need two to five minutes, and the rest may take up to 10 or 12
minutes.

Use your Python installation to run the main source yacaree.py and then
a GUI should open allowing you to either Finish, or Choose an input
dataset, through the corresponding buttons. Doing so enables also 
the "Run" button. Clicking on it disables the "Finish" button (if you
need to kill the window use the standard means) and starts yacaree;
the console will report occassionally about what is going on. Ignore
potential indications that the Python and yacaree windows "become 
nonresponsive" or whatever ("No responde" in Spanish), as this is
normal: some datasets require intensive computation and the GUI is 
only listened to infrequently.

Once the computation finishes, the info in the console (plus a bit
of timing) and the output rules will be found in the respective log
and rules files; their names start with the same name as the dataset, 
and include in the name the date and the time of the run, so that
they will appear ordered if several runs are made on the same dataset.
The "Run" button becomes disabled and the user can either Finish or
Choose a dataset again.

Some paragraphs for the data mining aficionado follow.

Opening with an IDE or text editor the file statics.py allows you
to modify some parameters. For the changes to take effect, you must
save the modified file and make sure that Python reloads it (this
may be nontrivial but closing all Python windows and opening yacaree 
again should work; PythonWin has a "reload" button that usually 
works too).

If your run threw a Python exception reporting "Memory error", 
then you are likely to need to reduce the pend_mem_limit from the 
current value (near 1GB) to a value in accordance with the availability
in your platform. Also, you may wish to set maxrules to 0 if you 
wish all the rules found to appear in the output file. 

Alternatively, you can increase confthr (the confidence threshold) 
or initialboost (the highest confidence boost threshold employed), 
or absoluteboost (the lowest confidence boost threshold allowed), 
or genabsupp in case you definitely want rules having less than 5 
supporting transactions. It is not recommended to modify any of
the other parameters, but feel free to experiment, as "yacaree"
means Yet Another Closure-based Association Rule Experimentation
Environment.

Enjoy!
