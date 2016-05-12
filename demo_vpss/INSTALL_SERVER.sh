#!/bin/bash

#sudo apt-get update

##############################################################################

# INSTALL PYTHON
sudo apt-get install --yes python
sudo apt-get install --yes python-mysqldb

##############################################################################

# INSTALL MYSQL SERVER
# --------------------
# - install 
#   LAMP 
#   or only
#   MySql 
#     (see http://zetcode.com/db/mysqlpython/ )

sudo apt-get install --yes mysql-server

# CONFIGURE MYSQL SERVER
# ----------------------
# - ensure the file
#   /etc/mysql/mysql.conf.d/mysqld.cnf
#   contains the following lines (the last is commented):
#
# [mysqld]
# user            = mysql
# pid-file        = /var/run/mysqld/mysqld.pid
# socket          = /var/run/mysqld/mysqld.sock
# port            = 3306
# basedir         = /usr
# datadir         = /var/lib/mysql
# tmpdir          = /tmp
# language        = /usr/share/mysql/English
# bind-address    = <HOST_IP_ADDRESS>
# # skip-networking
IP="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
sudo sed -i "s/bind-address/bind-address = "$IP"\n#/g" /etc/mysql/my.cnf

# - restart mysql with
# /etc/init.d/mysql restart
sudo service mysql restart
#################################################
# Grant access to remote IP address
# mysql -u root -p mysql
#   CREATE USER 'searchuser'@'localhost' IDENTIFIED BY 'search123';
#   CREATE USER 'searchuser'@'%' IDENTIFIED BY 'search123';
#   GRANT ALL ON *.* TO 'searchuser'@'localhost';
#   GRANT ALL ON *.* TO 'searchuser'@'%';
#################################################

##############################################################################

# INSTALL FTP SERVER
# ------------------
# check for example
# http://www.cviorel.com/2009/03/05/how-to-setup-vsftpd-ftp-on-ubuntu-linux/
#
sudo apt-get install --yes vsftpd

# CONFIGURE FTP SERVER
# --------------------

#  - modify file /etc/vsftpd.conf by setting:
#       * local_enable=YES
#       * write_enable=YES
#     and adding the three lines
#         userlist_enable=YES
#         userlist_deny=NO
#         userlist_file=/etc/vsftpd.user_list

sudo sed -i "s/local_enable=NO/local_enable=YES/g" /etc/vsftpd.conf
sudo sed -i "s/#write_enable/write_enable/g" /etc/vsftpd.conf
sudo sed -i "s/write_enable=NO/write_enable=YES/g" /etc/vsftpd.conf

sudo sed -i "/userlist_enable=YES/d" /etc/vsftpd.conf
sudo sed -i "/userlist_deny=NO/d" /etc/vsftpd.conf
sudo sed -i "/userlist_file=\/etc\/vsftpd.user_list/d" /etc/vsftpd.conf

echo "userlist_enable=YES" | sudo tee -a /etc/vsftpd.conf
echo "userlist_deny=NO" | sudo tee -a /etc/vsftpd.conf
echo "userlist_file=/etc/vsftpd.user_list" | sudo tee -a /etc/vsftpd.conf

#  - create the new file
#      /etc/vsftpd.user_list
#    and add the line (add the user "cloud" to the file)
#      cloud
if [ -f /etc/vsftpd.user_list ]; then
    sudo sed -i "/cloud/d" /etc/vsftpd.user_list
fi
echo "cloud" | sudo tee -a /etc/vsftpd.user_list

#  - edit /etc/shells and add the entry
#        /bin/false
#    sudo echo "/bin/false" > /etc/shells
sudo sed -i "\/bin\/false/d" /etc/shells
echo "/bin/false" | sudo tee -a /etc/shells

#  - add new user named "Cloud"
FTP_CLOUD_FOLDER="/home/cloud"
#FTP_CLOUD_FOLDER="C:\cloud"

sudo mkdir -p ${FTP_CLOUD_FOLDER}
sudo useradd cloud -d ${FTP_CLOUD_FOLDER} -s /bin/false
sudo passwd "cloud"
sudo chown -R cloud:users ${FTP_CLOUD_FOLDER}

#  - in case the previous commands do not work, try also these commands:
#        FTP_CLOUD_FOLDER="/home/cloud"
#        sudo mkdir ${FTP_CLOUD_FOLDER}
#        sudo useradd -d ${FTP_CLOUD_FOLDER} -g users -s /bin/false cloud
#        sudo passwd cloud
#        sudo chown -R cloud.users ${FTP_CLOUD_FOLDER}
#        sudo touch /etc/vsftpd.user_list 
#        sudo echo "cloud" > /etc/vsftpd.user_list

#  - restart the deamon with one of the following 
#    (only one should suffice if no errors occur)
#        sudo service vsftpd restart
#        sudo /etc/init.d/vsftpd restart
#        sudo /usr/sbin/vsftpd restart
#        sudo /etc/init.d/vsftpd start

sudo service vsftpd restart

##############################################################################

# SETUP PYTHON DEFINITIONS FILE
#sudo sed -i "s/DB_SERVER = \"localhost\"/DB_SERVER = \""$IP"\"/g" ./vpss_def.py
#sudo sed -i "s/CLOUD_SERVER = \"localhost\"/CLOUD_SERVER = \""$IP"\"/g" ./vpss_def.py
python SET_AUTHORITY_server.py
python SET_SEARCH_server.py
python SET_CLOUD_server.py














