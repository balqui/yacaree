"""
A simple Tkinter-based GUI for yacaree
"""

import Tkinter
import tkFileDialog
import tkFont
from datetime import datetime

import statics

class iface:

    @classmethod
    def go(cls,mainprog):
        cls.root = Tkinter.Tk()
        left_frame = Tkinter.Frame(cls.root)
        left_frame.pack(side=Tkinter.LEFT)
        logo = Tkinter.BitmapImage(file="yac-v03.xbm")
        logo_frame = Tkinter.Frame(left_frame)
        logo_frame.pack(side = Tkinter.TOP)
        slogan_label = Tkinter.Label(left_frame, text =
                                     "yet another closure-based association " +
                                     "rules\nexperimentation environment")
        slogan_label.pack(side=Tkinter.TOP)
        logo_label = Tkinter.Label(logo_frame,image=logo)
        namefont = tkFont.Font(family = "Helvetica",
                               size = 18,
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
        cls.console.pack(side=Tkinter.LEFT)
        cls.scrollY = Tkinter.Scrollbar(console_frame,
                                    orient = Tkinter.VERTICAL,
                                    command = cls.console.yview)
        cls.scrollY.pack(side=Tkinter.LEFT, fill = Tkinter.Y)
        cls.console.configure(yscrollcommand = cls.scrollY.set)

        button_width = 30
        button_height = 5

        cls.filepick = Tkinter.Button(process_frame)
        cls.filepick.configure(text = "1/ Choose a \ndataset file",
                               width = button_width,
                               height = button_height,
                               command = cls.choose_datafile)
        cls.filepick.pack()

        cls.run = Tkinter.Button(process_frame)
        cls.run.configure(text = "2/ Run yacaree\n(and be patient)",
                          width = button_width,
                          height = button_height,
                          state = Tkinter.DISABLED,
                          command = mainprog.standard_run)
        cls.run.pack()

        cls.finish_button = Tkinter.Button(process_frame)
        cls.finish_button.configure(text = "3/ Finish",
                                  width = button_width,
                                  height = button_height,
                                  command = cls.finish)
        cls.finish_button.pack()
        cls.root.mainloop()

    @classmethod
    def choose_datafile(cls):
        fnm = tkFileDialog.askopenfilename(
            defaultextension=".txt",
            filetypes = [("text files","*.txt"), ("all files","*.*")],
            title = "Choose a dataset file")
        if fnm:
            cls.run.configure(state = Tkinter.NORMAL)
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
    def report(cls,m):
        m = " " + m + "\n"
        cls.console.insert(Tkinter.END,"[yacaree]" + m)
        cls.console.see("end-2c")
        cls.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m)

    @classmethod
    def endreport(cls):
        pass

    @classmethod
    def reportwarning(cls,m):
        m = " " + m + "\n"
        cls.console.insert(Tkinter.END,"[yacaree warning]" + m)
        cls.console.see("end-2c")
        cls.console.update()
        if statics.logfile: 
            statics.logfile.write(str(datetime.now()) + m)

    @classmethod
    def reporterror(cls,m):
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
    

    
