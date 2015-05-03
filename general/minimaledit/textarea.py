
from Tkinter import *

class TextArea(Text):
    is_fullscreen = False
    
    textpack_conf = {"side": TOP, "expand":YES, "fill":Y, "anchor":CENTER}

    def __init__(self, parent=None):
        Text.__init__(self)
        self.config(font=('courier', 28, 'normal'), 
                    height=20,
                    # This is supposed to be "columns" but depending on the
                    # font size, I'm getting extra space. For example, with
                    # courier 20 normal font, I got 6 extra columns. For
                    # courier 28 normal font, I got no extra columns.
                    width=60,
                    background="#000000",
                    foreground="#00c322",
                    borderwidth=0,
                    highlightbackground="#000000",
                    wrap=WORD,
                    # BUG FIX: See function doc string for information.
                    xscrollcommand=self.correct_xscroll,
                    # Vocab:
                    # insert* settings correspond to the keyboard cursor.
                    # cursor* settings correspond to the mouse cursor.
                    insertbackground="#00c322")

        self.pack(**self.textpack_conf)

        self.mapkeys()

    def mapkeys(self):
        self.bind("<Tab>", self.ontab)

    def ontab(self, e):
        """Insert 4 spaces instead of a tab character.
        """
        self.insert(INSERT, "    ")
        # Cancel default behavior.
        return ("break")

    def correct_xscroll(self, *vargs):
        """Fix the accidental xscroll when it happens.
        
        This function exists solely for a bug that appears to exist on Mac
        OS X tkinter, which seems to be full of bugs.

        Correct and set any accidental horizontal scrolling back to no
        horizontal scrolling.
        """
        self.xview_moveto(0.0)

    def settext(self, text=''):
        self.delete('1.0', END)
        self.insert('1.0', text)
        self.mark_set(INSERT, '1.0')
        self.focus()

    def gettext(self):
        return self.get('1.0', END+'-1c')

    def findtext(self, target=''):
        t = self
        where = t.search(target, INSERT+"-1c", END)
        if where:
            pastit = where + ('+%dc' % len(target))
            t.tag_remove(SEL, '1.0', END)
            t.tag_add(SEL, where, pastit)
            t.mark_set(INSERT, pastit)
            t.see(INSERT)
            t.focus()

    def toggleminimal(self):
        if self.is_fullscreen == False:
            self.is_fullscreen = True            
        else:
            self.is_fullscreen = False
            
            

if __name__ == "__main__":
    s = TextPad()
    s.settext("Hello\nworld!")
    print s.gettext()
    s.master.bind('<Escape>', lambda a: s.toggleminimal())
    s.master.bind('<Control-f>', lambda a: s.findtext('Hello')) 
    s.master.mainloop()

