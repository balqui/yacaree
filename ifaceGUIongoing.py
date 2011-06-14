"""
Alternative interface with a simple Tkinter-based GUI
"""

from datetime import datetime
import Tkinter
import tkFileDialog

import statics

class iface:

    @classmethod
    def go(cls):
        cls.root = Tkinter.Tk()
        midframe = Tkinter.Frame(cls.root)
        midframe.pack()
        cls.console = Tkinter.Text(cls.root)
        cls.console.pack()
        filepick = Tkinter.Button(midframe)
        filepick.configure(text = "Choose dataset file",
                           command = cls.opendatafile)
        filepick.pack(side=Tkinter.LEFT)

        finetune = Tkinter.LabelFrame(midframe,
                                      text = "Process:",
                                      highlightcolor = "green"
                                      )
        finetune.pack(side=Tkinter.LEFT)
        cls.fineprocess = Tkinter.IntVar()
        cls.fineprocess.set(0)
        finebuttonwidth = 10
        finetune_std = Tkinter.Radiobutton(finetune)
        finetune_std.configure(text = "Standard",
                               width = finebuttonwidth,
                               anchor = Tkinter.W,
                               command = cls.indicator,
                               value = 0,
                               variable = cls.fineprocess)
        finetune_std.pack()
        finetune_gen = Tkinter.Radiobutton(finetune)
        finetune_gen.configure(text = "Generous",
                               width = finebuttonwidth,
                               anchor = Tkinter.W,
                               command = cls.indicator,
                               value = 1,
                               variable = cls.fineprocess)
        finetune_gen.pack()
        finetune_mnn = Tkinter.Radiobutton(finetune)
        finetune_mnn.configure(text = "Mean",
                               width = finebuttonwidth,
                               anchor = Tkinter.W,
                               command = cls.indicator,
                               value = 2,
                               variable = cls.fineprocess)
        finetune_mnn.pack()

    @classmethod
    def indicator(cls):
        "use a to modify the statics"
        a = cls.fineprocess.get()
        cls.console.insert(2.3,a)

    @classmethod
    def opendatafile(cls):
        fnm = tkFileDialog.askopenfilename(
            defaultextension=".txt",
            filetypes = [("text files","*.txt"), ("all files","*.*")],
            title = "Select a dataset file")
        if fnm:
            cls.openfile(fnm)


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

    ifa = iface()
    ifa.go()
    ifa.root.mainloop()

    

    
