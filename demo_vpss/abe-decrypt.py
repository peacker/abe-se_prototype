import sys     
import os

import time
from vpss_def import *

# ABE modules
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc

from choose_abe_scheme import *
#from abenc_waters09 import *

# for serialization
from charm.core.engine.util import objectToBytes,bytesToObject

from abe_fileio import *

def main():
    """
    All inputs are received as file with their absolute path
    INPUT:
    - group definition
    - public key
    - secret key
    - file name to be decrypted
    - decrypted file name (destination/output file)

    python3 abe-encrypt.py [group] [pk] [sk] [in_file] [out_file]
    EX:
    python3 abe-decrypt.py \
            ./public_parameters/groupname.g \
            ./public_parameters/public.k \
            ./users/utente1/secret_keys/ABE_sk/utente1_secret.k \
            ./users/utente1/ciphertexts/prova.txt.k.enc \
            ./users/utente1/secret_keys/AES_sk/symmetric.k 
    """

    # check inputs have been inserted
    assert len(sys.argv) == 6, "BAD or NO (GROUP, PUBLIC KEY, SECRET KEY, INPUT or OUTPUT FILE) DEFINED!!!"    

    # set group name, e.g. ./public_parameters/groupname.g
    # read group name from file
    with open(sys.argv[1], "r") as f:
        group_name = f.read()
    f.closed

    # set group definitions
    groupObj = PairingGroup(group_name)
    group = groupObj
    cpabe = CPabe(groupObj)
    
    # set publick key, e.g. ./public_parameters/public.k
    pk = read_object(sys.argv[2], group)
    #with open(sys.argv[2], "rb") as f:
    #    pk = bytesToObject(f.read(),group)
    #f.closed

    # set secret key, e.g. ./users/utente1/secret_keys/ABE_sk/utente1_secret.k
    sk = read_object(sys.argv[3], group)
    #with open(sys.argv[3], "rb") as f:
    #    sk = bytesToObject(f.read(),group)
    #f.closed

    # set input file
    infile = read_object(sys.argv[4], group)
    #with open(sys.argv[4], "rb") as f:
    #    infile = bytesToObject(f.read(),group)
    #f.closed

    # set output file, i.e. destination of the encrypted file 
    # (overwrites if already exists)
    outfile = sys.argv[5]

    # decrypt input file
    start = time.clock()
    dec_file = cpabe.decrypt(pk, sk, infile)
    end = time.clock()
    if verbose: 
        print ("*** abe-keygen CLOCK TIME: " + str(end - start) + " sec")
    
    if dec_file:
        # write to output file
        # e.g. ./users/utente1/ciphertexts/nome_file.k.enc
        write_deserialized_object(outfile, dec_file, group)
        #with open(outfile, "wb") as f:
        #    f.write(objectToBytes(dec_file, group))
        #f.closed
    else:
        with open(outfile, "wb") as f:
            f.write(b"USER_KEY_DOES_NOT_SATISFY_POLICY")

    del groupObj


if __name__ == "__main__":
    debug = True
    main()
