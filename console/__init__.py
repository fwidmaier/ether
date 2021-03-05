#from mgr.files import CFile
from mgr import chelp

class Console:
    def __init__(self):
        self.prompt = TermColor().bold().toStr("["+TermColor().cyan().toStr("ether")+"]$ ")

    def setprompt(self,text):
        self.prompt = TermColor().bold().toStr("["+TermColor().cyan().toStr("ether/" + text)+"]$ ")

    def getInp(self,question):
        print(question)
        while True:
            path = input(TermColor().bold().toStr("> "))
            if len(path) >= 2:
                return path
            else:
                print("Invalid input!")

    def getCmd(self,cmds):
        #chelp.phelp(cmds)
        #print("?\t\tDisplays this help")
        while True:
            cmd = input(self.prompt).lower().strip()
            if cmd in cmds:
                return cmd
            elif cmd == "?":
                chelp.phelp(cmds)
            else:
                print("Invalid input!")

    def ask(self, question):
        #print(question + TermColor().bold().toStr(" [y/n]"))
        while True:
            cmd = input(question + TermColor().bold().toStr(" [y/n] ")).lower().strip()
            if cmd == "y" or cmd == "yes":
                return "y"
            elif cmd == "n" or cmd == "no":
                return "n"
            else:
                print("Invalid input!")

    def warn(self, text):
        TermColor().red().bold().echo(text)

    def info(self, text,bold=False):
        if bold:
            TermColor().green().bold().echo(text)
            return
        TermColor().green().echo(text)

    def hwarn(self, text):
        TermColor().yellow().echo(text)

    def status(self, text,stat=""):
        print(TermColor().bold().toStr("["+stat+"] ") + text)


class TermColor:
    def __init__(self, seq=[]):
        self.seq = seq

    def toStr(self, data):
        codes = ";".join(self.seq)
        return "\x1b[{}m{}\x1b[0m".format(codes, data)

    def echo(self,text):
        print(self.toStr(text))

    def red(self):
        return TermColor(self.seq + ["31"])

    def yellow(self):
        return TermColor(self.seq + ["33"])

    def green(self):
        return TermColor(self.seq + ["32"])

    def bold(self):
        return TermColor(self.seq + ["1"])

    def cyan(self):
        return TermColor(self.seq + ["36"])

console = Console()
