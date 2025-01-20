"""
yacaree

Current revision: late Frimaire 2024

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)
"""

from datetime import datetime

class FileNames:

    def __init__(self, iface):
        """
        The property setter for filename handles most of the values.
        """
        self.iface = iface
        self._filename = None
        self._filenamefull = None
        self._filenamenow = None
        self._filenamext = ".txt" # TO MOVE ON INTO .td ONE DAY

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
