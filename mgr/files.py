from getpass import getpass
import os.path
import pickle
import hashlib
import random

from console import *
from engine.crcmod import *
from engine.crypt import *
from engine.helpers import *
import time

def sha256sum(filename): # Prüfsumme einer Datei
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

class CFile:
    def __init__(self, path=""):
        self.ipoly = "10011010" # check for inner stuff / contents checking
        self.ppoly = "10111011" # password polynome
        self.path = path
        self.passw = None
        self.data = dict()
        self.loggedin = False

    def setpassw(self): # fragt ein (neues) Passwort über die Konsole ab
        while True:
            p1 = getpass("Password: ")
            if len(p1) < 5:
                print("Use at least 5 characters!")
                continue
            p2 = getpass("Password (repeat): ")
            if p1 == p2:
                self.passw = p1
                console.info("The password has been successfully set!")
                return
            else:
                console.hwarn("The inputs do not match! Please try again!\n")

    def getpassw(self): # fragt ein Passwort über die Konsole ab
        print()
        self.passw = getpass("Password: ")
        print()

    def new(self): # dialog, um eine neue Schlüsseldatei anzulegen
       path = console.getInp("Please enter the name of your new cfile.")
       self.path = path
       print("Enter a new password for your cfile.\n")
       self.setpassw()
       console.status("File will be created...", "CFile")
       try:
           if os.path.isfile(path):
               ans = console.ask("The file already exists, override?")
               if ans == "n":
                   print("Abort.")
                   return
           self.write(self.data)
           self.loggedin = True
       except Exception as e:
            raise Exception("The file could not be created!")

    def get_entry(self, path): # gibt den Schlüsseleintrag einer Datei an
        fingerprint = sha256sum(path)
        dentry = None
        for entry in self.data:
            if self.data[entry]["hash"] == str(fingerprint):
                dentry = entry

        return dentry

    def restore(self, path): # restore a file from data stored in cfile
        if os.path.isfile(path) == False:
            console.hwarn("This is to the file you are looking for! (File was not found) ")
            return

        if not os.access(path, os.R_OK):
            console.warn("Permission denied! Could not decrypt " + path)
            return

        dentry = self.get_entry(path)
        
        if dentry is None:
            console.hwarn("There seems to be no information stored in this cfile about " + path)
            return

        file = File(path)
        npath = file.decrypt(self.data[dentry]["key"], newfname=self.data[dentry]["filename"])
        if sha256sum(npath) == self.data[dentry]["fingerprint"]:
            console.info("Sucessfully restored file!")
        else:
            console.warn("The file seems to be corrupt!")
            ans = console.ask("Delete the decrypted file?")
            if ans == "y":
                try:
                    os.remove(npath)
                except Exception as e:
                    console.hwarn("Failed to remove " + npath)

    def encrypt(self, path): # verschlüsselt eine Datei und legt (falls nicht vorhanden) einen neuen Schlüssel an
        if os.path.isfile(path) == False:
            console.hwarn("This is to the file you are looking for! (File was not found)")
            return

        if not os.access(path, os.R_OK):
            console.warn("Permission denied! Could not encrypt " + path)
            return
        
        fingerprint = sha256sum(path)
        dentry = None
        for entry in self.data:
            if self.data[entry]["fingerprint"] == str(fingerprint):
                dentry = entry
        if dentry is None:
            console.status("Creating new entry for " + os.path.basename(path) + "...", "CFile")
            self.newentry(path)
            return

        file = File(path)
        file.encrypt(self.data[dentry]["key"])
        

    def write(self, data=None): # schreibt die Daten in die Schlüsseldatei
        if data is None:
            data = self.data

        dd = lambda data: str(bin(int(data.hex(),16)))[2::]
        try:
            cfile = open(self.path, "wb")
            dbytes = pickle.dumps(data)
            console.status("Generating CRC for contents...","CRC")
            #print(dbytes)
            wcrc = gen_crc(dd(dbytes),self.ipoly)
            #print("CRC", wcrc)
            #print(dd(dbytes) + pd2bin(wcrc,len(self.ipoly)-1))
            cc = bytearray(dbytes)
            cc.append(wcrc)
            console.status("Establishing password security...","Password")
            pcrc = gen_crc(dd(bytes(self.passw, "utf-8")),self.ppoly)
            #print("PassCRC", pcrc)
            #print(dectobin(pcrc))
            cc.append(pcrc)
            dbytes = bytes(cc)
            #print(dbytes)
            console.status("Encryption of contents...")
            dbytes = CFileCrypt().encrypt(dbytes,self.passw)
            cfile.write(dbytes)
            cfile.close()
            console.info("Contents have been sucessfully writen to " + self.path)
        except Exception as e:
            print(e)

    def newentry(self, path): # legt einen neuen Schlüssel für eine Datei an
        if not os.path.isfile(path):
            console.warn("This is not the file you are looking for! (" + path + ") - not found.")
            return

        if self.get_entry(path) is not None:
            return

        dtemp = {
                "filename":os.path.basename(path),
                "fingerprint":sha256sum(path),
                "key":gen_pass(150),
                "hash":None # hash of encrypted file
        }

        file = File(path)
        _hash = file.encrypt(dtemp["key"])
        if _hash is None:
            return

        dtemp["hash"] = _hash
        self.data[os.path.basename(path) + str(time.time())] = dtemp

    def read(self, path=""): # ließt die Daten einer Schlüsseldatei ein
        if path == str():
            path = self.path

        if not os.path.isfile(path):
            console.hwarn("This is not the file you are looking for! (File was not found)")
            exit()
        
        dd = lambda data: str(bin(int(data.hex(),16)))[2::]
        try:
            cfile = open(path, "rb")
            dat = cfile.read()
            dat = bytearray(CFileCrypt().decrypt(dat, self.passw))
            #rpcrc = gen_crc(dd(bytes(self.passw, "utf-8")),self.ppoly)
            #print(dat)
            pcrc = dat[-1]
            del dat[-1]
            #print(pcrc)
            wcrc = dat[-1]
            del dat[-1]
            #print("CRC",wcrc)
            #check password
            #print(dectobin(pcrc))
            pstatus = cfe(dd(bytes(self.passw, "utf-8")) + pd2bin(pcrc, len(self.ppoly)-1),self.ppoly)
            if pstatus == False:
                console.warn("Permission denied!")
                exit()
            else:
                console.info("Permission granted...",True)
            #print(pcrc)
            # check file corrupt
            dat = bytes(dat)
            #print(dd(dat) + pd2bin(wcrc,len(self.ipoly)-1))
            fstatus = cfe(dd(dat) + pd2bin(wcrc,len(self.ipoly)-1),self.ipoly)
            if fstatus == False:
                console.warn("Corrupt file!")
                exit()
            console.status("Successfully read...","File")
            self.data = pickle.loads(dat)
            self.loggedin = True
        except Exception as e:
            print(e)

    def list(self): # listet alle Schlüssel auf der konsole
        if self.data == dict():
            console.hwarn("There are no keys to list!")

        i = 1
        for entry in self.data:
            dstr = entry + "\n"
            dstr += self.data[entry]["filename"] + ", "
            dstr += self.data[entry]["fingerprint"] + ", "
            dstr += self.data[entry]["key"]
            print(TermColor().bold().toStr("["+str(i)+"] ") + dstr)
            i += 1

    def delete(self, num): # löscht den Schlüssel mit der Nummer num
        if num > len(self.data):
            console.warn("Invalid number!")
            return
        i = 1
        dentry = None
        for entry in self.data:
            if i == num:
                dentry = entry
                break
            i += 1
        try:
            del self.data[dentry]
            console.info("Destroyed key " + dentry + "...")
        except Exception as e:
            console.hwarn("Could not delete key " + str(num) + "...")

    def close(self): # schließt die Datei und schreibt die Inhalte
        if self.loggedin == False:
            console.status("No cfile is currently opened!", "File")
            return False
        ans = console.ask("Are you sure you want to close the cfile?")
        if ans == "n":
            return False
        self.write()
        self.passw = str()
        self.loggedin = False
        self.data = dict()
        console.prompt = (TermColor().bold().toStr("["+TermColor().cyan().toStr("ether")+"]$ "))
        return True

class File:
    def __init__(self, path):
        self.path = path
        self.ending = ".ether"

    def encrypt(self, key, newfname="", delete=True): # newfname = new file name; delete = delete origigal?
        if os.path.isfile(self.path) == False:
            console.hwarn("The file " + self.path + " does not seem to exist!")
            return

        try:
            file = open(self.path, "rb")
            ocont = file.read() # original content
            file.close()
            ccont = CFileCrypt().encrypt(ocont, key)
            if newfname == str():
                fname = os.path.basename(self.path) + self.ending # filename of encrypted file
            else:
                fname = newfname + self.ending
            cryf = open(os.path.join(os.path.dirname(self.path), fname), "wb")
            cryf.write(ccont)
            cryf.close()
            console.status("Sucessfully encrypted...",os.path.basename(self.path))
            if delete:
                try:
                    console.status("Deleting file " + self.path)
                    os.remove(self.path)
                except Exception as e:
                    console.hwarn("Could not delete file " + self.path)
            return sha256sum(os.path.join(os.path.dirname(self.path),fname))
        except Exception as e:
            console.hwarn("Failed to encrypt " + self.path)

    def decrypt(self, key, newfname="", delete=True, overwrite=False):
        fname = os.path.basename(self.path)
        if fname.endswith(self.ending):
            fname = fname[:-len(self.ending)]
        else:
            fname += ".decrypt"

        try:
            if os.path.isfile(os.path.join(os.path.dirname(self.path), fname)) and overwrite == False:
                ans = console.ask("The file " + os.path.join(os.path.dirname(self.path), fname) + " already exists, overwrite?")
                if ans == "n":
                    fname += ".decrypt"
            file = open(self.path, "rb")
            cont = file.read()
            file.close()
            dec = CFileCrypt().decrypt(cont,key)
            #print(dec)
            ofile = open(os.path.join(os.path.dirname(self.path), fname), "wb")
            ofile.write(dec)
            ofile.close()
            console.status("Successfully decrypted...",fname)
            if delete:
                try:
                    os.remove(self.path)
                except Exception as e:
                    console.hwarn("Could not delete " + self.path)
            return os.path.join(os.path.dirname(self.path), fname)
        except Exception as e:
            console.hwarn("File " + self.path + " could not be restored...")
