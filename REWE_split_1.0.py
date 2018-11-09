from ftplib import FTP
import os # allows me to use os.chdir
import gzip
import shutil
import datetime

port=21
ip="193.186.209.35"
password='k8h5f9'
week=datetime.datetime.now().isocalendar()[1]-1 #returns calendar week, -1 because we are producing
yy=datetime.datetime.now().year

# working directory where we store splited files
working_dir=r"C:\Users\olwo7001\Desktop\REWE SPLIT"
os.chdir(working_dir) #changes the active dir - this is where downloaded files will be saved to
ftp = FTP(ip)
ftp.login('kop050b',password)
# print ("File List:")
# files = ftp.dir()

directory ="/in/Fil/" #dir i want to download files from, can be changed or left for user input

ftp.cwd(directory)
filename = 'FIIFNI'+str(week)+'.ZIP'
fhandle = open(filename, 'wb')
print('Getting ' + filename) #for confort sake, shows the file that's being retrieved
ftp.retrbinary('RETR ' + filename, fhandle.write)
fhandle.close()

directory ="/in/Total/" #dir i want to download files from, can be changed or left for user input

ftp.cwd(directory)
filename_t = 'TOIFNI'+str(week)+'.ZIP'
fhandle_t = open(filename_t, 'wb')
print('Getting ' + filename_t) #for confort sake, shows the file that's being retrieved
ftp.retrbinary('RETR ' + filename_t, fhandle_t.write)
fhandle_t.close()

imported_file = working_dir+r'\\' + filename  # working ZIP file name and his directory
new_file = imported_file[:-3]+'gz'  # working GZ file name and his directory
working_file = imported_file[:-3]+'txt'  # working TXT file name and his directory
os.rename(imported_file, new_file)  # Change name from ZIP to gz

imported_file_t = working_dir+r'\\' + filename_t  # working ZIP file name and his directory
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

biw = open(working_dir+r'\\' + 'BIW'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
b2w = open(working_dir+r'\\' + 'B2W'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
aaw = open(working_dir+r'\\' + 'AAW'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
arw = open(working_dir+r'\\' + 'ARW'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
mew = open(working_dir+r'\\' + 'MEW'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
pen = open(working_dir+r'\\' + 'PYW'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
sut = open(working_dir+r'\\' + 'S7W'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')
x1 = open(working_dir+r'\\' + 'X1W'+str(yy)+str(week)+'.DAT', "w", encoding='ansi')

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
