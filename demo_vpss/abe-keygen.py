import sys     

import time
from vpss_def import *

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
    - group definition, as string
    - location of the group definition
    - location of the public key and public key name
    - location of the master key and master key name

    python3 abe-setup.py [group_name] [mk] [pk] [attr_list] [sk]
    EX:
    python3 abe-keygen.py \
        ./public_parameters/${GROUP_NAME}".g" \
        ./authority/master_keys/master.k
        ./public_parameters/public.k \
        ATTR1:ATTR2 \
        ./authority/user_data/secret.k
    """
    # check inputs have been inserted
    assert len(sys.argv) == 6, "BAD or NO (GROUP NAME, MASTER KEY, " + \
                               "PUBLIC KEY, ATTRIBUTE LIST, SECRET KEY ) " + \
                               "DEFINED!!!"  

    # set attribute list
    attr_list = sys.argv[4].split(":")

    # read group name from file
    with open(sys.argv[1], "r") as f:
        group_name = f.read()
    f.closed

    # set group definitions
    groupObj = PairingGroup(group_name)
    group = groupObj
    cpabe = CPabe(groupObj)

    # read master key from master.k
    msk = read_object(sys.argv[2], group)

    # read public key from public.k
    pk = read_object(sys.argv[3], group)

    start = time.clock()
    # create secret key
    sk = cpabe.keygen(pk, msk, attr_list)
    end = time.clock()
    if verbose: 
        print ("*** abe-keygen CLOCK TIME: " + str(end - start) + " sec")

    # write secret key to file secret.k
    write_object(sys.argv[5], sk, group)

    del groupObj

if __name__ == "__main__":
    debug = True
    main()
