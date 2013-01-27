"""
A simple Tkinter-based GUI for yacaree
"""

import Tkinter
import tkFileDialog
import tkFont
from datetime import datetime
from time import clock

import statics

class iface:

    @classmethod
    def go(cls,mainprog):
        cls.root = Tkinter.Tk()

        button_width = 25
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
                                     "rules\nexperimentation environment\n(" +
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
        cls.report("This is yacaree " + statics.version) 

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
        cls.clock_at_report = clock()
        cls.root.mainloop()

    @classmethod
    def choose_datafile(cls):
        fnm = tkFileDialog.askopenfilename(
            defaultextension=".txt",
            filetypes = [("text files","*.txt"), ("all files","*.*")],
            title = "Choose a dataset file")
        if fnm:
            cls.run.configure(state = Tkinter.NORMAL)
            cls.run50.configure(state = Tkinter.NORMAL)
            statics.filenamefull = fnm
            statics.filename, statics.filenamext = fnm.rsplit('.',1)
            cls.report("Selected dataset in file " + fnm)

    @classmethod
    def finish(cls):
        if statics.logfile: statics.logfile = None
        cls.root.destroy()
        exit(0)

    @classmethod
    def enable_again(cls):
        cls.run.configure(state = Tkinter.DISABLED)
        cls.run50.configure(state = Tkinter.DISABLED)
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

if __name__ == "__main__":

    i = iface()
    

    
