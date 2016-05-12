#!/bin/bash

#sudo apt-get update

sudo chmod -R 755 ../../VPSS

# INSTALL CLIENT FTP AND MYSQL
# ----------------------------

sudo apt-get install --yes ftp
echo "********************* ftp INSTALLED *********************"

# - to uninstall mysql
#sudo service mysql stop
#sudo killall -9 mysql
#sudo killall -9 mysqld
#sudo apt-get remove --purge mysql-server mysql-client mysql-common
#sudo apt-get autoremove
#sudo apt-get autoclean
#sudo deluser mysql
#sudo rm -rf /var/lib/mysql
#sudo apt-get purge mysql-server-core-5.5
#sudo apt-get purge mysql-client-core-5.5
# - or
#sudo apt-get purge mysql-client-core-5.6
#sudo apt-get autoremove
#sudo apt-get autoclean

sudo apt-get install --yes mysql-client
sudo apt-get install --yes mysql-server

#If you are using ubuntu, you have to use the following steps to avoid this error:
# - run the command vim /etc/mysql/my.cnf
# - comment bind-address = 127.0.0.1 using the # symbol
# - restart your mysql server once with
#    service mysql restart
#    or
#    /etc/init.d/mysql restart
echo "********************* MySql INSTALLED *********************"

#INSTALL DEPENDENCIES
#--------------------
# PYTHON 2.7, PYTHON3, WXPYTHON
sudo apt-get install --yes python
sudo apt-get install --yes python-mysqldb
sudo apt-get install --yes python3
sudo apt-get install --yes python-wxgtk2.8
echo "********************* python modules INSTALLED *********************"
# OTHER LIBRARIES:
#      (instructions in the folder CP-ABE-LIB)
#        - GMP 5.x
#        - PBC 0.5.14
#        - OPENSSL

sudo apt-get install --yes m4
echo "********************* m4 INSTALLED *********************"

cd demo_vpss


cd ../CP-ABE-LIB

tar -xvjf gmp-6.0.0a.tar.bz2
tar -xvf pbc-0.5.14.tar
tar -xzvf openssl-1.0.2d.tar.gz
tar -xzvf pycrypto-2.6.1.tar.gz

# gmp library
cd gmp-6.0.0

./configure
make
sudo make install
echo "********************* gmp-6.0.0 INSTALLED *********************"

sudo apt-get install --yes flex
sudo apt-get install --yes bison
echo "********************* flex,bison INSTALLED *********************"
# openssl
sudo apt-get install --yes libssl-dev

echo "********************* libssl-dev INSTALLED *********************"
# pbc library
cd ../../CP-ABE-LIB/pbc-0.5.14
./configure
make
sudo make install
echo "********************* pbc-0.5.14 INSTALLED *********************"

#INSTALL CHARM
#-------------
#    - from a terminal, navigate into the folder
#      "charm-0.43"
#      and run the following commands:

cd ../../charm-0.43
sh configure.sh
sudo make
sudo make install
sudo ldconfig
echo "********************* charm-0.43 INSTALLED *********************"
# do it again...
#cd ../CP-ABE-LIB/pbc-0.5.14
#./configure
#make -l
#sudo make install

#cd ../../charm-0.43
#sh configure.sh
#sudo make -l
#sudo make install
#sudo ldconfig


cd ../demo_vpss
python SET_VPSS_client.py

