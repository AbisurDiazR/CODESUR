#!python3
"""tkinter and ExplorerBrowser
"""
# Original codes are from pywin32/com/win32comext/shell/demos explorer_browser.py
import sys
from tkinter import *
from tkinter.ttk import *

import pythoncom
import pywintypes
from win32com.shell import shell, shellcon
import win32gui
from win32com.server.util import wrap, unwrap


# event handler for the browser.
IExplorerBrowserEvents_Methods = """OnNavigationComplete OnNavigationFailed 
                                    OnNavigationPending OnViewCreated""".split()
class EventHandler:
    _com_interfaces_ = [shell.IID_IExplorerBrowserEvents]
    _public_methods_ = IExplorerBrowserEvents_Methods

    def OnNavigationComplete(self, pidl):
        print("OnNavComplete", pidl)

    def OnNavigationFailed(self, pidl):
        print("OnNavigationFailed", pidl)

    def OnNavigationPending(self, pidl):
        print("OnNavigationPending", pidl)

    def OnViewCreated(self, view):
        print("OnViewCreated", view)
        # And if our demo view has been registered, it may well
        # be that view!
        try:
            pyview = unwrap(view)
            print("and look - its a Python implemented view!", pyview)
        except ValueError:
            pass


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master, width=800, height=600)
        self.bind('<Destroy>', self.OnDestroy)
        self.bind('<Configure>', self.OnConfigure)
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.hwnd = pywintypes.HANDLE(self.winfo_id())

        eb = pythoncom.CoCreateInstance(shellcon.CLSID_ExplorerBrowser, None, pythoncom.CLSCTX_ALL, shell.IID_IExplorerBrowser)
        # as per MSDN docs, hook up events early
        self.event_cookie = eb.Advise(wrap(EventHandler()))

        eb.SetOptions(shellcon.EBO_SHOWFRAMES)
        rect = win32gui.GetClientRect(self.hwnd)
        # Set the flags such that the folders autoarrange and non web view is presented
        flags = (shellcon.FVM_LIST, shellcon.FWF_AUTOARRANGE | shellcon.FWF_NOWEBVIEW)
        eb.Initialize(self.hwnd, rect, (0, shellcon.FVM_DETAILS))
        if len(sys.argv)==2:
            # If an arg was specified, ask the desktop parse it.
            # You can pass anything explorer accepts as its '/e' argument -
            # eg, "::{guid}\::{guid}" etc.
            # "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}" is "My Computer"
            pidl = shell.SHGetDesktopFolder().ParseDisplayName(0, None, sys.argv[1])[1]
        else:
            # And start browsing at the root of the namespace.
            pidl = []
        eb.BrowseToIDList(pidl, shellcon.SBSP_ABSOLUTE)
        # and for some reason the "Folder" view in the navigator pane doesn't
        # magically synchronize itself - so let's do that ourself.
        # Get the tree control.
        sp = eb.QueryInterface(pythoncom.IID_IServiceProvider)
        try:
            tree = sp.QueryService(shell.IID_INameSpaceTreeControl,
                                   shell.IID_INameSpaceTreeControl)
        except pythoncom.com_error as exc:
            # this should really only fail if no "nav" frame exists...
            print("Strange - failed to get the tree control even though " \
                  "we asked for a EBO_SHOWFRAMES")
            print(exc)
        else:
            # get the IShellItem for the selection.
            si = shell.SHCreateItemFromIDList(pidl, shell.IID_IShellItem)
            # set it to selected.
            tree.SetItemState(si, shellcon.NSTCIS_SELECTED, shellcon.NSTCIS_SELECTED)

        #eb.FillFromObject(None, shellcon.EBF_NODROPTARGET); 
        #eb.SetEmptyText("No known folders yet...");  
        self.eb = eb

    def OnDestroy(self, event):
        print("tearing down ExplorerBrowser...")
        self.eb.Unadvise(self.event_cookie)
        self.eb.Destroy()
        self.eb = None

        self.hwnd.Detach()
        self.hwnd = None

    def OnConfigure(self, event):
        x = event.width
        y = event.height
        self.eb.SetRect(None, (0, 0, x, y))


if __name__ == '__main__':
    root = Tk()
    app = Application(master=root)
    app.mainloop()