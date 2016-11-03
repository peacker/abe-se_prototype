import sys     
import os

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
    Generates the file [OUTPUT_FILE] 
    containing a random element of the group defined in the file [GROUP_FILE].

    python3 abe-random-ec-point.py [GROUP_FILE] [OUTPUT_FILE]
    EX:
    python3 abe-random-ec-point.py ./public_parameters/groupname.g 
                                   ./users/utente1/secret_keys/AES_sk/symmetric.k
    """
    
    assert len(sys.argv) == 3, "ERROR! BAD or NO (INPUT or OUTPUT FILE) DEFINED!"

    # set group name, e.g. ./public_parameters/groupname.g
    # read group name from file
    with open(sys.argv[1], "r") as f:
        groupname = f.read()
    f.closed

    # set group definitions
    groupObj = PairingGroup(groupname)
    group = groupObj
    cpabe = CPabe(groupObj)

    # generate random symmetric key
    symk = groupObj.random(GT)

    # write to file the symmetric key
    # write symmetric key to file symmetric.k
    write_deserialized_object(sys.argv[2], symk, group)

if __name__ == '__main__':
    debug = True
    main()
