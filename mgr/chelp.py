def phelp(cmds):
    """
    cmds(dict)
    """
    print("OPTIONS:")
    for cmd in cmds:
        print(cmd + "\t\t" + cmds[cmd])
