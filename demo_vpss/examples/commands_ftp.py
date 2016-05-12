SERVER = "localhost"
CLOUD_USERNAME = "cloud"
CLOUD_PASSWORD = "cloud"

from ftplib import FTP

# login
ftp = FTP(SERVER)
ftp.login(user=CLOUD_USERNAME, passwd = CLOUD_PASSWORD)

# change folder
#ftp.cwd("/whyfix/")


# download
fileout = "provapython.txt"
filein = "prova.txt"
localfile = open(fileout, "wb")
ftp.retrbinary("RETR " + filein, localfile.write, 1024)
localfile.close()

# get list of files
files = []
try:
    files = ftp.nlst()
except ftplib.error_perm, resp:
    if str(resp) == "550 No files found":
        print "No files in this directory"
    else:
        raise

for f in files:
    print f


# upload
filein = "ISTRUZIONI.txt"
fileout = "example.txt"
ftp.storbinary("STOR " + fileout, open(filein, "rb"))
# upload to "/home/cloud"

# close connection
ftp.quit() 

