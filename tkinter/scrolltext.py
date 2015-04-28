
from Tkinter import *

sbarPackConf = {"side":RIGHT, "fill":Y}
textPackConf = {"side":LEFT, "expand":YES, "fill":BOTH}
framePackConf = {"expand":YES, "fill":BOTH}

class ScrollText(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(**framePackConf)
        self.makewidgets()
        self.isMinimal = False

    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self)
        
        sbar.config(command=text.yview)
        sbar.pack(**sbarPackConf)
        self.sbar = sbar

        text.config(yscrollcommand=sbar.set, font=('courier', 20, 'normal'), height=20)
        text.pack(**textPackConf)
        self.text = text

    def settext(self, text=''):
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0', END+'-1c')

    def findtext(self, target=''):
        t = self.text
        where = t.search(target, INSERT+"-1c", END)
        if where:
            pastit = where + ('+%dc' % len(target))
            t.tag_remove(SEL, '1.0', END)
            t.tag_add(SEL, where, pastit)
            t.mark_set(INSERT, pastit)
            t.see(INSERT)
            t.focus()

    def toggleminimal(self):
        if self.isMinimal == False:
            self.isMinimal = True
            self.sbar.pack_forget()
        else:
            self.isMinimal = False
            self.pack_forget()
            self.text.pack_forget()

            self.pack(**framePackConf)
            self.sbar.pack(**sbarPackConf)
            self.text.pack(**textPackConf)

if __name__ == "__main__":
    s = ScrollText()
    s.settext("Hello\nworld!")
    print s.gettext()
    s.master.bind('<Escape>', lambda a: s.toggleminimal())
    s.master.bind('<Control-f>', lambda a: s.findtext('Hello')) 
    s.mainloop()

