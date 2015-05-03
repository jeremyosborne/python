minimaledit
a very simple, full screen text editor
by Jeremy Osborne



TODO
====
* Make a configuration file.
* Can't use any of the included dialogs as they make the mac top bar
  menu appear. Need to code everything by hand (ugh).
    * Near term solution: force the file to open on load,
      or if no file is chosen, it's a new file.
      Then at least we can edit in peace before we need to
      begin.
      After file is open, expand the screen.
* Need to modify the message boxes when in minimal mode so they don't cause
  the menu bar to come back.
* Change the name of ScrollText to something simple, like textarea.
* Make pressing the tab key insert 4 spaces, not a tab.
* Make a display of information about:
    * How many lines the file is in this view.
    * Which column and line the cursor is on.
    * How many words are in the file.
    * Make the display of the information toggleable.
    * Make the display possible in a popup window.

