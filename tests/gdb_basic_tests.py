import gdbundle

gdbundle.init()

debugger = gdbundle.get_debugger()

if debugger == 'gdb':
    gdb.execute("gdbundle")
    gdb.execute("gdbundle list")

