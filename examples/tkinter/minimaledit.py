
import re
from Tkinter import *
from scrolltext import ScrollText
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename, askopenfilename
from tkMessageBox import askokcancel


class MinimalEdit(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("MinimalEdit")

        self.isMinimal = False
        self.prevGeometry = None
        
        self.makewidgets()

        self.protocol("WM_DELETE_WINDOW", self.onquit)

    def makewidgets(self):
        self.actionbuttons = Frame(self)
        self.actionbuttons.pack(side=TOP, expand=NO, fill=X)
        Button(self.actionbuttons, text='New', command=self.onnew).pack(side=LEFT)
        Button(self.actionbuttons, text='Load', command=self.onload).pack(side=LEFT)
        Button(self.actionbuttons, text='Save', command=self.onsave).pack(side=LEFT)
        Button(self.actionbuttons, text='Find', command=self.onfind).pack(side=LEFT)

        self.scrolltext = ScrollText(self)

    def onquit(self):
        ans = askokcancel("Verify exit", "Really quit?")
        if ans:
            self.quit()

    def onnew(self):
        ans = askokcancel("Verify new file", "Really start a new file?")
        if ans:
            self.scrolltext.settext(text='')

    def onload(self):
        filename = askopenfilename()
        if filename:
            f = open(filename, 'r')
            alltext = f.read()
            self.scrolltext.settext(alltext)
            f.close()

    def onsave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.scrolltext.gettext()
            f = open(filename, 'w') 
            f.write(alltext)
            f.close()

    def onfind(self):
        target = askstring('Search String', '')
        if target:
            self.scrolltext.findtext(target)

    def setfullscreen(self):
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

    def storegeometry(self):
        pg = re.split(r"x|\+", self.geometry())
        self.prevGeometry = tuple(pg)

    def restoreprevgeometry(self):
        self.overrideredirect(False)
        if self.prevGeometry:
            self.geometry("{0[0]}x{0[1]}+{0[2]}+{0[3]}".format(self.prevGeometry))

    def toggleminimal(self):
        if self.isMinimal == False:
            self.isMinimal = True

            self.storegeometry()

            self.setfullscreen()

            self.actionbuttons.pack_forget()
            self.scrolltext.toggleminimal()

        else:
            self.isMinimal = False

            self.restoreprevgeometry()

            self.actionbuttons.pack(side=TOP, expand=NO, fill=X)
            self.scrolltext.toggleminimal()


if __name__ == '__main__':
    s = MinimalEdit()

    s.bind("<Control-n>", lambda a: s.onnew())
    s.bind("<Control-l>", lambda a: s.onload())
    s.bind("<Control-s>", lambda a: s.onsave())
    s.bind("<Control-f>", lambda a: s.onfind())
    s.bind("<Escape>", lambda a: s.toggleminimal())

    s.mainloop()
