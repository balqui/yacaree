"""
Project: yacaree
Programmer: JLB
"""

from datetime import datetime

class FileNames:

    def __init__(self, iface):
        """
        """
        self.iface = iface
        self._filename = None
        self._filenamefull = None
        self._filenamenow = None
        self._filenamext = ".txt" # TO MOVE ON INTO .td ONE DAY

        # ~ self.logfile = None
        # ~ self.datafile = None
        # ~ self.rulesfile = None

        self._running = False # actually out of place admittedly

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, val):
        self._running = bool(val)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, name):
        "store the file name and also set up the related ones"
        if name.endswith('.td') or name.endswith('.txt'):
            ".txt will be deprecated at some point"
            self._filenamefull = name
            self._filename, _ = name.rsplit('.',1)
        else:
            self._filename = name
            self._filenamefull = name + self._filenamext
        now = datetime.today().strftime("%Y%m%d%H%M%S")
        self._filenamenow = self._filename + now


    def openfile(self, filename, mode = "r"):
        "checks for readability"
        if mode == "r":
            self.iface.report("Opening file " +
                       filename + " for reading.")
            try:
                f = open(filename)
                assert f._checkReadable()
                self.iface.report("File is now open.")
                return f # open(filename)
            except (IOError, OSError, AssertionError):
                self.iface.reportwarning("Nonexistent or unreadable file.")
        elif mode == "w":
            self.iface.report("Opening file " +
                       filename + " for writing.")
            try:
                f = open(filename, "w")
                assert f._checkWritable()
                self.iface.report("File is now open.")
                return f
            except (IOError, OSError, AssertionError):
                self.iface.reportwarning("Unable to open or to write to file.")
        else:
            self.iface.reporterror("Requested to open file in mode '" +
                            mode + "': no such mode available.")


    # ~ def setfile(self, IFace, fnm):
        # ~ "temporary detour, has to be done this way, IFace.filename fails"
        # ~ iface = IFace()
        # ~ iface.filename = fnm


    # ~ def setfiles(self):
        # ~ "temporary detour"
        # ~ if self.iface.filename is None:
            # ~ self.iface.reportwarning("No dataset file specified.")
            # ~ self.iface.filename = input("Dataset File Name? ")
        # ~ self.iface.openfiles()

# NNNOOOOO!!!:
    # ~ def openfiles(self):
        # ~ self.datafile = self.openfile(self._filenamefull)
        # ~ while not self.datafile:
            # ~ "find the dataset file"
            # ~ filename = cls.ask_input("Dataset File Name again? [RET to exit]")
            # ~ if not filename:
                # ~ exit()
            # ~ cls.filename = filename
            # ~ self.datafile = self.openfile(self._filenamefull)
        # ~ cls.logfile = cls.openfile(cls._filenamenow + ".log", "w")
        # ~ cls.rulesfilename = cls._filenamenow + "_rules.log"
        # ~ cls.rulesfile = cls.openfile(cls.rulesfilename, "w") # + "_rules.txt" to get back to

    # ~ @classmethod
    # ~ def finish(cls):
        # ~ "only on GUI, to bind a button"
        # ~ if cls._gui:
            # ~ if statics.running:
                # ~ "please stop mining ASAP"
                # ~ cls.finish_button.configure(state = Tkinter.DISABLED)
                # ~ cls.report("User-requested stop of mining process.")
                # ~ statics.running = False
            # ~ else:
                # ~ "not running, hence exit - somehow launches again !?!"
                # ~ if cls.logfile: cls.logfile = None # not sure still necessary
                # ~ cls.sound_bell()
                # ~ cls.root.destroy()
                # ~ exit(0)


    # ~ @classmethod
    # ~ def get_ready_for_new_run(cls):
        # ~ "Only on GUI. After one of run/run50, user may wish to run the other"
        # ~ if cls._gui:
            # ~ cls.run.configure(state = Tkinter.NORMAL)
            # ~ cls.run50.configure(state = Tkinter.NORMAL)
            # ~ cls.filepick.configure(state = Tkinter.NORMAL)
            # ~ cls.finish_button.configure(state = Tkinter.NORMAL)


    # ~ @classmethod
    # ~ def get_ready_for_run(cls):
        # ~ "Only on GUI."
        # ~ if cls._gui:
            # ~ cls.filepick.configure(state = Tkinter.DISABLED)
            # ~ cls.run.configure(state = Tkinter.DISABLED)
            # ~ cls.run50.configure(state = Tkinter.DISABLED)


    # ~ @classmethod
    # ~ def report(cls, m = "", warnlevel = ''): #, noskip = True):
        # ~ "SIMPLIFY"
        # ~ cls.clock_at_report = clock()
        # ~ if noskip or \
            # ~ clock_now - cls.clock_at_report > cls.report_period:
        # ~ m = " " + m + "\n"
        # ~ if cls._gui:
            # ~ cls.console.insert(Tkinter.END,"[yacaree]" + m)
            # ~ cls.console.see("end-2c")
            # ~ cls.console.update()
        # ~ else:
            # ~ print("[yacaree]" + m, end = '', flush = True)
            # ~ stdout.flush()
        # ~ if cls.logfile: 
            # ~ cls.logfile.write(str(datetime.now()) + m)


    # ~ @classmethod
    # ~ def reportwarning(cls, m = ""):
        # ~ "get warning to be an argument of report instead"
        # ~ cls.clock_at_report = clock()
        # ~ m = " " + m + "\n"
        # ~ cls.sound_bell()
        # ~ if cls._gui:
            # ~ cls.console.insert(Tkinter.END,"[yacaree warning]" + m)
            # ~ cls.console.see("end-2c")
            # ~ cls.console.update()
        # ~ else:
            # ~ print("[yacaree warning]" + m, end = '', flush = True)
        # ~ if cls.logfile: 
            # ~ cls.logfile.write(str(datetime.now()) + m)
        # ~ sleep(1)


    # ~ @classmethod
    # ~ def reporterror(cls, m = ""):
        # ~ "get error to be an argument of report instead"
        # ~ cls.clock_at_report = clock()
        # ~ cls.sound_bell()
        # ~ if cls._gui:
            # ~ cls.finish_button.configure(state = Tkinter.DISABLED)
            # ~ m += "\n"
            # ~ cls.console.insert(Tkinter.END,"[yacaree error] " + m)
            # ~ cls.console.configure(background = "misty rose")
            # ~ cls.console.update()
            # ~ sleep(8)
            # ~ cls.root.destroy()
        # ~ else:
            # ~ m = "Error: " + m + " Exiting.\n"
            # ~ sleep(2)
        # ~ if cls.logfile: 
            # ~ cls.logfile.write(str(datetime.now()) + " " + m)
        # ~ exit("[yacaree error] " + m)


    # ~ @classmethod
    # ~ def report_log_file(cls, filename):
        # ~ """
        # ~ Refactor so that the names are constructed only in one place -
        # ~ not reported like the rest for lack of log file
        # ~ """
        # ~ cls.clock_at_report = clock()
        # ~ m_log = " Log file " + filename + ".log (this file) set up.\n"
        # ~ m_cls = " Log file " + filename + ".log set up.\n"
        # ~ if cls._gui:
            # ~ cls.console.insert(Tkinter.END,"[yacaree]" + m_cls)
            # ~ cls.console.see("end-2c")
            # ~ cls.console.update()
        # ~ if cls.logfile: 
            # ~ "print already done, here just log entry (????)"
            # ~ cls.logfile.write(str(datetime.now()) + m_log)


    # ~ @classmethod
    # ~ def sound_bell(cls):
        # ~ if cls._gui:
            # ~ cls.console.bell()
        # ~ else:
            # ~ print('\a', end = '', flush = True)


    # ~ @classmethod # filename made a property now
    # ~ def storefilename(cls, filename):
        # ~ if len(filename)<=3 or filename[-4] != '.':
            # ~ cls.filename = filename
            # ~ cls.filenamefull = filename + cls.filenamext
        # ~ else:
            # ~ cls.filename, _ = filename.rsplit('.',1)
            # ~ cls.filenamefull = filename


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


    # ~ @classmethod
    # ~ def ask_input(cls, prompt):
        # ~ "Refactor, check only use is for dataset file, add a loop until correct"
        # ~ if cls.logfile: cls.logfile.write("Asked:" + prompt + "\n")
        # ~ ans = input(prompt)
        # ~ if cls.logfile: cls.logfile.write("Answer:" + ans + "\n")
        # ~ return ans
