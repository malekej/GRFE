from REWE_split import download, delete
from mft_send import mft

decision = ''

if __name__=='__main__':
    while decision != 'q':

        flag = False

        decision = input('''
Please select action:
    • split - to download files and split them
    • delete - to delte files from ftp
    • mft - to upload to mft
    • help - for some tips
    • q - to close script\n''')

        try:#checks if you want overwrite automate settings
            decision_lst = decision.split(' ')
            if len(decision_lst) == 2:
                decision, week_diff = decision_lst[0], int(decision_lst[1])
                flag = True
        except:
            pass

        if decision == 'split' and flag:
            download(week_diff=week_diff)
        elif decision == 'split' and not flag:
            download()

        if decision == 'delete' and flag:
            delete(week_diff=week_diff)
        elif decision == 'delete' and not flag:
            delete()

        if decision == 'mft' and flag:
            mft(week_diff=week_diff)
        elif decision == 'mft' and not flag:
            mft()

        if decision == 'help':
            print('''To overwrite base settings insert how many weeks back you want to download file from.
            For example, if you want to download file from two weeks ago, insert after space '2': download 2.''')


