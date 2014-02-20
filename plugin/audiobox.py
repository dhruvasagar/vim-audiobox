import vim
from dbus import SessionBus, Interface, DBusException, UnknownMethodException

bus = SessionBus()
proxy_obj = bus.get_object(vim.eval('g:audiobox_dbus_dest'),
                            vim.eval('g:audiobox_dbus_path'))
player = Interface(proxy_obj, vim.eval('g:audiobox_dbus_interface'))
properties = Interface(proxy_obj, vim.eval('g:audiobox_dbus_properties_interface'))

def trycatch(func):
    def wrap_function():
        try:
            func()
        except DBusException:
            vim.command("echoerr \"Player not launched!\"")
        except UnknownMethodException:
            vim.command("echoerr \"Unknown method!?\"")
        except:
            vim.command("echoerr \"Unknown exception!\"")
    return wrap_function

@trycatch
def Play():
    """Play current song"""
    player.Play()

@trycatch
def Pause():
    """Pause current song"""
    player.Pause()

@trycatch
def Next():
    """Play the next song"""
    player.Next()

@trycatch
def Prev():
    """Play the previous song"""
    player.Previous()

@trycatch
def PlayPause():
    """Play / Pause the current song"""
    player.PlayPause()

@trycatch
def Stop():
    """Stop the current song"""
    player.Stop()

@trycatch
def GetCurrentSong():
    """Get the title of the current song"""
    metadata = properties.Get(vim.eval('g:audiobox_dbus_interface'), 'Metadata')
    vim.command("echohl String | echom \"" + ("Song: %s, Artist: %s, Album: %s" % (str(metadata['xesam:title']), str(metadata['xesam:artist'][0]), str(metadata['xesam:album']))) + "\" | echohl None")
