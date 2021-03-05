from console import *
from mgr.files import *
import os

class Session:
    def __init__(self):
        self.cfile = CFile()

    def start(self):
        cmds = {
                "encrypt":"Encrypt a file",
                "decrypt":"Decrypt a file",
                "load":"Load a CFile",
                "close":"Close the cfile",
                "list":"Lists all keys",
                "delete":"Deletes a key",
                "exit":"Leave ether"
        }
        cmd = console.getCmd(cmds)
        if cmd == "encrypt":
            self.encrypt()
        elif cmd == "decrypt":
            self.decrypt()
        elif cmd == "close":
            self.cfile.close()
            self.start()

        elif cmd == "list":
            self.cfile.list()
            self.start()

        elif cmd == "delete":
            self.cfilem()
        
        elif cmd == "exit":
            if self.cfile.loggedin:
                self.cfile.write()
            exit()
        elif cmd == "load":
            if self.cfile.loggedin:
                console.warn("Please close the cfile before loading another one!")
                self.start()

            self.load()
            self.start()

    def encrypt(self):
        if self.cfile.loggedin == False:
            cmd = console.ask("Use existing cfile?")
            if cmd == "y":
                self.cfile.path = console.getInp("Please enter the path to your cfile!")
                self.cfile.getpassw()
                self.cfile.read()
            else:
                self.cfile.new()

        console.setprompt(os.path.basename(self.cfile.path))
        print()
        console.status("Enter the files/directories you want to encrypt... (X to leave)")
        while True:
            cmd = input(TermColor().bold().toStr(os.path.basename(self.cfile.path) + "/encrypt> "))
            if cmd == "X":
                break

            if os.path.isfile(cmd):
                self.cfile.encrypt(cmd)

            if os.path.isdir:
                for root, dirs, files in os.walk(cmd):
                    for file in files:
                        self.cfile.encrypt(os.path.join(root,file))
        self.start()

    def cfilem(self): #delete mode
        self.load()
        print()
        console.status("Enter the key-number to delete... (X to leave, list= lists all keys, * = destroys all keys)")
        while True:
            cmd = input(TermColor().bold().toStr(os.path.basename(self.cfile.path) + "/delete> "))
            if cmd == "X":
                break
            elif cmd == "list":
                print()
                self.cfile.list()
                self.cfilem()
            elif cmd == "*":
                ans = console.ask("Do you really destroy all keys?")
                if ans == "y":
                    self.cfile.data = dict()
                    console.info("Successfully destroyed all keys...")
                    self.start()
                else:
                    self.cfilem()

            try:
                cmd = int(cmd)
            except Exception as e:
                console.hwarn("Invalid input!")
                cmd = None
            if cmd is not None:
                ans = console.ask("Do you really destroy key " + str(cmd) + "?")
                if ans == "y":
                    self.cfile.delete(cmd)
        self.start()

    def decrypt(self):
        print("Dec")
        self.load()
        print()
        console.status("Enter the files/directories you want to decrypt... (X to leave)")
        while True:
            cmd = input(TermColor().bold().toStr(os.path.basename(self.cfile.path) + "/decrypt> "))
            if cmd == "X":
                break

            if os.path.isfile(cmd):
                self.cfile.restore(cmd)

            if os.path.isdir:
                for root, dirs, files in os.walk(cmd):
                    for file in files:
                        if os.path.isfile(os.path.join(root,file)):
                            self.cfile.restore(os.path.join(root,file))
        self.start()

    def load(self):
        if self.cfile.loggedin == False:
            self.cfile.path = console.getInp("Please enter the path to your cfile!")
            self.cfile.getpassw()
            self.cfile.read()
        else:
            return

        console.setprompt(os.path.basename(self.cfile.path))

