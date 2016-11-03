import sys     
import os
from subprocess import *

# ABE modules
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc

from choose_abe_scheme import *
#from abenc_waters09 import *

# for serialization
from charm.core.engine.util import objectToBytes,bytesToObject

def read_serialized_object(filename, group):
    """
    Only for elliptic curve elements
    EX:
    from abe_fileio import *
    read_serialized_object
    """

    with open(filename, "rb") as f:
        #return bytesToObject(f.read(),group)
        return group.deserialize(f.read())
    f.closed

def write_deserialized_object(filename, obj, group):
    """
    EX:
    Only for elliptic curve elements
    from abe_fileio import *
    write_deserialized_object
    """

    with open(filename, "wb") as f:
        #f.write(objectToBytes(obj, group)) 
        f.write(group.serialize(obj))
    f.closed

def read_object(filename, group):
    """
    EX:
    from abe_fileio import *
    read_object
    """

    with open(filename, "rb") as f:
        return bytesToObject(f.read(),group)
        #return group.deserialize(f.read())
    f.closed

def write_object(filename, obj, group):
    """
    EX:
    from abe_fileio import *
    write_object
    """

    with open(filename, "wb") as f:
        f.write(objectToBytes(obj, group)) 
        #f.write(group.serialize(obj))
    f.closed



#def create_metadata_and_encrypted_file():
    

#def extract_metadata_from_encrypted_file():
    
