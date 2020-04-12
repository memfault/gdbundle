import gdb
from gdbundle import LOADED_PLUGINS

class GDBundleCommand(gdb.Command):
    GDB_CMD = "gdbundle override_me"

    def __init__(self, *args, **kwargs):
        super(GDBundleCommand, self).__init__(self.GDB_CMD, gdb.COMMAND_USER, *args, **kwargs)


class GDBundle(GDBundleCommand):
    """GDBundle commands"""

    GDB_CMD = "gdbundle"

    def __init__(self):
        super(GDBundle, self).__init__(gdb.COMPLETE_NONE, prefix=True)

    def invoke(self, arg, from_tty):
        gdb.execute("help gdbundle")


class GDBundleListPlugins(GDBundleCommand):
    """List GDBundle packages"""
    
    GDB_CMD = "gdbundle list"

    def invoke(self, _unicode_args, _from_tty):
        for plugin in LOADED_PLUGINS:
            print(plugin.replace("gdbundle_", ""))


GDBundle()
GDBundleListPlugins()
