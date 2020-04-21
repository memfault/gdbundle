import lldb
from gdbundle import LOADED_PLUGINS


def gdbundle_list(debugger, command, result, internal_dict):
    for plugin in LOADED_PLUGINS:
            print(plugin.replace("gdbundle_", ""))

lldb.debugger.HandleCommand('command script add -f gdbundle.commands_lldb.gdbundle_list gdbundle_list')
