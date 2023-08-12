import os
from cryptography.fernet import Fernet
from tkinter import filedialog


def print_logo():
    clear()
    print(r"""

     ______   __  __   ______   ________   ______   ______
    /_____/\ /_/\/_/\ /_____/\ /_______/\ /_____/\ /_____/\
    \:::_ \ \\ \ \ \ \\::::_\/_\::: _  \ \\::::_\/_\::::_\/_
     \:(_) \ \\:\_\ \ \\:\/___/\\::(_)  \ \\:\/___/\\:\/___/\
      \: ___\/ \::::_\/ \_::._\:\\:: __  \ \\:::._\/ \::___\/_
       \ \ \     \::\ \   /____\:\\:.\ \  \ \\:\ \    \:\____/\
        \_\/      \__\/   \_____\/ \__\/\__\/ \_\/     \_____\/
    
    
                                                            creator : brielosos
        """)


def generate_key():
    key = Fernet.generate_key()

    with open('filekey.key', 'wb') as filekey:
        filekey.truncate()
        filekey.write(key)


def read_key():
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    return key


def load_key(key):
    fernet = Fernet(key)
    return fernet


def key_exist():
    try:
        f = open('filekey.key', 'r')
        f.close()
        return True
    except FileNotFoundError:
        return False


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File to Encrypt (you should always use an Usb device to store the encrypted file)",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))

    return filename


def print_warnings():
    print(
        'WARNING ... if you delete the key file you will not be able to recover the encrypted data'
        '(for safety reasons i suggest to keep the encrypted data in an Usb device, to avoid having data and key in the same device)')


def encrypt(filename, key):
    key = load_key(key)
    with open(filename, 'rb') as file:
        original = file.read()

    encrypted = key.encrypt(original)

    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt(filename, key):
    key = load_key(key)
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = key.decrypt(encrypted)

    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)


def encryption_request():
    clear()
    print_warnings()
    input('press Enter for the file selection')
    filename = browseFiles()

    if not key_exist():
        choice = input('It appears you havent created a key yet, do you want to create one now?(Y/N)\n>>>').lower()
        if choice == 'y':
            generate_key()
        else:
            menu()

    encrypt(filename, read_key())
    input('Encryption complete ... Press Enter to return the the menu')
    menu()


def decryption_request():
    clear()
    print_warnings()

    if not key_exist():
        print('Error ... there is no key to load. '
              'Be sure that the key file is in the same folder of the script')
        input('Press Enter to return to the menu')
        menu()

    input('press Enter for the file selection')
    filename = browseFiles()
    decrypt(filename, read_key())
    input('Decryption complete ... Press Enter to return the the menu')
    menu()


def new_key_request():
    clear()
    print(
        'WARNING ... if you have files encrypted with a key, you have to make a backup of it before creating a new one.'
        '\nCREATING A NEW KEY WILL DELETE THE EXISTING ONE')
    confirmation = input('Type CONFIRM to create the new key\n>>>').lower()
    if confirmation == 'confirm':
        generate_key()
        input('\nNew key generated ... press Enter to return to the menu')
        menu()
    else:
        input('Operation aborted ... press Enter to return to the menu')
        menu()


def clear():
    os.system('cls')


def print_commands():
    print('''\n1) Encrypt a file\n2) Decrypt a file\n3) Generate new key''')


def menu():
    print_logo()
    print('\nWelcome to pySafe menu, please select your command')
    while True:
        try:
            print_commands()
            selection = input('>>> ')
            if selection.lower() == 'exit':
                quit()
            selection = int(selection)
            if selection == 1:
                encryption_request()
            elif selection == 2:
                decryption_request()
            elif selection == 3:
                new_key_request()
            else:
                raise ValueError
            break

        except ValueError:
            print('Request not possible ... try again')
            continue


menu()