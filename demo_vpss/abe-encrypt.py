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
    All inputs (except policy) are received as file with their absolute path
    INPUT:
    - group definition
    - public key
    - policy
    - file name to be encrypted (must contain an elliptic curve point)
    - encrypted file name (destination/output file)

    python3 abe-encrypt.py [group] [pk] [policy] [in_file] [out_file]
    EX:
    python3 abe-encrypt.py \
            ./public_parameters/groupname.g \
            ./public_parameters/public.k \
            '(ATTR1 and ATTR2)' \
            ./users/utente1/secret_keys/AES_sk/symmetric.k \
            ./users/utente1/ciphertexts/symmetric.k.enc
    """

    # check inputs have been inserted
    assert len(sys.argv) == 6, "BAD or NO (GROUP, PUBLIC KEY, " + \
                               "POLICY, INPUT or OUTPUT FILE) DEFINED!!!"    

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
    # read public key from public.k
    pk = read_object(sys.argv[2], group)
    #with open(sys.argv[2], "rb") as f:
    #    pk = bytesToObject(f.read(),group)
    #f.closed

    # set policy
    pol = sys.argv[3]

    # set input file
    infile = read_serialized_object(sys.argv[4], group)
    #with open(sys.argv[4], "rb") as f:
    #    infile = bytesToObject(f.read(),group)
    #f.closed

    # set output file, i.e. destination of the encrypted file 
    # (overwrites if already exists)
    outfile = sys.argv[5]

    #print ("infile = %s\n" % infile)
    #print ("outfile = %s\n" % outfile)

    # encrypt input file
    start = time.clock()
    enc_file = cpabe.encrypt(pk, infile, pol)
    end = time.clock()
    if verbose: 
        print ("*** abe-keygen CLOCK TIME: " + str(end - start) + " sec")

    #print ("enc_file = %s\n" % enc_file)

    # write to output file
    # e.g. ./users/utente1/ciphertexts/nome_file.k.enc
    write_object(outfile, enc_file, group)
    #with open(outfile, "wb") as f:
    #    f.write(objectToBytes(enc_file, group))
    #f.closed

    del groupObj

if __name__ == '__main__':
    debug = True
    main()
