from REWE_split import download, delete
from mft_send import mft
decision=''

if __name__=='__main__':
    while decision != 'q':
        decision = input('''
Please select action:
    • split - to download files and split them
    • delete - to delte files from ftp
    • mft - to upload to mft
    • q - to close script
    ''')
        if decision == 'split':
            download()

        if decision == 'delete':
            delete()

        if decision == 'mft':
            mft()

