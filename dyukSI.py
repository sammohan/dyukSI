# -*- coding: utf-8 -*-

#####################
'''Status line at the bottom
is working good here.
'''
#####################
from  tkinter import *
from  tkinter.filedialog import *
from tkinter import ttk
from tkinter.scrolledtext import *
import os

from  sanHarvardKyoto import *
from  engVirgin import *

TITLE = "संयुक्ता"

class IndicEditor(Text, object):
    def __init__(self, master, **options):
        Text.__init__(self, master, **options)

        self.config(
            borderwidth=0,
            font=("Mangal", 11),
            foreground="white",
            background="black",
            insertbackground="yellow", # cursor
            selectforeground="white", # selection
            selectbackground="grey",
            wrap=WORD, # use word wrapping
            undo=True,
            width=64,
            )
        self.filename = None # current document

    def _getfilename(self):
        return self._filename

    def _setfilename(self, filename):
        self._filename = filename
        title = os.path.basename(filename or "(new document)")
        title = title + " - " + TITLE
        self.winfo_toplevel().title(title)

    filename = property(_getfilename, _setfilename)

    def resetTitle(self):
        title = "(new document)"
        title = title + " - " + TITLE
        self.winfo_toplevel().title(title)
 
    def load(self, filename):
            text = open(filename, mode='rb').read()
            self.delete(1.0, END)
            self.insert(END, text.decode('utf8'))
            self.mark_set(INSERT, 1.0)
            self.edit_modified( False )
            self.filename = filename

    def save(self, filename=None):
            if filename is None:
                filename = self.filename
            f = open(filename, "wb")
            s = self.get(1.0, END)
            try:
                tdt = s.rstrip() # remove tkinter's whitespace junk at end
                f.write(tdt.encode('utf8'))  # write data
                f.write("\n".encode('utf8')) # add a newline
                f.close()
            finally:
                f.close()
            self.edit_modified( False )
            self.filename = filename

    def onUndo(self):
        try:
            self.edit_undo()
        except TclError:                # exception if stacks empty
            showinfo('SaMyuktA', 'Nothing to undo')

    def onRedo(self):
        try:
            self.edit_redo()
        except TclError:
            showinfo('SaMyuktA', 'Nothing to redo')
        
FILETYPES = [
    ("Text files", "*.txt"), ("All files", "*")
    ]

class Cancel(Exception):
    pass

def open_as():
    f = filedialog.askopenfilename(parent=root, filetypes=FILETYPES)
    if not f:
        raise Cancel
    try:
        editor.load(f)
    except IOError:
        from tkMessageBox import showwarning
        showwarning("Open", "Cannot open the file.")
        raise Cancel

def save_as():
    f = filedialog.asksaveasfilename(parent=root, defaultextension=".txt")
    if not f:
        raise Cancel
    try:
        editor.save(f)
    except IOError:
        from messageBox import showwarning
        showwarning("Save As", "Cannot save the file.")
        raise Cancel

def save():
    if editor.filename:
        try:
            editor.save(editor.filename)
        except IOError:
            from tkMessageBox import showwarning
            showwarning("Save", "Cannot save the file.")
            raise Cancel
    else:
        save_as()

def saveIfModified():
    if (editor.edit_modified() == False):
        return
    if messagebox.askyesno(TITLE, "Document modified. Save changes?"):
        save()
        editor.edit_modified( False )

def file_new(event=None):
    try:
        saveIfModified()
        editor.delete('1.0', END)
        editor.resetTitle()
    except Cancel:
        pass
    return "break" # don't propagate events

def file_open(event=None):
    try:
        saveIfModified()
        open_as()
    except Cancel:
        pass
    return "break"

def file_save(event=None):
    try:
        if (editor.edit_modified() == True):
            save()
    except Cancel:
        pass
    return "break"

def file_save_as(event=None):
    try:
        save_as()
    except Cancel:
        pass
    return "break"

def file_quit(event=None):
    try:
        saveIfModified()
    except Cancel:
        return
    root.destroy()

def about_command():
    label = messagebox.showinfo(
            "About",
            "संयुक्ता - Sanskrit Editor\nCopyright © 2016 www.SpokenSanskrit.org\nAll Rights Reserved.")

def howtouse():
    ''' This has to have a tab for each encoding
    scheme and one for Intro and one tab for
    misc. info
    '''
    hwin = Toplevel( root )
    hwin.title( "Harvard-Kyoto Transliteration Map" )
    frame1 = Frame( master = hwin, bg = '#001a00' )
    frame1.pack(fill='both', expand='yes')
    editArea = Text( master = frame1, wrap = WORD, width = 86, height = 39 )
    editArea.pack( padx=10, pady=10, fill=BOTH, expand=True )
    khImage = PhotoImage(file ="./KH-scheme.gif")
    editArea.image = khImage  # keep ref. to image!
    editArea.image_create( '1.0', image = khImage)
    hwin.protocol( "WM_DELETE_WINDOW", hwin.destroy)

def dummy():
    print( "Not Implemented" )

## .......................................
def onFind( event=None ):
    t2=Toplevel( root )

    def close_search():
        editor.tag_remove( 'match', '1.0', END)
        t2.destroy()

    t2.title( "Find" )
    t2.geometry( '381x68+200+250' )
    t2.transient( root )

    Label(t2, text = "Find:").grid( row = 0, column = 0, sticky = 'e' )
    
    e = Text( t2 ) 
    e.grid( row=0, column =1, padx =2, pady=2, sticky='we')
    e.config(
        width = 30,
        height = 1, 
        font=("Mangal", 11),
        foreground="white",
        background="black",
        insertbackground="yellow", # cursor
        )
    e.lastneedle = None
    editor.srchindex = '1.0'
    e.focus_set()
    
    Button(t2, text = "Find Next", command = lambda: search( c.get(), editor,
                                                                 t2, e)).grid(row =0, column =2,
                                                                                       sticky = 'e'+'w', padx = 2,
                                                                                       pady = 2)

    c = IntVar()
    c.set(2)
    
    Radiobutton(t2, text="Forward", variable=c, value=2).grid( row = 1, column = 1, sticky = 'w' )
    Radiobutton(t2, text="Backward", variable=c, value=1).grid( row = 1, column = 1, sticky = 'e' )

    Button(t2, text = "Cancel", command = close_search).grid( row =1, column =2,
                                                                                       sticky = 'e', padx = 2,
                                                                                       pady = 2)

    t2.protocol( "WM_DELETE_WINDOW", close_search)

    ## .................Local scope function.....................
    def search( upordown, editor, t2, e ):
        needle = e.get( "insert linestart", INSERT)
        if not needle: return
        if upordown == 1:
            backwards = 1 # up
            idx = '%s-%dc' % (editor.index( INSERT ), len( needle ))   
        else:
            backwards = 0 # down
            idx = editor.index( INSERT )
        idx = editor.search( needle, idx, nocase=1, backwards = backwards )
        if not idx: return
        lastidx = '%s+%dc' % (idx, len( needle ))
        editor.tag_remove('match', '1.0', 'end')
        editor.tag_remove(SEL, '1.0', 'end')
        editor.tag_add('match', idx,  lastidx)
        editor.tag_add(SEL, idx,  lastidx)
        editor.tag_config( 'match', foreground = 'red', background = 'yellow')
        editor.mark_set("insert", lastidx)
        editor.see(INSERT)
        editor.focus_force()
        e.focus_set()

## .............................................    
root = Tk()
root.wm_state("zoomed")
menu = Menu(root)
root.config(menu=menu, background ="#001a00") #margin color

## -----
editor = IndicEditor(root)
editor.pack(fill=Y, expand=1, pady=0)
editor.focus_set()
## -----
filemenu = Menu( menu, tearoff = 0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=file_new, accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=file_open, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=file_save, accelerator="Ctrl+S")
filemenu.add_command(label="Save as...", command=file_save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=file_quit, accelerator="<Ctrl+Q>")
# ---
editmenu = Menu(menu, tearoff = 0)
menu.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", command=editor.onUndo, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=editor.onRedo, accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Find", command=onFind, accelerator="Ctrl+F")
editmenu.add_separator()
editmenu.add_command(label="Preferences", command=dummy)
# ---
helpmenu = Menu(menu, tearoff = 0)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="How to use...", command=howtouse)
helpmenu.add_separator()
helpmenu.add_command(label="About...", command=about_command)
# ---Provide status bar at the bottom to display current settings

statusFrame = Frame(root)
statusFrame.pack(side=BOTTOM, fill=X)

mapLabel = Label( statusFrame, text="Map: ", relief=SUNKEN)
mapLabel.pack( side = LEFT)

scriptLabel = Label( statusFrame, text="Script: ", relief=SUNKEN)
scriptLabel.pack( side = LEFT )

langLabel = Label( statusFrame, text="Lang: ", relief=SUNKEN)
langLabel.pack( side = LEFT )

colLabel = Label( statusFrame, text="Col: ", relief=SUNKEN)
colLabel.pack( side = RIGHT)

lineLabel = Label( statusFrame, text="Ln: " ,relief=SUNKEN)
lineLabel.pack( side = RIGHT )

#------------

# punctuations
lekhanacihnam = ['exclam', 'quotedbl', 'numbersign', 'dollar', 'percent',
                 'quoteright', 'parenleft', 'parenright', 'asterisk', 'plus', 'comma',
                 'minus', 'period', 'slash', 'colon', 'semicolon', 'less', 'equal',
                 'greater', 'question', 'at', 'bracketleft', ' backslash', 'bracketright',
                 'asciicircum', 'underscore', 'quoteleft', 'braceleft', 'bar', 'braceright',
                 'asciitilde', 'ampersand']

class _nirdezakaH( object ):
    'परिवर्तनं केन साधनेन करणीयमिति सूचयति'

    def __init__(self, map='KyotoHarvard', form='Devanagari',
                 infont='Mangal', infontsz=11, bhASA='Sanskrit'):      
        self.lang = bhASA
        self.script = form
        self.transliteration = map
        self.font = infont
        self.fontsz = infontsz
        self.escaped = False

        self.currentLang = bhASA
        self.currentScript = form
        self.currentTrans = map
        self.currentLine = 1
        self.currentCol = 0

    def displayStatus( self, event =  None ):
        strLoc = editor.index( INSERT )
        loc = strLoc.split('.')
        self.currentLine = loc[0]
        self.currentCol = loc[1]
        langLabel.config( text = 'Lang: ' + self.currentLang )
        scriptLabel.config( text = 'Script: ' + self.currentScript )
        mapLabel.config( text = 'Map: ' + self.currentTrans )
        lineLabel.config( text = 'Line: ' + str(self.currentLine))
        colLabel.config( text = 'Col: ' + str(self.currentCol ))
        statusFrame.update_idletasks()
 
    def setLang( self, lang ):
        self.lang = lang

    def setScript ( self, script ):
        self.script = script

    def setMap( self, map ):
        self.transliteration = map

    def toggle( self ):
        self.escaped = not( self.escaped )
        if self.escaped:
            self.currentLang = 'LatinAny'
            self.currentScript = 'Latin'
            self.currentTrans = 'None'
        else:
            self.currentLang = self.lang
            self.currentScript = self.script
            self.currentTrans = self.transliteration
        self.displayStatus() # update GUI status
#............................................................        
def siddhatAkR(event):
    ## उपकरणतः सद्यावलिः आनय
    saAva = event.widget.get( "insert linestart", INSERT)

    ## यत्र अवधिः भवति तत्र खण्डयतु
    zabdAvali = saAva.split(' ')
    if len( zabdAvali ) > 1:
        zabdAvali[-1] = zabdAvali[-2] + ' ' + zabdAvali[-1]
        zabdAvali.pop(-2)
    ## परिवर्तनं कुरु
    if nirdezakaH.currentScript == 'Devanagari':
        zabdAvali[-1] = sanHK_parivRtyatAm( event.keysym,  zabdAvali[-1] )
    else:
        # Latin mode, skip conversion
        zabdAvali[-1] = engVirgin_parivRtyatAm( event.keysym,  zabdAvali[-1] )

    #sarvaM yojaya
    nu_saAva = ' '.join(zabdAvali)

    ## उपकरणे [in widget] अभ्यन्तरी कुरु
    event.widget.delete( "insert linestart", INSERT )  # delete old
    event.widget.insert( INSERT, nu_saAva)
    return
#............................................................
def ghaTanA( event ):
    nirdezakaH.displayStatus() # update status at the bottom
    if event.char==event.keysym:
        siddhatAkR( event )
    elif event.keysym in lekhanacihnam:
        siddhatAkR( event )
    elif event.keysym == "Escape":
        nirdezakaH.toggle()
#............................................................
# instantiate mode manager
nirdezakaH = _nirdezakaH()
nirdezakaH.displayStatus() # update status at the bottom
root.bind_all( '<Key>', ghaTanA )
root.bind("<Button-1>", nirdezakaH.displayStatus )
root.bind("<Control-n>", file_new)
root.bind("<Control-o>", file_open)
root.bind("<Control-s>", file_save)
root.bind("<Control-Shift-S>", file_save_as)
root.bind("<Control-f>", onFind)
root.bind("<Control-q>", file_quit)

root.protocol("WM_DELETE_WINDOW", file_quit) # window close button

try:
    editor.load(sys.argv[1])
except (IndexError, IOError):
    pass

mainloop()
''' To-do
Turn the code into OO
config menu/pop-up - change translit., target script, target lang, font & size
preserve in a cookie - (ala darkroom)
    current config,
    unsaved editor,
    search string,
    [un]zoom option]
    Recently saved files
Add ITRANS, Velthuis, WX, SLP1, 
Backspace - "completely delete what was entered with a single key"
From Basic-English spell checker, create dictionary of 5000+ words and their 7 vibhatis. use that for
spell-check  :-)
'''
