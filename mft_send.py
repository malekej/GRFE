import os
import datetime

#working_dir = r'C:\Users\mima8005\Desktop\NO IV\GRFE'
working_dir = r'\\atwieisi01\Blackdata_Input\Data\BackupFTP\\aktJahr'
passwords={'AA':('atadegaktiv','reweadeg1', 'AdegAktiv'), 'AR':('atadegrewe','reweadeg2', 'AdegRewe'),
           'S7':('atsutterluety','rewesutterluety3','Sutterluety'), 'PY':('atpenny','rewepenny4', 'Penny'),
           'B2':('atbipa','rewebipa5', 'Bipa'), 'ME':('atmerkur','rewemerkur6', 'Merkur'),
           'BI':('atbilla','rewebilla7', 'Billa')}


def mft(week, year, week_diff=0):

    if week_diff != 0:
        dayz = (week_diff + 1) * 7  # calculating how many days back
        week = datetime.datetime.now().isocalendar()[1] - 1  # returns calendar week, -1 because we are producing 1 week back
        if week == 0:  # if it was week 1 of new year it will return week from last year, timedelta says how many days back we want to go back
            week = (datetime.datetime.now() - datetime.timedelta(days=dayz)).isocalendar()[1]
            year = (datetime.datetime.now() - datetime.timedelta(days=dayz)).year
        else:
            year = datetime.datetime.now().year


    os.chdir(working_dir)
    for tag in passwords:
        exc=''
        if tag == 'AA': # handling exception
            exc = '_new'

        text_file = open('{}.mft'.format(tag), 'w')#creating file
        text_file.write(
'''open sftp://{user}:{password}@eumft.nielsen.com:22
dir *.*
copy  o:\Data\BackupFTP\\aktJahr\{fullname}\{shortcut}W{year}{week}.* /{shortcut}_{fullname}{exception}/
dir *.*
exit
'''.format(shortcut = tag, week=week, year=str(year)[-2:], user = passwords[tag][0], password = passwords[tag][1],
           fullname=passwords[tag][2], exception=exc))
        text_file.close()


    os.startfile('batch.bat')#starts the bat file

    for tag in passwords:#removes temporary files
        os.remove(tag+'.mft')



