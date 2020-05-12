"""
THIS FILE IS SLATED FOR DELETION SOON. PLEASE IGNORE IT.

Project: yacaree
Programmer: JLB

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
from time import clock # only for gui right now
from six.moves import input as raw_input
import statics

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

class iface_text:

    def __init__(self):
        "GUI requires initialization deferred to go, CLI does the same"
        pass

    def go(self, yacaree):
        self.report("This is yacaree, version " + statics.version + ".")
        if statics.filenamefull is None:
            self.reportwarning("No dataset file specified.")
            filename = self.ask_input("Dataset File Name? ")
            self.storefilename(filename)
        if statics.maxrules == 0:
            self.report("Running for all rules.")
        yacaree.standard_run() # no need to call run_all as maxrules already at 0

    @staticmethod
    def storefilename(filename):
        if len(filename)<=3 or filename[-4] != '.':
            statics.filename = filename
            statics.filenamefull = filename + statics.filenamext
        else:
            statics.filename, _ = filename.rsplit('.',1)
            statics.filenamefull = filename

    @staticmethod
    def report(m = ""):
        print("[yacaree] " + m)
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @staticmethod
    def report_log_file(filename):
        "not reported like the rest for lack of log file"
        if statics.logfile: 
            "print already done, here just log entry"
            m = "Log file " + filename + ".log (this file) set up."
            statics.logfile.write(str(datetime.now()) + " " + m + "\n")
            stdout.flush()

    # ~ def endreport(self):
        # ~ "flush - may become again necessary for line breaks"
        # ~ pass
    
    @staticmethod
    def reportwarning(m=""):
        print("[yacaree warning] " + m)
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @staticmethod
    def reporterror(m = ""):
        m = m + " Exiting.\n"
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m)
        exit("[yacaree error] " + m)
    
    @staticmethod
    def ask_input(prompt):
        "See import from six.moves above"
        if statics.logfile: statics.logfile.write("Asked:" + prompt + "\n")
        ans = raw_input(prompt)
        if statics.logfile: statics.logfile.write("Answer:" + ans + "\n")
        return ans

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
                f = open(filename,"w")
                self.report("File is now open.")
                return f
            except (IOError, OSError):
                self.reporterror("Unable to open file.")
        else:
            self.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")

    def sound_bell(a):
        print('\a')

    def get_ready_for_run(self):
        "stand-in for GUI, no such thing in the text CLI case"
        pass

    def get_ready_for_new_run(self):
        "stand-in for GUI, no such thing in the text CLI case"
        pass




class iface_gui:
    "Initially a case of something like a singleton pattern, not anymore"

    def __init__(self):
        """Instantiation is made before having a yacaree to  
        bind the buttons to, hence everything deferred to self.go()
        """
        pass

    def go(self, yacaree):
        "Bindings could not be made in a regular __init__()"
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
                                     statics.version + ")")
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
        self.report("This is yacaree, version " + statics.version + ".") 

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
        self.finish_button.configure(text = "Finish",
                                  width = button_width,
                                  height = button_height,
                                  command = self.finish)
        self.finish_button.pack()
        if statics.maxrules == 0:
            self.report("Requested all rules as output.")
        if statics.filenamefull:
            self.report("Selected dataset in file " + statics.filenamefull)
            self.run.configure(state = Tkinter.NORMAL)
            if statics.maxrules:
                self.run50.configure(state = Tkinter.NORMAL)
        self.clock_at_report = clock()
        self.root.mainloop()

    def choose_datafile(self):
        fnm = tkFileDialog.askopenfilename(
            defaultextension=".txt",
            filetypes = [("text files","*.txt"), ("all files","*.*")],
            title = "Choose a dataset file")
        if fnm:
            "dialog could have been canceled, but actual file chosen"
            self.storefilename(fnm)
            self.report("Selected dataset in file " + statics.filenamefull + ".")
            self.run.configure(state = Tkinter.NORMAL)
            if statics.maxrules:
                self.run50.configure(state = Tkinter.NORMAL)

    def finish(self):
        if statics.logfile: statics.logfile = None # not sure still necessary
        self.sound_bell()
        self.root.destroy()
        exit(0)

    def get_ready_for_new_run(self):
        "After one of run/run50, user may wish to run the other"
        self.run.configure(state = Tkinter.NORMAL)
        self.run50.configure(state = Tkinter.NORMAL)
        self.filepick.configure(state = Tkinter.NORMAL)
        self.finish_button.configure(state = Tkinter.NORMAL)

    # ~ def disable_again(self):
        # ~ pass

    # ~ def enable_finish(self):
        # ~ self.finish_button.configure(state = Tkinter.NORMAL)

    # ~ def disable_finish(self):
        # ~ self.finish_button.configure(state = Tkinter.DISABLED)

    # ~ def disable_filepick(self):
        # ~ self.filepick.configure(state = Tkinter.DISABLED)

    # ~ def disable_run(self):
        # ~ self.run.configure(state = Tkinter.DISABLED)
        # ~ self.run50.configure(state = Tkinter.DISABLED)

    def get_ready_for_run(self):
        self.filepick.configure(state = Tkinter.DISABLED)
        self.run.configure(state = Tkinter.DISABLED)
        self.run50.configure(state = Tkinter.DISABLED)

    def report(self, m):
        self.clock_at_report = clock()
        m = " " + m + "\n"
        self.console.insert(Tkinter.END,"[yacaree]" + m)
        self.console.see("end-2c")
        self.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m)

    def possibly_report(self, m):
        "report only if too long time elapsed since last reporting"
        clock_now = clock()
        if clock_now - self.clock_at_report > statics.report_period:
            self.report(m)

    # ~ def endreport(self):
        # ~ pass

    def reportwarning(self, m):
        self.clock_at_report = clock()
        m = " " + m + "\n"
        self.console.insert(Tkinter.END,"[yacaree warning]" + m)
        self.console.see("end-2c")
        self.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m)

    def reporterror(self, m):
        self.clock_at_report = clock()
        m += "\n"
        self.console.insert(Tkinter.END,"[yacaree error] " + m)
        m = "Error: " + m
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m)
        sleep(10)
        self.sound_bell()
        self.root.destroy()
        exit(m)

    def report_log_file(self, filename):
        self.clock_at_report = clock()
        m_log = " Log file " + filename + ".log (this file) set up.\n"
        m_cls = " Log file " + filename + ".log set up.\n"
        self.console.insert(Tkinter.END,"[yacaree]" + m_cls)
        self.console.see("end-2c")
        self.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m_log)

    @staticmethod
    def storefilename(filename):
        if len(filename)<=3 or filename[-4] != '.':
            statics.filename = filename
            statics.filenamefull = filename + statics.filenamext
        else:
            statics.filename, _ = filename.rsplit('.',1)
            statics.filenamefull = filename

    def openfile(self, filename,mode = "r"):
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
                f = open(filename,"w")
                self.report("File is now open.")
                return f
            except (IOError, OSError):
                self.reporterror("Unable to open file.")
        else:
            self.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")

    def sound_bell(self):
        self.console.bell()

