import vim
from traceback import print_exc
from dbus import SessionBus, Interface, DBusException, UnknownMethodException

class Audiobox():
    """Audiobox class"""
    def __init__(self):
        self.bus = SessionBus()
        self.init()

    def init(self):
        self.proxy_obj = self.bus.get_object(vim.eval('g:audiobox_dbus_dest'),
                                             vim.eval('g:audiobox_dbus_path'))
        self.player = Interface(self.proxy_obj, vim.eval('g:audiobox_dbus_interface'))
        self.properties = Interface(self.proxy_obj, vim.eval('g:audiobox_dbus_properties_interface'))

    def Play(self):
        """Play current song"""
        if self.player:
            self.player.Play()

    def Pause(self):
        """Pause current song"""
        if self.player:
            self.player.Pause()

    def Next(self):
        """Play the next song"""
        if self.player:
            self.player.Next()

    def Prev(self):
        """Play the previous song"""
        if self.player:
            self.player.Previous()

    def PlayPause(self):
        """Play / Pause the current song"""
        if self.player:
            self.player.PlayPause()

    def Stop(self):
        """Stop the current song"""
        if self.player:
            self.player.Stop()

    def GetCurrentSong(self):
        """Get the title of the current song"""
        if self.properties:
            metadata = self.properties.Get(vim.eval('g:audiobox_dbus_interface'), 'Metadata')
            if len(metadata) > 0:
                vim.command("echohl String | echom \"" + ("Song: %s, Artist: %s, Album: %s"
                    % (str(metadata['xesam:title']),
                        str(metadata['xesam:artist'][0]),
                        str(metadata['xesam:album']))) + "\" | echohl None")

audioboxObject = None
def setup():
    """return audiobox instance"""
    global audioboxObject
    try:
        if audioboxObject is None:
            audioboxObject = Audiobox()
        else:
            audioboxObject.init()
        return audioboxObject
    except DBusException:
        vim.command("echohl Error | echom \"Player not launched!\" | echohl None")
        if int(vim.eval('g:audiobox_debug')) == 1:
            print_exc()
    except UnknownMethodException:
        vim.command("echohl Error | echom \"Unknown method!?\" | echohl None")
        if int(vim.eval('g:audiobox_debug')) == 1:
            print_exc()
    except:
        vim.command("echohl Error | echom \"Unknown exception!\" | echohl None")
        if int(vim.eval('g:audiobox_debug')) == 1:
            print_exc()
