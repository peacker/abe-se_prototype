import sys     
import os

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc

from choose_abe_scheme import *
#from abenc_waters09 import *

# for serialization
from charm.core.engine.util import objectToBytes,bytesToObject


def main():

    # check inputs have been inserted
    assert len(sys.argv) == 4, 'BAD or NO (PUBLIC KEY, POLICY, USER NAME) DEFINED!!!'    
    
    # set publick key
    pk = sys.argv[1]

    # set policy
    pol = sys.argv[2]

    # set userfolder
    username = sys.argv[3]

    # read group name from file
    with open(os.getcwd() + '/public_parameters/groupname.g', 'r') as fg:
        group_name = fg.read()
    fg.closed

    # set group definitions
    groupObj = PairingGroup(group_name)
    group = groupObj
    cpabe = CPabe(groupObj)

    # generate random symmetric key
    symk = groupObj.random(GT)
    # write to file the symmetric key
    # write symmetric key to file symmetric.k
    with open(os.getcwd() + "/users/" + username + '/secret_keys/AES_sk/symmetric.k', 'wb') as fsk:
        fsk.write(objectToBytes(symk, group))
    fsk.closed

    # read public key from public.k
    with open(os.getcwd() + '/public_parameters/' + pk, 'rb') as fp:
        pk = bytesToObject(fp.read(),group)
    fp.closed

    # encrypt the symmetric key (should be hashed before use)
    enc_symk = cpabe.encrypt(pk, symk, pol)

    # print to shell
    """
    if debug:
        groupObj.debug(enc_symk)
        print('encrypted symmetric key = %s' % enc_symk)
    """
     
    # write to file the encrypted symmetric key
    # write encrypted symmetric key to file symmetric.k.enc
    with open(os.getcwd() + "/users/" + username + '/secret_keys/AES_sk/symmetric.k.enc', 'wb') as fesk:
        fesk.write(objectToBytes(enc_symk, group))
    fesk.closed

    del groupObj

if __name__ == '__main__':
    debug = True
    main()
