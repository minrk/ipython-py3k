""" Utilities for accessing the platform's clipboard.
"""

import subprocess
import sys

from IPython.core.error import TryNext


def win32_clipboard_get():
    """ Get the current clipboard's text on Windows.

    Requires Mark Hammond's pywin32 extensions.
    """
    try:
        import win32clipboard
    except ImportError:
        message = ("Getting text from the clipboard requires the pywin32 "
            "extensions: http://sourceforge.net/projects/pywin32/")
        raise TryNext(message)
    win32clipboard.OpenClipboard() 
    text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT) 
    # FIXME: convert \r\n to \n?
    win32clipboard.CloseClipboard() 
    return text

def osx_clipboard_get():
    """ Get the clipboard's text on OS X.
    """
    p = subprocess.Popen(['pbpaste', '-Prefer', 'ascii'],
        stdout=subprocess.PIPE)
    text, stderr = p.communicate()
    # Text comes in with old Mac \r line endings. Change them to \n.
    text = text.replace('\r', '\n')
    return text

def tkinter_clipboard_get():
    """ Get the clipboard's text using Tkinter.

    This is the default on systems that are not Windows or OS X. It may
    interfere with other UI toolkits and should be replaced with an
    implementation that uses that toolkit.
    """
    try:
        import tkinter
    except ImportError:
        message = ("Getting text from the clipboard on this platform "
            "requires Tkinter.")
        raise TryNext(message)
    root = tkinter.Tk()
    root.withdraw()
    text = root.clipboard_get()
    root.destroy()
    return text


