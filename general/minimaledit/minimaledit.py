"""A minimal, full screen text editor.

"""

import re
from Tkinter import *
from textarea import TextArea
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename, askopenfilename
from tkMessageBox import askokcancel
import os_sniffer



class MinimalEdit(Tk):
    """The minimaledit application.
    
    Create, and then call the .mainloop() method.
    
    """

    is_fullscreen = False
    saved_geometry = None
    textarea = None

    def __init__(self):
        Tk.__init__(self)

        self.makewidgets()

        self.mapkeys()

        self.style()

        # Catch the "click on close" event.
        self.protocol("WM_DELETE_WINDOW", self.onquit)

    def style(self):
        self.config(background="#000000",
                    borderwidth=0,
                    highlightbackground="#000000")
        if os_sniffer.is_mac:
            # Trying to get rid of the title bar on a mac.
            # This must be done before the window is actually created.
            # If we want to be able to have a title bar in windowed mode and
            # have no title bar in minimal editing mode, we'll need to rebuild
            # the window.
            self.tk.call("::tk::unsupported::MacWindowStyle", "style", self._w, "plain", "noTitleBar")
            # On Mac OS X, attempt to make the window appear on top vs. behind
            # other windows.
            # This is a total hack, but it seems to work quite well.
            # We set up a delayed callback that will ensure the application is
            # up and running, force the application to be topmost which will,
            # even on mac move the application above all other windows in the
            # desktop, but then allow the window to lose focus later if the user
            # chooses to switch to another application in the desktop.
            # I'm working around an apparent bug according to the interwebs,
            # but it seems to work.
            # NOTE: The best I can do with this so far is setting the window on
            # top. Having the window have focus is not happening when not running
            # this application as a py2app.
            # TODO: test running as a py2app to see if I can grab focus.
            def mac_osx_lift_callback():
                self.tk.call('wm', 'attributes', '.', '-topmost', '1')
                self.tk.call('update')
                self.tk.call('wm', 'attributes', '.', '-topmost', '0')
                self.tk.call('update')
            self.after(100, mac_osx_lift_callback)

    def makewidgets(self):
        self.title("MinimalEdit")
        self.textarea = TextArea(self)

    def mapkeys(self):
        if os_sniffer.is_mac:
            command_key = "Command"
        else:
            command_key = "Control"
        self.bind("<"+command_key+"-n>", lambda a: self.onnew())
        self.bind("<"+command_key+"-l>", lambda a: self.onload())
        self.bind("<"+command_key+"-s>", lambda a: self.onsave())
        self.bind("<"+command_key+"-f>", lambda a: self.onfind())
        self.bind("<"+command_key+"-q>", lambda a: self.onquit())
        self.bind("<Escape>", lambda a: self.toggleminimal())

    def onquit(self):
        ans = askokcancel("Verify exit", "Really quit?")
        if ans:
            # NOTE: On Mac, there seems to be a bug with preventing the
            # program from quitting. We can intercept the event and do
            # what clean up we need to do here. However, once this function 
            # exits, on mac os x (but not on windows) our program will close
            # no matter what. This is a tkinter version problem on mac.
            # TODO: Need to confirm that I'm using the non-Apple tkinter.
            self.quit()

    def onnew(self):
        ans = askokcancel("Verify new file", "Really start a new file?")
        if ans:
            self.textarea.settext(text='')

    def onload(self):
        filename = askopenfilename()
        if filename:
            f = open(filename, 'r')
            alltext = f.read()
            self.textarea.settext(alltext)
            f.close()

    def onsave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.textarea.gettext()
            f = open(filename, 'w') 
            f.write(alltext)
            f.close()

    def onfind(self):
        target = askstring('Search String', '')
        if target:
            self.textarea.findtext(target)

    def storegeometry(self):
        pg = re.split(r"x|\+", self.geometry())
        self.saved_geometry = tuple(pg)

    def restoregeometry(self):
        if self.saved_geometry:
            self.geometry("{0[0]}x{0[1]}+{0[2]}+{0[3]}".format(self.saved_geometry))
    
    def setfullscreenview(self):
        # Store the previous geometry
        self.storegeometry()

        if os_sniffer.is_mac:
            # Assuming this is TK 8.5 or higher
            self.wm_attributes('-fullscreen', 1)
        # Default for all systems
        self.overrideredirect(1)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

    def setwindowedview(self):
        if os_sniffer.is_mac:
            # Assuming this is TK 8.5 or higher
            self.wm_attributes('-fullscreen', 0)
        # Default for all systems
        self.overrideredirect(0)
        self.restoregeometry()

    def toggleminimal(self):
        if self.is_fullscreen == False:
            self.is_fullscreen = True
            self.setfullscreenview()
            self.textarea.toggleminimal()            
        else:
            self.is_fullscreen = False
            self.setwindowedview()
            self.textarea.toggleminimal()



if __name__ == '__main__':
    app = MinimalEdit()
    # Our job to call the mainloop when we're ready.
    app.mainloop()


