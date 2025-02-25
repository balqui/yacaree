"""
yacaree

Current revision: late Frimaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Old, to check out: "Close" button does not always work, I believe 
already in the frozen version. CAVEAT.

Heavily refactored to bring here all interfaces and take them 
out of statics.py

Usage (to be reviewed):

report*: outputs a string message, prepends a line break,
 variants for warnings and errors
ask_input: user communication
openfile, storefilename: to set up the data source
go: calls run method of main program
others: to handle the communication with Tk

Can one combine decorator @classmethod with @property-related?

"""


from datetime import datetime
from time import sleep, time as clock
from filenames import FileNames

# ~ # Had this when it was necessary to fly under both Python 2 and 3
# ~ try:
    # ~ "Python 2 version - all these imports only for gui"
    # ~ import Tkinter
    # ~ import tkFileDialog
    # ~ import tkFont
# ~ except ModuleNotFoundError:
    # ~ "Python 3 (or beyond?) version"
    # ~ import tkinter as Tkinter
    # ~ from tkinter import filedialog as tkFileDialog
    # ~ from tkinter import font as tkFont

import tkinter as Tkinter
from tkinter import filedialog as tkFileDialog
from tkinter import font as tkFont

class IFace:

    version = "2.0.0"  # OK TO HAVE THIS HERE?

    report_period = 30 # seconds between possibly_report calls

    fn = None          # filename slot

    _gui = False

    @property
    def gui(self):
        return type(self)._gui

    @gui.setter
    def gui(self, val):
        type(self)._gui = bool(val)

    datafile = None
    logfile = None
    rulesfile = None

    _running = False

    @property
    def running(self):
        return type(self)._running

    @running.setter
    def running(self, val):
        type(self)._running = bool(val)

    @classmethod
    def go(cls, yacaree):
        """
        Might try to move bindings to a regular __init__()
        (this could not be done in the earlier structure).
        But can't have only hpar as argument, need also 
        standard_run and standard_run_all already existing
        so as to bind the buttons to.
        """
        cls.hpar = yacaree.hpar
        cls.fn = FileNames(cls)

        if cls._gui:

            cls.root = Tkinter.Tk()

            button_width = 35
            button_height = 4
            text_width = 92
            text_height = 28

            left_frame = Tkinter.Frame(cls.root)
            left_frame.pack(side=Tkinter.LEFT)
            logo = Tkinter.BitmapImage(file="yac-v03.xbm")
            logo_frame = Tkinter.Frame(left_frame)
            logo_frame.configure(width = button_width)
            logo_frame.pack(side = Tkinter.TOP)
            slogan_label = Tkinter.Label(left_frame, text =
                      "yet another\nclosure-based association " +
                      "rules\nexperimentation environment\n(version " +
                      cls.version + ")")
            slogan_label.configure(width = button_width)
            slogan_label.pack(side=Tkinter.TOP)
            logo_label = Tkinter.Label(logo_frame,image=logo)
            namefont = tkFont.Font(family = "Helvetica",
                                   size = 18,
                                   slant = "italic",
                                   weight = "bold")
            name = Tkinter.Label(logo_frame,text="yacaree",
                                 font = namefont,
                                 anchor = Tkinter.SW)
            logo_label.pack(side=Tkinter.LEFT)
            name.pack(side=Tkinter.LEFT)
            process_frame = Tkinter.LabelFrame(left_frame,
                                               text="Process")
            process_frame.pack(side=Tkinter.BOTTOM)

            console_frame = Tkinter.LabelFrame(cls.root, text="Console")
            console_frame.pack(side=Tkinter.LEFT)
            cls.console = Tkinter.Text(console_frame)
            cls.console.configure(width = text_width, 
                                  height = text_height)
            cls.console.pack(side=Tkinter.LEFT)
            cls.scrollY = Tkinter.Scrollbar(console_frame,
                                        orient = Tkinter.VERTICAL,
                                        command = cls.console.yview)
            cls.scrollY.pack(side=Tkinter.LEFT, fill = Tkinter.Y)
            cls.console.configure(yscrollcommand = cls.scrollY.set)

            cls.filepick = Tkinter.Button(process_frame)
            cls.filepick.configure(text = "Choose a dataset file",
                                   width = button_width,
                                   height = button_height,
                                   command = cls.choose_datafile)
            cls.filepick.pack()

            cls.run = Tkinter.Button(process_frame)
            cls.run.configure(text = "Run yacaree for " + 
                              "all rules\n(and be patient), or...",
                              width = button_width,
                              height = button_height,
                              state = Tkinter.DISABLED,
                              command = yacaree.standard_run_all)
            cls.run.pack()

            cls.run50 = Tkinter.Button(process_frame)
            cls.run50.configure(text = "...Run yacaree for " + 
                         "at most 50 rules\n(but be equally patient)",
                         width = button_width,
                         height = button_height,
                         state = Tkinter.DISABLED,
                         command = yacaree.standard_run)
            cls.run50.pack()

            cls.finish_button = Tkinter.Button(process_frame)
            cls.finish_button.configure(text = "Stop ASAP (be patient) / Close",
                                      width = button_width,
                                      height = button_height,
                                      command = cls.finish)
            cls.finish_button.pack()

            cls.report("This is yacaree, version " + cls.version + ".")
            if yacaree.datafilename:
                cls.report("Called on dataset in file " + 
                           yacaree.datafilename)
                cls.run.configure(state = Tkinter.NORMAL)
                if cls.hpar.maxrules:
                    cls.run50.configure(state = Tkinter.NORMAL)
                cls.opendatafile(yacaree.datafilename)
            cls.clock_at_report = clock()
            cls.root.mainloop()

        else:
            "CLI interface"
            cls.report("This is yacaree, version " + cls.version + ".")
            cls.opendatafile(yacaree.datafilename)
            yacaree.standard_run() 
            # no need to call run_all as maxrules already at 0


    @classmethod
    def choose_datafile(cls):
        "only on GUI - consider merging with above"
        if cls._gui:
            fnm = tkFileDialog.askopenfilename(
                defaultextension = cls.fn._filenamext, 
                filetypes = [("text files","*.txt"), 
                             ("all files","*.*")],
                title = "Choose a dataset file")
            if fnm:
                "dialog possibly canceled, but maybe actual file chosen"
                cls.datafile = None  
                cls.opendatafile(fnm)
                cls.report("Selected dataset in file " + 
                           cls.fn._filenamefull + ".")
                cls.run.configure(state = Tkinter.NORMAL)
                if cls.hpar.maxrules:
                    cls.run50.configure(state = Tkinter.NORMAL)


    @classmethod
    def opendatafile(cls, datafilename):
        """
        Decoupled now from openauxfiles in case of repeated analysis
        on the same data; from here, filehandler's filename can be 
        handled as a property.
        """
        if datafilename:
            cls.fn.filename = datafilename
            cls.datafile = cls.fn.openfile(cls.fn._filenamefull)
        else:
            cls.datafile = None
        while not cls.datafile:
            "find the dataset file"
            filename = input("Dataset File Name again? [RET to exit] ")
            if not filename:
                exit()
            cls.fn.filename = filename
            cls.datafile = cls.fn.openfile(cls.fn._filenamefull)


    @classmethod
    def openauxfiles(cls):
        if cls._gui:
            cls.run.configure(state = Tkinter.NORMAL)
            if cls.hpar.maxrules:
                cls.run50.configure(state = Tkinter.NORMAL)
        cls.logfile = cls.fn.openfile(cls.fn._filenamenow + ".log", "w")
        cls.rulesfile = cls.fn.openfile(cls.fn._filenamenow + 
            "_rules.log", "w") # + "_rules.txt" to get back to
        if not cls.logfile or not cls.rulesfile:
            cls.reporterror("Could not open or write on output" +
                            " and/or log files.")


    @classmethod
    def finish(cls):
        "only on GUI, to bind a button to"
        if cls._gui:
            if cls._running:
                "please stop mining ASAP"
                cls.finish_button.configure(state = Tkinter.DISABLED)
                cls.report("User-requested stop of mining process.")
                cls._running = False
            else:
                "not running, hence exit"
                cls.sound_bell()
                cls.root.destroy()
                exit(0)


    @classmethod
    def get_ready_for_new_run(cls):
        "Only on GUI. After one of run/run50, may wish to run the other"
        if cls._gui:
            cls._running = False
            cls.run.configure(state = Tkinter.NORMAL)
            cls.run50.configure(state = Tkinter.NORMAL)
            cls.filepick.configure(state = Tkinter.NORMAL)
            cls.finish_button.configure(state = Tkinter.NORMAL)
            # ~ refresh datetime in names, 
            # ~ just in case we use the same dataset
            # ~ (done by the property setter in the FileNames class)
            cls.fn.filename = cls.fn.filename 


    @classmethod
    def get_ready_for_run(cls):
        "Only on GUI."
        if cls._gui:
            cls.filepick.configure(state = Tkinter.DISABLED)
            cls.run.configure(state = Tkinter.DISABLED)
            cls.run50.configure(state = Tkinter.DISABLED)


    @classmethod
    def report(cls, m = ""): # , warnlevel = ''):
        cls.clock_at_report = clock()
        m = " " + m + "\n"
        if cls._gui:
            cls.console.insert(Tkinter.END,"[yacaree]" + m)
            cls.console.see("end-2c")
            cls.console.update()
        else:
            print("[yacaree]" + m, end = '', flush = True)
        if cls.logfile and not cls.logfile.closed:
            "Remains to report the opening of the log!" 
            cls.logfile.write(str(datetime.now()) + m)


    @classmethod
    def reportwarning(cls, m = ""):
        "get warning to be an argument of report instead"
        cls.clock_at_report = clock()
        m = " " + m + "\n"
        cls.sound_bell()
        if cls._gui:
            cls.console.insert(Tkinter.END,"[yacaree warning]" + m)
            cls.console.see("end-2c")
            cls.console.update()
        else:
            print("[yacaree warning]" + m, end = '', flush = True)
        if cls.logfile: 
            cls.logfile.write(str(datetime.now()) + m)
        sleep(1)


    @classmethod
    def reporterror(cls, m = ""):
        "get error to be an argument of report instead"
        cls.clock_at_report = clock()
        cls.sound_bell()
        if cls._gui:
            cls.finish_button.configure(state = Tkinter.DISABLED)
            m += "\n"
            cls.console.insert(Tkinter.END,"[yacaree error] " + m)
            cls.console.configure(background = "misty rose")
            cls.console.update()
            sleep(8)
            cls.root.destroy()
        else:
            m = "Error: " + m + " Exiting.\n"
            sleep(2)
        if cls.logfile: 
            cls.logfile.write(str(datetime.now()) + " " + m)
        exit("[yacaree error] " + m)


    @classmethod
    def sound_bell(cls):
        pass
        # ~ if cls._gui:
            # ~ cls.console.bell()
        # ~ else:
            # ~ print('\a', end = '', flush = True)
