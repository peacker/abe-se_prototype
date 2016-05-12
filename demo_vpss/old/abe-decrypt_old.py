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
    assert len(sys.argv) == 5, "BAD or NO (PUBLIC KEY, SECRET KEY, " + \
                               "FILENAME, USER FOLDER) DEFINED!!!"    
    
    # set publick key
    pk = sys.argv[1]

    # set policy
    sk = sys.argv[2]

    # filename
    filename = sys.argv[3]

    # set userfolder
    username = sys.argv[4]

    # read group name from file
    with open(os.getcwd() + "/public_parameters/" + "groupname.g", "r") as fg:
        group_name = fg.read()
    fg.closed

    # set group definitions
    groupObj = PairingGroup(group_name)
    group = groupObj
    cpabe = CPabe(groupObj)

    # read public key from public.k
    with open(os.getcwd() + "/public_parameters/" + "public.k", "rb") as fp:
        pk = bytesToObject(fp.read(),group)
    fp.closed

    # read secret key from secret.k
    with open(os.getcwd() + "/users/"+ username + "/secret_keys/ABE_sk/" + sk, "rb") as fs:
        sk = bytesToObject(fs.read(),group)
    fs.closed

    # read encrypted symmetric key from symmetric.k.enc
    with open(os.getcwd() + "/users/"+ username + "/secret_keys/AES_sk/symmetric.k.enc", "rb") as feck:
        enc_symk = bytesToObject(feck.read(),group)
    feck.closed

    # decrypt the encrypted symmetric key
    symk = cpabe.decrypt(pk, sk, enc_symk)


    # print to shell
    """
    if debug:
        groupObj.debug(symk)
        print('symmetric key = %s' % symk)
    """
     
    # write decrypted symmetric key to file symmetric.k
    with open(os.getcwd() + "/users/"+ username + "/secret_keys/AES_sk/symmetric.k", "wb") as fsk:
        fsk.write(objectToBytes(symk, group))
    fsk.closed

    del groupObj

if __name__ == "__main__":
    debug = True
    main()
