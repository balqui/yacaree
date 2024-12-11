"""
Project: yacaree
Programmer: JLB

CAVEAT: "Close" button does not always work, I believe already in the frozen version.

Refactoring underway.

Description:

iface_text:
Textual command-line interface, 
originally previous to the GUI and later concurrent with it

iface_gui:
Slight evolution of the first, simple Tkinter-based GUI for yacaree

Usage:
report*: outputs a string message, prepends a line break,
 variants for warnings and errors
ask_input: user communication
openfile, storefilename: to set up the data source
go: calls run method of miner
others: to handle the communication with Tk
"""




from sys import stdout
from datetime import datetime
from time import time as clock # only for gui right now
# ~ from time import clock # only for gui right now
# ~ from six.moves import input as raw_input
import statics # for version, maxrules, running

try:
    "Python 2 version - all these imports only for gui"
    import Tkinter
    import tkFileDialog
    import tkFont
except ModuleNotFoundError:
    "Python 3 (or beyond?) version"
    import tkinter as Tkinter
    from tkinter import filedialog as tkFileDialog
    from tkinter import font as tkFont

# ~ class iface_gui:
class IFace:

    def __init__(self, gui = False):
        """
        Instantiation is made before having a yacaree to  
        bind the buttons to, hence everything deferred to self.go()
        NOT SURE OF THE RIGHT PLACE TO IMPORT tkinter
        """
        self.gui = gui
        self.report_period = 30 # seconds between possibly_report calls
        self.filenamext = ".td"
        self.logfile = None
        self.filenamefull = None
        # ~ if gui: # tried to import Tkinter here but did not work

    def go(self, yacaree):
        """Bindings could not be made in a regular __init__()
        try to have only hpar as argument
        """
        self.hpar = yacaree.hpar

        if self.gui:

            self.root = Tkinter.Tk()
    
            button_width = 35
            button_height = 4
            text_width = 92
            text_height = 28
    
            left_frame = Tkinter.Frame(self.root)
            left_frame.pack(side=Tkinter.LEFT)
            logo = Tkinter.BitmapImage(file="yac-v03.xbm")
            logo_frame = Tkinter.Frame(left_frame)
            logo_frame.configure(width = button_width)
            logo_frame.pack(side = Tkinter.TOP)
            slogan_label = Tkinter.Label(left_frame, text =
                                         "yet another\nclosure-based association " +
                                         "rules\nexperimentation environment\n(version " +
                                         self.hpar.version + ")")
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
            process_frame = Tkinter.LabelFrame(left_frame,text="Process")
            process_frame.pack(side=Tkinter.BOTTOM)
    
            console_frame = Tkinter.LabelFrame(self.root,text="Console")
            console_frame.pack(side=Tkinter.LEFT)
            self.console = Tkinter.Text(console_frame)
            self.console.configure(width = text_width, height = text_height)
            self.console.pack(side=Tkinter.LEFT)
            self.scrollY = Tkinter.Scrollbar(console_frame,
                                        orient = Tkinter.VERTICAL,
                                        command = self.console.yview)
            self.scrollY.pack(side=Tkinter.LEFT, fill = Tkinter.Y)
            self.console.configure(yscrollcommand = self.scrollY.set)
            self.report("This is yacaree, version " + self.hpar.version + ".") 
    
            self.filepick = Tkinter.Button(process_frame)
            self.filepick.configure(text = "Choose a dataset file",
                                   width = button_width,
                                   height = button_height,
                                   command = self.choose_datafile)
            self.filepick.pack()
    
            self.run = Tkinter.Button(process_frame)
            self.run.configure(text = "Run yacaree for all rules\n(and be patient), or...",
                              width = button_width,
                              height = button_height,
                              state = Tkinter.DISABLED,
                              command = yacaree.standard_run_all)
            self.run.pack()
    
            self.run50 = Tkinter.Button(process_frame)
            self.run50.configure(text = "...Run yacaree for at most 50 rules\n(but be equally patient)",
                              width = button_width,
                              height = button_height,
                              state = Tkinter.DISABLED,
                              command = yacaree.standard_run)
            self.run50.pack()
    
            self.finish_button = Tkinter.Button(process_frame)
            self.finish_button.configure(text = "Stop ASAP (be patient) / Close",
                                      width = button_width,
                                      height = button_height,
                                      command = self.finish)
            self.finish_button.pack()
            if statics.maxrules == 0:
                self.report("CLI call requested all rules as output.")
            if self.filenamefull:
                self.report("Selected dataset in file " + self.filenamefull)
                self.run.configure(state = Tkinter.NORMAL)
                if statics.maxrules:
                    self.run50.configure(state = Tkinter.NORMAL)
            self.clock_at_report = clock()
            self.root.mainloop()

        else:
            "CLI interface"
            self.report("This is yacaree, version " + yacaree.hpar.version + ".")
            if self.filenamefull is None:
                self.reportwarning("No dataset file specified.")
                filename = self.ask_input("Dataset File Name? ")
                self.storefilename(filename)
            yacaree.standard_run() # no need to call run_all as maxrules already at 0


    def ask_input(self, prompt):
        "Refactor, check only use is for dataset file, add a loop until correct"
        if self.logfile: self.logfile.write("Asked:" + prompt + "\n")
        ans = input(prompt)
        if self.logfile: self.logfile.write("Answer:" + ans + "\n")
        return ans


    def storefilename(self, filename):
        if len(filename)<=3 or filename[-4] != '.':
            self.filename = filename
            self.filenamefull = filename + self.filenamext
        else:
            self.filename, _ = filename.rsplit('.',1)
            self.filenamefull = filename
        print(self.filename, self.filenamefull) ####


    def choose_datafile(self):
        "only on GUI - consider merging with above"
        if self.gui:
            fnm = tkFileDialog.askopenfilename(
                defaultextension=".txt",
                filetypes = [("text files","*.txt"), ("all files","*.*")],
                title = "Choose a dataset file")
            if fnm:
                "dialog could have been canceled, but actual file chosen"
                self.storefilename(fnm)
                self.report("Selected dataset in file " + self.filenamefull + ".")
                self.run.configure(state = Tkinter.NORMAL)
                if statics.maxrules:
                    self.run50.configure(state = Tkinter.NORMAL)

    def finish(self):
        "only on GUI"
        if statics.running:
            "please stop mining ASAP"
            self.finish_button.configure(state = Tkinter.DISABLED)
            self.report("User-requested stop of mining process.")
            statics.running = False
        else:
            "not running, hence exit"
            if self.logfile: self.logfile = None # not sure still necessary
            self.sound_bell()
            self.root.destroy()
            exit(0)

    def get_ready_for_new_run(self):
        "Only on GUI. After one of run/run50, user may wish to run the other"
        if self.gui:
            self.run.configure(state = Tkinter.NORMAL)
            self.run50.configure(state = Tkinter.NORMAL)
            self.filepick.configure(state = Tkinter.NORMAL)
            self.finish_button.configure(state = Tkinter.NORMAL)

    def get_ready_for_run(self):
        "Only on GUI."
        if self.gui:
            self.filepick.configure(state = Tkinter.DISABLED)
            self.run.configure(state = Tkinter.DISABLED)
            self.run50.configure(state = Tkinter.DISABLED)

    def report(self, m = ""):
        self.clock_at_report = clock()
        m = " " + m + "\n"
        if self.gui:
            self.console.insert(Tkinter.END,"[yacaree]" + m)
            self.console.see("end-2c")
            self.console.update()
        else:
            print("[yacaree]" + m, end = '')
            stdout.flush()
        if self.logfile: 
            self.logfile.write(str(datetime.now()) + m)

    def possibly_report(self, m):
        "report only if too long time elapsed since last reporting"
        clock_now = clock()
        if clock_now - self.clock_at_report > self.report_period:
            self.report(m)

    def reportwarning(self, m = ""):
        "get warning to be an argument of report instead"
        self.clock_at_report = clock()
        m = " " + m + "\n"
        if self.gui:
            self.console.insert(Tkinter.END,"[yacaree warning]" + m)
            self.console.see("end-2c")
            self.console.update()
        else:
            print("[yacaree warning]" + m, end = '')
            stdout.flush()
        if self.logfile: 
            self.logfile.write(str(datetime.now()) + m)


    def reporterror(self, m = ""):
        "get error to be an argument of report instead"
        self.clock_at_report = clock()
        m += "\n"
        if self.gui:
            self.console.insert(Tkinter.END,"[yacaree error] " + m)
            self.sound_bell()
            sleep(10)
            self.root.destroy()
        else:
            m = "Error: " + m + " Exiting.\n"
        if self.logfile: 
            self.logfile.write(str(datetime.now()) + " " + m)
        exit("[yacaree error] " + m)


    def report_log_file(self, filename):
        """
        Refactor so that the names are constructed only in one place -
        not reported like the rest for lack of log file
        """
        self.clock_at_report = clock()
        m_log = " Log file " + filename + ".log (this file) set up.\n"
        m_cls = " Log file " + filename + ".log set up.\n"
        if self.gui:
            self.console.insert(Tkinter.END,"[yacaree]" + m_cls)
            self.console.see("end-2c")
            self.console.update()
        if self.logfile: 
            "print already done, here just log entry (????)"
            self.logfile.write(str(datetime.now()) + m_log)
            # ~ stdout.flush()


    def openfile(self, filename, mode = "r"):
        "checks for readability"
        if mode == "r":
            self.report("Opening file " +
                       filename + " for reading.")
            try:
                f = open(filename)
                f.readline()
                f.close
                self.report("File is now open.")
                return open(filename)
            except (IOError, OSError):
                self.reporterror("Nonexistent or unreadable file.")
        elif mode == "w":
            self.report("Opening file " +
                       filename + " for writing.")
            try:
                f = open(filename, "w")
                self.report("File is now open.")
                return f
            except (IOError, OSError):
                self.reporterror("Unable to open file.")
        else:
            self.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")


    def sound_bell(self):
        if self.gui:
            self.console.bell()
        else:
            print('\a')

