"""
CRC-Implementation in Python 3.x
In diesem Skript wird die Erzeugung des CRC für eine Nachricht implementiert.

21.03.2020 - Felix Widmaier
"""

# Eine Methode, um int in einen str zu konvertieren.
# Diese Methode wandelt eine Dezimalzahl in eine Binärzahl.
dectobin = lambda data: str(bin(data))[2::]

def pd2bin(data, l):
    """
    Diese Methode passt das Ergebnis der dectobin-Methode an.
    Somit soll eine schöne Ausgabe auf der Konsole gewährleistet werden.
    Diese Methode verlängert das Ergebnis der dectobin-Methode um l Nullen.
    Die Nullen werden vor die Zahl geschrieben. Damit wird der numerische
    Wert der Zahl nicht verändert.

    data (int): Die Zahl, welche konvertiert werden soll
    l (int): Die gewünschte Länge der Outputs
    """
    data = dectobin(data)
    if len(data) < l:
        while len(data) != l: # Die Nullen werden solange angehängt,
            data = "0" + data # bis der Output hinreichend groß ist
    return data

def concat(data, symb):
    """
    Konkateniert eine Zahl mit einer anderen (einstelligen) Zahl.
    Das Konkatenieren wird in der Basis 2 durchgeführt.

    data(str/int): 1. Zahl
    symb(str/int): 2. (einstellige) Zahl
    """
    if type(data) == str:
        data = int(data,2)
    data *= 2 # shift um eine Stelle nach links zur Basis 2
    data += int(symb) # addieren der einstelligen Zahl
    return data

def operate(wcrc, pol, i=0):
    """
    Verrechnet (temporären) CRC mit dem Generatorpolynom mittels XOR. Falls die größte Stelle
    des (temporären) CRC "0" ist, so wird mit "0" statt dem Generatorpolynom gearbeitet.
    
    wcrc(int): temporärer CRC
    pol(str): Generatorpolynom
    """
    if len(dectobin(wcrc)) < len(pol):
        wcrc ^= 0
        #print(" "*i + "0"*len(pol))
    else:
        wcrc ^= int(pol,2)
        #print(" "*i + pol)
    #print(" "*i + "-"*len(pol))
    return wcrc

def gen_crc(data, pol):
    """
    Methode zur Erstellung des CRC.

    data(str): Die Nachricht / Nutzdaten
    pol(str): Das Generatorpolynom
    """
    #print("Calculating CRC-Checksum...")
    for i in pol[1::]: # Zunächst werden die Nullen an die Nachricht angehängt
        data += "0"
    wcrc = int(data[:len(pol):], 2) # data wird zu einem int gecastet
    #print(data)
    #print(pol)
    wcrc = operate(wcrc, pol)
    i = 1 # Zähler für den Output
    for symbol in data[len(pol)::]:
        # Wir iterieren nun durch alle verbleibenden Stellen in der Nachricht
        wcrc = concat(wcrc,symbol) # die Stelle wird angehängt
        #print(" "*i + pd2bin(wcrc,len(pol)))
        wcrc = operate(wcrc, pol, i)
        i += 1

    #print(" "*(i) + pd2bin(wcrc, len(pol)-1)) # Ausgabe des CRC.
    return wcrc


def cfe(data, pol): # Check For Errors
    """
    Eine Methode zur Erkennung von Übertragungsfehlern
    """
    wcrc = int(data[:len(pol):], 2) # data wird zu einem int gecastet
    #print(data)
    #print(pol)
    wcrc = operate(wcrc, pol)
    i = 1 # Zähler für den Output
    for symbol in data[len(pol)::]:
        # Wir iterieren nun durch alle verbleibenden Stellen in der Nachricht
        wcrc = concat(wcrc,symbol) # die Stelle wird angehängt
        #print(" "*i + pd2bin(wcrc,len(pol)))
        wcrc = operate(wcrc, pol, i)
        i += 1

    #print(" "*(i) + pd2bin(wcrc, len(pol)-1)) # Ausgabe des CRC.

    if wcrc == 0:
        #print("Es wurden keine Fehler bei der Übertragung gemacht.")
        return True
    else:
        #print("Es wurden Fehler bei der Übertragung erkannt!")
        return False

