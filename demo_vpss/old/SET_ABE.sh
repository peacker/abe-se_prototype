#!/bin/bash
 
##########################
# run typing in terminal: 
# sudo bash SET_ABE.sh         
##########################

# remove all files from "cloud" folder
#rm /home/cloud/*

GROUP_NAME="SS512"
#GROUP_NAME="SS_e_R224Q1024"
#GROUP_NAME="SS_e_R224Q1024"

# keys names
PK="public.k"
MK="master.k"
#SK="secret.k"
SYMK="symmetric.k"

#public parameters folder
AUTHFOLDER="./authority"
PPFOLDER="./public_parameters"
USERSFOLDER="./users"
CLOUD="./encrypted_files"

# attributes universe
#ATTR=( ATTR1 ATTR2 ATTR3 ATTR4 ATTR5 )
ATTR=( "ATTR1" "ATTR2" "ATTR3" "ATTR4" "ATTR5" )
NUM_ATTR=${#ATTR[@]}

# user data
USERS=("utente1" "utente2" "utente3")
NUM_USERS=${#USERS[@]}
USERS_ATTR=(
  ${ATTR[0]}
  ${ATTR[0]}:${ATTR[1]}
  ${ATTR[0]}:${ATTR[1]}:${ATTR[2]}:${ATTR[3]}
)

# file names
PT=("prova1.txt" "prova2.txt" "prova3.txt" "prova4.txt")
NUM_PT=${#PT[@]}
CT_ABEK=("prova1.txt.k.enc" "prova2.txt.k.enc" "prova3.txt.k.enc" "prova4.txt.k.enc")
CT=("prova1.txt.enc" "prova2.txt.enc" "prova3.txt.enc" "prova4.txt.enc")


# ---------------------------------------------------------------------------

# -------------------
# SETUP ABE FOLDERS
# -------------------

# Clear folders

rm -r ${AUTHFOLDER}
rm -r ${USERSFOLDER}
rm -r ${PPFOLDER}
rm -r ${CLOUD}

# Set new cleaned folders

mkdir ${AUTHFOLDER}
mkdir ${AUTHFOLDER}/master_keys \
      ${AUTHFOLDER}/user_data

mkdir ${PPFOLDER}

mkdir ${CLOUD}

mkdir ${USERSFOLDER}

for (( i=0; i<${NUM_USERS}; i++ ));
do
  mkdir ${USERSFOLDER}/${USERS[$i]}

  # prepare ${USERNAME} folder
  mkdir ${USERSFOLDER}/${USERS[$i]}/ciphertexts \
        ${USERSFOLDER}/${USERS[$i]}/plaintexts  \
        ${USERSFOLDER}/${USERS[$i]}/secret_keys

  mkdir ${USERSFOLDER}/${USERS[$i]}/secret_keys/ABE_sk \
        ${USERSFOLDER}/${USERS[$i]}/secret_keys/AES_sk

  # generate plaintext file
  for (( j=0; j<${NUM_PT}; j++ ));
  do 
      echo "ciao come va???" > ${USERSFOLDER}/${USERS[$i]}/plaintexts/${PT[$j]}
  done 
done


# ---------------------------------------------------------------------------

# -------------------
# TEST ABE SCHEME
# -------------------

# ABE setup
python3 abe-setup.py \
        ${GROUP_NAME} \
        ${PPFOLDER}  \
        ${PPFOLDER}/${PK} \
        ${AUTHFOLDER}/master_keys/${MK}

# ---------------------------------------------------------------------------

# ABE keygen: create one key for each user
SK="secret"
for (( i=0; i<${NUM_USERS}; i++ ));
do
    SK=${USERS[$i]}"_secret.k"
    ATTR_LIST=${USERS_ATTR[$i]}

    python3 abe-keygen.py \
            ${PPFOLDER}/${GROUP_NAME}".g" \
            ${AUTHFOLDER}/master_keys/${MK} \
            ${PPFOLDER}/${PK} \
            ${ATTR_LIST} \
            ${AUTHFOLDER}/user_data/${SK}

    # assign keys to users
    cp ${AUTHFOLDER}/user_data/${SK} \
       ${USERSFOLDER}/${USERS[$i]}/secret_keys/ABE_sk/${SK}
done

# ---------------------------------------------------------------------------

USERNAME=${USERS[0]}

# ABE generate random point on elliptic curve
python3 abe-random-ec-point.py \
        ${PPFOLDER}/${GROUP_NAME}".g" \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK}

# ---------------------------------------------------------------------------

# ABE encryption
python3 abe-encrypt.py \
        ${PPFOLDER}/${GROUP_NAME}".g" \
        ${PPFOLDER}/${PK} \
        "(ATTR1 and ATTR2)" \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} \
        ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT_ABEK[0]}

# AES encryption
python3 aescrypt.py -f \
        ${USERSFOLDER}/${USERNAME}/plaintexts/${PT[0]} \
        ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT[0]} \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} 


# remove original files
rm ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK}
#rm ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} \
#   ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/symmetric_.k    
rm ${USERSFOLDER}/${USERNAME}/plaintexts/${PT[0]}

# ---------------------------------------------------------------------------

# FAILED ABE decryption
python3 abe-decrypt.py \
        ${PPFOLDER}/${GROUP_NAME}".g" \
        ${PPFOLDER}/${PK} \
        ${USERSFOLDER}/${USERNAME}/secret_keys/ABE_sk/$USERNAME"_secret.k" \
        ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT_ABEK[0]} \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} 

# FAILED AES decryption
python3 aescrypt.py -d -f \
        ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT[0]} \
        ${USERSFOLDER}/${USERNAME}/plaintexts/${PT[0]} \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} 

# ---------------------------------------------------------------------------

#USERNAME=${USERS[1]}

# ABE decryption
python3 abe-decrypt.py \
        ${PPFOLDER}/${GROUP_NAME}".g" \
        ${PPFOLDER}/${PK} \
        ${USERSFOLDER}/utente2/secret_keys/ABE_sk/utente2_secret.k \
        ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT_ABEK[0]} \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} 

# AES decryption
python3 aescrypt.py -d -f \
        ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT[0]} \
        ${USERSFOLDER}/${USERNAME}/plaintexts/${PT[0]} \
        ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK} 

# remove encrypted files
rm ${USERSFOLDER}/${USERNAME}/secret_keys/AES_sk/${SYMK}
rm ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT[0]}
rm ${USERSFOLDER}/${USERNAME}/ciphertexts/${CT_ABEK[0]}

