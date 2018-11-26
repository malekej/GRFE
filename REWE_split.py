from ftplib import FTP
import os # allows me to use os.chdir
import gzip
import shutil
import datetime
from mail import mail, mail_failure, mail_missing
from mft_send import mft


# working directory where we store splited files
working_dir = r'O:\Data\BackupFTP\aktJahr'

directory_FIIFNI = '/in/Fil/' #dirrectory of FIIFNI file in FTP
directory_TOIFNI = '/in/Total/' #directory of TOIFNI file in FTP

def download(week_diff=0):
    i, j = 0, 0
    flagA, flagB = False, False

    dayz = (week_diff+1)*7#calculating how many days back

    week=datetime.datetime.now().isocalendar()[1]-1 #returns calendar week, -1 because we are producing 1 week back
    if week == 0:#if it was week 1 of new year it will return week from last year, timedelta says how many days back we want to go back
        week=(datetime.datetime.now() - datetime.timedelta(days=dayz)).isocalendar()[1]
        yy=(datetime.datetime.now() - datetime.timedelta(days=dayz)).year
    else:
        yy = datetime.datetime.now().year


    #working_dir=r"C:\Users\olwo7001\Desktop\REWE SPLIT"

    #logging to ftp
    ip = "193.186.209.35"
    password = 'k8h5f9'
    ftp = FTP(ip, 'kop050b', password)


    os.chdir(working_dir+'\REWE_originals') #changes the active dir - this is where downloaded files will be saved to

    # print ("File List:")
    # files = ftp.dir()

    ftp.cwd(directory_FIIFNI)
    filename = 'FIIFNI'+str(week)+'.ZIP'
    for file in ftp.nlst(filename):
        i+=1
    if i == 1:
        flagA = True
    fhandle = open(filename, 'wb')
    print('Getting ' + filename) #for confort sake, shows the file that's being retrieved
    ftp.retrbinary('RETR ' + filename, fhandle.write)
    fhandle.close()

    ftp.cwd(directory_TOIFNI)
    filename_t = 'TOIFNI'+str(week)+'.ZIP'
    for file in ftp.nlst(filename_t):
        j+=1
    if i == 1:
        flagB = True
    fhandle_t = open(filename_t, 'wb')
    print('Getting ' + filename_t) #for confort sake, shows the file that's being retrieved
    ftp.retrbinary('RETR ' + filename_t, fhandle_t.write)
    fhandle_t.close()
    if flagA and flagB:

        imported_file = working_dir+'\REWE_originals\\' + filename  # working ZIP file name and his directory
        new_file = imported_file[:-3]+'gz'  # working GZ file name and his directory
        working_file = imported_file[:-3]+'txt'  # working TXT file name and his directory
        os.rename(imported_file, new_file)  # Change name from ZIP to gz

        imported_file_t = working_dir+'\REWE_originals\\' + filename_t  # working ZIP file name and his directory
        new_file_t = imported_file_t[:-3]+'gz'  # working GZ file name and his directory
        working_file_t = imported_file_t[:-3]+'txt'  # working TXT file name and his directory
        os.rename(imported_file_t, new_file_t)  # Change name from ZIP to gz

        # unzipping FIL file
        with gzip.open(new_file, 'rb') as f_in:
            with open(working_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # unzipping FIL file
        with gzip.open(new_file_t, 'rb') as f_in:
            with open(working_file_t, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        biw = open(working_dir+'\Billa\BIW'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        b2w = open(working_dir+'\Bipa\B2W'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        aaw = open(working_dir+'\AdegAktiv\AAW'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        arw = open(working_dir+'\AdegRewe\ARW'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        mew = open(working_dir+'\Merkur\MEW'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        pen = open(working_dir+'\Penny\PYW'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        sut = open(working_dir+'\SutterLuety\S7W'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')
        x1 = open(working_dir+'\X1_BMLSonstige\X1W'+str(yy)[-2:]+str(week)+'.DAT', "w", encoding='ansi')

        with open(working_file, encoding='ansi') as f:
            i=0
            for r in f:
                if i == 0:
                    period = str(13 * ' ' + r[11:].strip() + 157 * ' '+'\n')
                    biw.write(period)
                    aaw.write(period)
                    arw.write(period)
                    mew.write(period)
                    pen.write(period)
                    b2w.write(period)
                    sut.write(period)
                    x1.write(period)
                if r[0:2] in ('00', '60', 'BI'):
                    biw.write(r)
                elif r[0:2] in ('03'):
                    b2w.write(r)
                elif r[0:2] in ('E3'):
                    aaw.write(r)
                elif r[0:2] in ('E2'):
                    arw.write(r)
                elif r[0:2] in ('08', 'MF', '68', 'MR', '09'):
                    mew.write(r)
                elif r[0:2] in ('78', '65'):
                    pen.write(r)
                elif r[0:2] in ('F1', 'F2', 'F4'):
                    sut.write(r)
                else:
                    if r[0:4] not in ('ANFS', 'ENDS'):
                        x1.write(r)
                i+=1

        with open(working_file_t, encoding='ansi') as t:
            for r in t:
                if r[0:2] in ('00', '60', 'BI'):
                    biw.write(r)
                elif r[0:2] in ('03'):
                    b2w.write(r)
                elif r[0:2] in ('E3'):
                    aaw.write(r)
                elif r[0:2] in ('E2'):
                    arw.write(r)
                elif r[0:2] in ('08', 'MF', '68', 'MR', '09'):
                    if not (r[0:2] == '09' and r[2:7] == '99999'):
                        mew.write(r)
                elif r[0:2] in ('78', '65'):
                    pen.write(r)
                elif r[0:2] in ('F1', 'F2', 'F4'):
                    sut.write(r)
                else:
                    if r[0:4] not in ('ANFS', 'ENDS'):
                        x1.write(r)

        biw.close()
        b2w.close()
        aaw.close()
        arw.close()
        mew.close()
        pen.close()
        sut.close()
        x1.close()

        #trying to upload to mft, if can't then will send mail
        try:
            mft(week=week, year=yy, flag = True)
            mail()
        except:
            mail_failure()
            pass
    else:
        mail_missing(flagA, flagB)

def delete(week_diff=0):
    ip = "193.186.209.35"
    password = 'k8h5f9'
    ftp = FTP(ip,'kop050b', password)#logging to ftp

    flag_1 = False
    flag_2 = False


    dayz = (week_diff+1)*7#calculating how many days back

    week=datetime.datetime.now().isocalendar()[1]-1 #returns calendar week, -1 because we are producing 1 week back
    if week == 0:#if it was week 1 of new year it will return week from last year, timedelta says how many days back we want to go back
        week=(datetime.datetime.now() - datetime.timedelta(days=dayz)).isocalendar()[1]

    filename = 'FIIFNI' + str(week) + '.ZIP'
    filename_t = 'TOIFNI' + str(week) + '.ZIP'

    # deleting FIIFNI
    try:
        ftp.cwd(directory_FIIFNI)
        ftp.delete(filename)
        flag_1 = True
    except FileNotFoundError:
        print('I didn\'t find FIIFNI file in FTP')
        pass

    # deleting TOIFNI
    try:
        ftp.cwd(directory_TOIFNI)
        ftp.delete(filename_t)
        flag_2 = True
    except FileNotFoundError:
        print('I didn\'t find TOIFNI file in FTP')
        pass

    os.chdir(working_dir+'REWE_originals')
    try:
        os.remove('FIIFNI' + str(week) + '.txt')
    except FileNotFoundError:
        print('I didn\'t find unpacked FIIFNI file in folder.')

    try:
        os.remove('TOIFNI' + str(week) + '.txt')
    except FileNotFoundError:
        print('I didn\'t find unpacked TOIFNI file in folder.')

    if flag_1 and flag_2:
        print('Both files are deleted from FTP')
    elif flag_1 and not flag_2:
        print('I deleted FIIFNI file but couldn\'t find TOIFNI file.')
    elif not flag_1 and flag_2:
        print('I deleted TOIFNI file but couldn\'t find FIIFNI file.')
    else:
        print('I couldn\'t find any of these files.')

