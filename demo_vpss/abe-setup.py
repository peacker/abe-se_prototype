import os
import sys     

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

    python3 abe-setup.py [group_name] [group] [pk] [mk]
    EX:
    python3 abe-setup.py "SS512" \
        ./public_parameters/             # groupname destination
        ./public_parameters/public.k     # public key destination
        ./authority/master_keys/master.k # master key destinationv
    """
    # check inputs have been inserted
    assert len(sys.argv) == 5, "BAD or NO (GROUP NAME, GROUP DESTINATION, " + \
                               "PUBLIC KEY, MASTER KEY) DEFINED!!!"  

    #Get the eliptic curve with the bilinear mapping feature needed.
    if ( sys.argv[1] != "SS512"  and 
         sys.argv[1] != "SS_e_R224Q1024" and 
         sys.argv[1] != "SS_e_R224Q2048" and 
         sys.argv[1] != "SS_e_R256Q3072" and 
         sys.argv[1] != "SS_e_R384Q8192"
        ) : 
        print ("Error: Unknown group definition!")
    else: 
        group_name = sys.argv[1]

    # set group definitions
    groupObj = PairingGroup(group_name)
    group = groupObj

    cpabe = CPabe(groupObj)
    (msk, pk) = cpabe.setup()

    # print to file the group name
    #grouppath = os.path.join(sys.argv[2], sys.argv[1] + ".g")
    grouppath = os.path.join(sys.argv[2], "group" + ".g")
    with open(grouppath, "w") as f:
        f.write(group_name)
    f.closed

    # print to file the base64 encoded string of msk
    write_object(sys.argv[4], msk, group)

    # print to file the base64 encoded string of pk
    write_object(sys.argv[3], pk, group)

    del groupObj

if __name__ == "__main__":
    debug = True
    main()
