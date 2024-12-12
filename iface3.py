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

REVISE URGENTLY

report*: outputs a string message, prepends a line break,
 variants for warnings and errors
ask_input: user communication
openfile, storefilename: to set up the data source
go: calls run method of miner
others: to handle the communication with Tk

"""




from datetime import datetime
from time import sleep, time as clock
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

    # ~ def __init__(self, gui = False):
        # ~ """
        # ~ Instantiation is made before having a yacaree to  
        # ~ bind the buttons to, hence everything deferred to self.go()
        # ~ NOT SURE OF THE RIGHT PLACE TO IMPORT tkinter
        # ~ """
        # ~ self.gui = gui
        # ~ self.report_period = 30 # seconds between possibly_report calls
        # ~ self.filenamext = ".td"
        # ~ self.logfile = None
        # ~ self.filenamefull = None
        # ~ if gui: # tried to import Tkinter here but did not work

    report_period = 30 # seconds between possibly_report calls
    filenamext = ".td"
    logfile = None
    filenamefull = None
    filenamenow = None

    print("NO LOG FILE") ####

    _gui = False

    @property
    def gui(self):
        return type(self)._gui

    @gui.setter
    def gui(self, val):
        type(self)._gui = bool(val)


    @classmethod
    def go(cls, yacaree):
        """Bindings could not be made in a regular __init__()
        try to have only hpar as argument
        """
        cls.hpar = yacaree.hpar

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
                                         cls.hpar.version + ")")
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
            cls.report("This is yacaree, version " + cls.hpar.version + ".") 
    
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
                              command = yacaree.standard_run_all)
            cls.run.pack()
    
            cls.run50 = Tkinter.Button(process_frame)
            cls.run50.configure(text = "...Run yacaree for at most 50 rules\n(but be equally patient)",
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
            if statics.maxrules == 0:
                cls.report("CLI call requested all rules as output.")
            if cls.filenamefull:
                cls.report("Selected dataset in file " + cls.filenamefull)
                cls.run.configure(state = Tkinter.NORMAL)
                if statics.maxrules:
                    cls.run50.configure(state = Tkinter.NORMAL)
            cls.clock_at_report = clock()
            cls.root.mainloop()

        else:
            "CLI interface"
            cls.report("This is yacaree, version " + yacaree.hpar.version + ".")
            if cls.filenamefull is None:
                cls.reportwarning("No dataset file specified.")
                filename = cls.ask_input("Dataset File Name? ")
                cls.storefilename(filename)
            yacaree.standard_run() # no need to call run_all as maxrules already at 0


    @classmethod
    def ask_input(cls, prompt):
        "Refactor, check only use is for dataset file, add a loop until correct"
        if cls.logfile: cls.logfile.write("Asked:" + prompt + "\n")
        ans = input(prompt)
        if cls.logfile: cls.logfile.write("Answer:" + ans + "\n")
        return ans


    @classmethod
    def storefilename(cls, filename):
        if len(filename)<=3 or filename[-4] != '.':
            cls.filename = filename
            cls.filenamefull = filename + cls.filenamext
        else:
            cls.filename, _ = filename.rsplit('.',1)
            cls.filenamefull = filename


    @classmethod
    def choose_datafile(cls):
        "only on GUI - consider merging with above"
        if cls._gui:
            fnm = tkFileDialog.askopenfilename(
                defaultextension=".txt",
                filetypes = [("text files","*.txt"), ("all files","*.*")],
                title = "Choose a dataset file")
            if fnm:
                "dialog could have been canceled, but actual file chosen"
                cls.storefilename(fnm)
                cls.report("Selected dataset in file " + cls.filenamefull + ".")
                cls.run.configure(state = Tkinter.NORMAL)
                if statics.maxrules:
                    cls.run50.configure(state = Tkinter.NORMAL)


    @classmethod
    def finish(cls):
        "only on GUI"
        if statics.running:
            "please stop mining ASAP"
            cls.finish_button.configure(state = Tkinter.DISABLED)
            cls.report("User-requested stop of mining process.")
            statics.running = False
        else:
            "not running, hence exit"
            if cls.logfile: cls.logfile = None # not sure still necessary
            cls.sound_bell()
            cls.root.destroy()
            exit(0)


    @classmethod
    def get_ready_for_new_run(cls):
        "Only on GUI. After one of run/run50, user may wish to run the other"
        if cls._gui:
            cls.run.configure(state = Tkinter.NORMAL)
            cls.run50.configure(state = Tkinter.NORMAL)
            cls.filepick.configure(state = Tkinter.NORMAL)
            cls.finish_button.configure(state = Tkinter.NORMAL)


    @classmethod
    def get_ready_for_run(cls):
        "Only on GUI."
        if cls._gui:
            cls.filepick.configure(state = Tkinter.DISABLED)
            cls.run.configure(state = Tkinter.DISABLED)
            cls.run50.configure(state = Tkinter.DISABLED)


    @classmethod
    def report(cls, m = "", warnlevel = ''): #, noskip = True):
        "SIMPLIFY"
        cls.clock_at_report = clock()
        # ~ if noskip or \
            # ~ clock_now - cls.clock_at_report > cls.report_period:
        m = " " + m + "\n"
        if cls._gui:
            cls.console.insert(Tkinter.END,"[yacaree]" + m)
            cls.console.see("end-2c")
            cls.console.update()
        else:
            print("[yacaree]" + m, end = '', flush = True)
            # ~ stdout.flush()
        if cls.logfile: 
            cls.logfile.write(str(datetime.now()) + m)

    # ~ @classmethod
    # ~ def possibly_report(cls, m):
        # ~ """
        # ~ report only if too long time elapsed since last reporting
        # ~ Some day: replace by direct calls using noskip and remove
        # ~ (BUT DO I HAVE IT ANYWHERE?)
        # ~ """
        # ~ # clock_now = clock()
        # ~ # if clock_now - cls.clock_at_report > cls.report_period:
            # ~ # cls.report(m)
        # ~ cls.report(m, warnlevel = '', noskip = True)


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
        sleep(1)
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
    def report_log_file(cls, filename):
        """
        Refactor so that the names are constructed only in one place -
        not reported like the rest for lack of log file
        """
        cls.clock_at_report = clock()
        m_log = " Log file " + filename + ".log (this file) set up.\n"
        m_cls = " Log file " + filename + ".log set up.\n"
        if cls._gui:
            cls.console.insert(Tkinter.END,"[yacaree]" + m_cls)
            cls.console.see("end-2c")
            cls.console.update()
        if cls.logfile: 
            "print already done, here just log entry (????)"
            cls.logfile.write(str(datetime.now()) + m_log)


    @classmethod
    def openfile(cls, filename, mode = "r"):
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
                f = open(filename, "w")
                cls.report("File is now open.")
                return f
            except (IOError, OSError):
                cls.reporterror("Unable to open file.")
        else:
            cls.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")


    @classmethod
    def sound_bell(cls):
        if cls._gui:
            cls.console.bell()
        else:
            print('\a', end = '', flush = True)

