import vim
import dbus

bus = dbus.SessionBus()
proxy_obj = bus.get_object(vim.eval('g:audiobox_dbus_dest'),
                            vim.eval('g:audiobox_dbus_path'))
player = dbus.Interface(proxy_obj, vim.eval('g:audiobox_dbus_interface'))
properties = dbus.Interface(proxy_obj, vim.eval('g:audiobox_dbus_properties_interface'))

def trycatch(func):
    def wrap_function():
        try:
            func()
        except dbus.exceptions.DBusException:
            vim.command("echohl Error | echom \"Player not launched\" | echohl None")
        except dbus.exceptions.UnknownMethodException:
            vim.command("echohl Error | echom \"Unknown method!?\" | echohl None")
        except:
            vim.command("echohl Error | echom \"Unknown exception!\" | echohl None")
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
