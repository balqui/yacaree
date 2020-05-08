"""

Project: yacaree
Programmer: JLB

Description:

iface_text:
Textual command-line interface, 
originally previous to the GUI and now concurrent with it

iface_gui:
A simple Tkinter-based GUI for yacaree


Usage (oldish, to review):
say: outputs a string message, no line breaks
report: likewise, prepends a line break,
 variants for warnings and errors
ask_input:
 user communication
go:
 calls run method of miner, matching approximately 
 the similar button and callback of the GUI

ToDo: optionally several messages in the same line?
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
        pass

    @classmethod
    def go(cls, yacaree):
        cls.report("This is yacaree, version " + statics.version + ".")
        if statics.filenamefull is None:
            cls.reportwarning("No dataset file specified.")
            filename = cls.ask_input("Dataset File Name? ")
            cls.storefilename(filename)
        if statics.maxrules == 0:
            cls.report("Running for all rules.")
        yacaree.standard_run() # no need to call run_all as maxrules already at 0

    @classmethod
    def storefilename(cls, filename):
        if len(filename)<=3 or filename[-4] != '.':
            statics.filename = filename
            statics.filenamefull = filename + statics.filenamext
        else:
            '''statics.filenamext should not be modified:
            o/w if a new dataset is loaded, the default extension no longer applies
            '''
            # ~ statics.filename, statics.filenamext = filename.rsplit('.',1)
            statics.filename, _ = filename.rsplit('.',1)
            statics.filenamefull = filename
        # ~ cls.report("Selected dataset in file " + statics.filenamefull)

    @classmethod
    def report(cls,m=""):
        print("[yacaree] " + m)
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @classmethod
    def report_log_file(cls, filename):
        "not reported like the rest for lack of log file"
        if statics.logfile: 
            "print already done, here just log entry"
            m = "Log file " + filename + ".log (this file) set up."
            statics.logfile.write(str(datetime.now()) + " " + m + "\n")
            stdout.flush()

    @classmethod
    def endreport(cls):
        "flush - may become again necessary for line breaks"
        pass
    
    @classmethod
    def reportwarning(cls,m=""):
        print("[yacaree warning] " + m)
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m + "\n")
        stdout.flush()

    @classmethod
    def reporterror(cls,m=""):
        # ~ print("[yacaree error] " + m)
        m = m + " Exiting.\n"
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m)
        exit("[yacaree error] " + m)

    @classmethod
    def ask_input(cls,prompt):
        "See import from six.moves above"
        if statics.logfile: statics.logfile.write("Asked:" + prompt + "\n")
        ans = raw_input(prompt)
        if statics.logfile: statics.logfile.write("Answer:" + ans + "\n")
        return ans

    @classmethod
    def openfile(cls,filename,mode="r"):
        "checks for readability"
        if mode == "r":
            cls.report("Opening file " +
                       filename + " for reading.")
            try:
                f = open(filename)
                f.readline()
                f.close
                cls.report("File is now open.")
                return open(filename)
            except (IOError, OSError):
                cls.reporterror("Nonexistent or unreadable file.")
        elif mode == "w":
            cls.report("Opening file " +
                       filename + " for writing.")
            try:
                f = open(filename,"w")
                cls.report("File is now open.")
                return f
            except (IOError, OSError):
                cls.reporterror("Unable to open file.")
        else:
            cls.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")

    @classmethod
    def sound_bell(a):
        print('\a')

## Temporary stand-ins for GUI-related calls

    @classmethod
    def disable_filepick(a):
        pass

    @classmethod
    def disable_finish(a):
        pass

    @classmethod
    def disable_run(a):
        pass

    @classmethod
    def enable_again(a):
        pass

    @classmethod
    def enable_finish(a):
        pass




class iface_gui:

    def __init__(self):
        pass

    @classmethod
    def go(cls,mainprog):
        "Parts of this must go into a regular __init__()"
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

        console_frame = Tkinter.LabelFrame(cls.root,text="Console")
        console_frame.pack(side=Tkinter.LEFT)
        cls.console = Tkinter.Text(console_frame)
        cls.console.configure(width = text_width, height = text_height)
        cls.console.pack(side=Tkinter.LEFT)
        cls.scrollY = Tkinter.Scrollbar(console_frame,
                                    orient = Tkinter.VERTICAL,
                                    command = cls.console.yview)
        cls.scrollY.pack(side=Tkinter.LEFT, fill = Tkinter.Y)
        cls.console.configure(yscrollcommand = cls.scrollY.set)
        cls.report("This is yacaree, version " + statics.version + ".") 

        cls.filepick = Tkinter.Button(process_frame)
        cls.filepick.configure(text = "Choose a dataset file",
                               width = button_width,
                               height = button_height,
                               command = cls.choose_datafile)
        cls.filepick.pack()

        cls.run = Tkinter.Button(process_frame)
        cls.run.configure(text = "Run yacaree for all rules\n(and be patient), or...",
                          width = button_width,
                          height = button_height,
                          state = Tkinter.DISABLED,
                          command = mainprog.standard_run_all)
        cls.run.pack()

        cls.run50 = Tkinter.Button(process_frame)
        cls.run50.configure(text = "...Run yacaree for at most 50 rules\n(but be equally patient)",
                          width = button_width,
                          height = button_height,
                          state = Tkinter.DISABLED,
                          command = mainprog.standard_run)
        cls.run50.pack()

        cls.finish_button = Tkinter.Button(process_frame)
        cls.finish_button.configure(text = "Finish",
                                  width = button_width,
                                  height = button_height,
                                  command = cls.finish)
        cls.finish_button.pack()
        if statics.filenamefull:
            cls.report("Selected dataset in file " + statics.filenamefull)
            cls.run.configure(state = Tkinter.NORMAL)
            if statics.maxrules == 0:
                cls.report("Requested all rules as output.")
            else:
                cls.run50.configure(state = Tkinter.NORMAL)
        cls.clock_at_report = clock()
        cls.root.mainloop()

    @classmethod
    def choose_datafile(cls):
        fnm = tkFileDialog.askopenfilename(
            defaultextension=".txt",
            filetypes = [("text files","*.txt"), ("all files","*.*")],
            title = "Choose a dataset file")
        cls.storefilename(fnm)
        cls.run.configure(state = Tkinter.NORMAL)
        cls.run50.configure(state = Tkinter.NORMAL)
        cls.report("Selected dataset in file " + statics.filenamefull + ".")

    @classmethod
    def finish(cls):
        if statics.logfile: statics.logfile = None # not sure still necessary
        cls.console.bell()
        cls.root.destroy()
        exit(0)

    @classmethod
    def enable_again(cls):
        "After one of run/run50, user may wish to run the other"
        # ~ cls.run.configure(state = Tkinter.DISABLED)
        # ~ cls.run50.configure(state = Tkinter.DISABLED)
        cls.run.configure(state = Tkinter.NORMAL)
        cls.run50.configure(state = Tkinter.NORMAL)
        cls.filepick.configure(state = Tkinter.NORMAL)

    @classmethod
    def disable_again(cls):
        pass

    @classmethod
    def enable_finish(cls):
        cls.finish_button.configure(state = Tkinter.NORMAL)

    @classmethod
    def disable_finish(cls):
        cls.finish_button.configure(state = Tkinter.DISABLED)
##        cls.finish_button.update()

    @classmethod
    def disable_filepick(cls):
        cls.filepick.configure(state = Tkinter.DISABLED)

    @classmethod
    def disable_run(cls):
        cls.run.configure(state = Tkinter.DISABLED)
        cls.run50.configure(state = Tkinter.DISABLED)

    @classmethod
    def report(cls,m):
        cls.clock_at_report = clock()
        m = " " + m + "\n"
        cls.console.insert(Tkinter.END,"[yacaree]" + m)
        cls.console.see("end-2c")
        cls.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m)

    @classmethod
    def possibly_report(cls,m):
        "report only if too long time elapsed since last reporting"
        clock_now = clock()
        if clock_now - cls.clock_at_report > statics.report_period:
            cls.report(m)

    @classmethod
    def endreport(cls):
        pass

    @classmethod
    def reportwarning(cls,m):
        cls.clock_at_report = clock()
        m = " " + m + "\n"
        cls.console.insert(Tkinter.END,"[yacaree warning]" + m)
        cls.console.see("end-2c")
        cls.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m)

    @classmethod
    def reporterror(cls,m):
        cls.clock_at_report = clock()
        m += "\n"
        cls.console.insert(Tkinter.END,"[yacaree error] " + m)
        m = "Error: " + m
        if statics.logfile: statics.logfile.write(str(datetime.now()) + " " + m)
        sleep(10)
        cls.root.destroy()
        exit(m)

    @classmethod
    def report_log_file(cls, filename):
        cls.clock_at_report = clock()
        m_log = " Log file " + filename + ".log (this file) set up.\n"
        m_cls = " Log file " + filename + ".log set up.\n"
        cls.console.insert(Tkinter.END,"[yacaree]" + m_cls)
        cls.console.see("end-2c")
        cls.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m_log)

        # ~ "not reported like the rest for lack of log file"
        # ~ if statics.logfile: 
            # ~ "print already done, here just log entry"
            # ~ statics.logfile.write(str(datetime.now()) + " " + m + "\n")
            # ~ stdout.flush()

    @classmethod
    def storefilename(cls, filename):
        if len(filename)<=3 or filename[-4] != '.':
            statics.filename = filename
            statics.filenamefull = filename + statics.filenamext
        else:
            '''statics.filenamext should not be modified:
            o/w if a new dataset is loaded, the default extension no longer applies
            '''
            # ~ statics.filename, statics.filenamext = filename.rsplit('.',1)
            statics.filename, _ = filename.rsplit('.',1)
            statics.filenamefull = filename

    @classmethod
    def openfile(cls,filename,mode="r"):
        if mode == "r":
            cls.report("Opening file " +
                       filename + " for reading.")
            try:
                f = open(filename)
                f.readline()
                f.close
                cls.report("File is now open.")
                return open(filename)
            except (IOError, OSError):
                cls.reporterror("Nonexistent or unreadable file.")
        elif mode == "w":
            cls.report("Opening file " +
                       filename + " for writing.")
            try:
                f = open(filename,"w")
                cls.report("File is now open.")
                return f
            except (IOError, OSError):
                cls.reporterror("Unable to open file.")
        else:
            cls.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")

    @classmethod
    def sound_bell(cls):
        cls.console.bell()

