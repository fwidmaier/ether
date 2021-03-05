# ether
This is just a proof-of-concept thing to generate and store a password-crc.

## Sample usage...
### ... for encryption
For example, we want to encrypt the file test.txt. To do this, we create a new key file with the name test.key and set a new password. Then the file test.txt is encrypted and the contents of the key file are written into the key file.
```console
python3 ether.py
     ,*-~"`^"*u_                                _u*"^`"~-*,
  p!^       /  jPw                            w9j \        ^!p
w^.._      /      "\_                      _/"     \        _.^w
     *_   /          \_      _    _      _/         \     _* 
       q /           / \q   ( `--` )   p/ \          \   p
       jj5****._    /    ^\_) o  o (_/^    \    _.****6jj
                *_ /      "==) ;; (=="      \ _*
                 `/.w***,   /(    )\   ,***w."
                  ^ ilmk ^c/ )    ( \c^      ^
                          'V')_)(_('V'
[ether]$  enctypt
Use existing cfile? [y/n] n
Please enter the name of your new cfile.
> test.key
Enter a new password for your cfile.

Password: 
Password (repeat): 
The password has been successfully set!
[CFile] File will be created...
[CRC] Generating CRC for contents...
[Password] Establishing password security...
[] Encryption of contents...
Contents have been sucessfully writen to test.key

[] Enter the files/directories you want to encrypt... (X to leave)
test.key/encrypt> test.txt
[CFile] Creating new entry for test.txt...
[test.txt] Sucessfully encrypted...
[] Deleting file test.txt
test.key/encrypt> X
[ether/test.key]$ exit
[CRC] Generating CRC for contents...
[Password] Establishing password security...
[] Encryption of contents...
Contents have been sucessfully writen to test.key
```
### ... for decryption
Now we want to decrypt the just encrypted file test.txt. We do this by specifying the key file and entering the correct password. The file test.txt.ether can then be decrypted!
```console
python3 ether.py
     ,*-~"`^"*u_                                _u*"^`"~-*,
  p!^       /  jPw                            w9j \        ^!p
w^.._      /      "\_                      _/"     \        _.^w
     *_   /          \_      _    _      _/         \     _* 
       q /           / \q   ( `--` )   p/ \          \   p
       jj5****._    /    ^\_) o  o (_/^    \    _.****6jj
                *_ /      "==) ;; (=="      \ _*
                 `/.w***,   /(    )\   ,***w."
                  ^ ilmk ^c/ )    ( \c^      ^
                          'V')_)(_('V'
[ether]$ decrypt
Dec
Please enter the path to your cfile!
> test.key

Password: 

Permission granted...
[File] Successfully read...

[] Enter the files/directories you want to decrypt... (X to leave)
test.key/decrypt> test.txt.ether
[test.txt] Successfully decrypted...
Sucessfully restored file!
test.key/decrypt> X
[ether/test.key]$ exit
[CRC] Generating CRC for contents...
[Password] Establishing password security...
[] Encryption of contents...
Contents have been sucessfully writen to test.key
```

For further documentation, check out [doc/doc.pdf](https://github.com/fwidmaier/ether/blob/main/doc/doc.pdf) (however, this file is written in German).
