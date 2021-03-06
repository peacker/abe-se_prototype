# system modules
import os

# ----------------------------------------------------------------------------

# get users
def get_users_data(filename):
    """
    Reads users data from the file filename, 
    whose structure must be as follows:
    -------------------------------------------
    utente1:123:ATTR1
    utente2:123:ATTR1,ATTR2
    utente3:123:ATTR1,ATTR2,ATTR3,ATTR4
    AUTHORITY:123:ATTR1,ATTR2,ATTR3,ATTR4,ATTR5
    -------------------------------------------
    """
    with open(os.getcwd() + os.sep + filename,"r") as f:
        lines = f.read().splitlines()
    f.close()
    users = []
    i = 0
    for l in lines:
        users.append({})
        users[i]["name"] =  l.split(":")[0]
        users[i]["pwd"] =  l.split(":")[1]
        users[i]["attr"] =  l.split(":")[2].split(",")
        i = i + 1
    return users

# ----------------------------------------------------------------------------

# get attributes
def get_attribute_universe(filename):
    """
    Reads attribute universe from the file filename, 
    whose structure must be as follows:
    -------------------------------------------
    ATTR1,ATTR2,ATTR3,ATTR4,ATTR5
    -------------------------------------------
    """
    with open(os.getcwd() + os.sep + filename,"r") as f:
        s = f.read().splitlines()[0]
    f.close()
    return s.split(",")

# ----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

# --------------
# ERROR MESSAGES
# --------------

OK = 0
WRONG_CIPHERTEXT_EXTENSION = -1
ABE_DECRYPTION_FAILED = -2
AES_DECRYPTION_FAILED = -3
UNAUTHORIZED_DECRYPTION_KEY = -4
ABE_ENCRYPTION_FAILED = -5
AES_ENCRYPTION_FAILED = -6
RANDOM_POINT_GEN_FAILED = -7
OBSOLETE_ENCRYPTED_FILE = -8
SEARCH_DB_CONNECTION_FAILED = -9
BAD_SYNTAX = -10
NO_SEARCH_KEY_AVAILABLE = -11

#-----------------------------------------------------------------------------

# ----------
# FILE NAMES
# ----------

# files
ATTRIBUTES_FILE = "def_attributes.txt"
POLICIES_FILE = "def_policies.txt"
USERS_FILE = "def_users.txt"

TELSY_LOGO_ICO = "telsy_logo.ico"
TELSY_LOGO_PNG = "telsy_logo.png"

# keys names
PK = "public.k"
MK = "master.k"
SYMK = "password.k"
SEAK = "search.k"
search_key = "0123456789abcdef"
search_iv = "0000000000000000"

# file names
PT = ["prova1.txt", "prova2.txt", "prova3.txt", "prova4.txt"]
CT_ABEK = ["prova1.txt.k.enc", "prova2.txt.k.enc", "prova3.txt.k.enc", "prova4.txt.k.enc"]
CT = ["prova1.txt.enc", "prova2.txt.enc", "prova3.txt.enc", "prova4.txt.enc"]



#-----------------------------------------------------------------------------

# ----------------
# GLOBAL VARIABLES
# ----------------

verbose = True

FILESEPARATOR = "___FILESEPARATOR___"
NODATA = b"EMPTY"

# curves
CURVES = [[80,"SS512"],
          [112,"SS_e_R224Q1024"],
          [112,"SS_e_R224Q2048"],
          [128,"SS_e_R256Q1536"],
          [256,"SS_e_R512Q7680"]
]
#          [128,"SS_e_R256Q3072"]
#          [192,"SS_e_R384Q8192"]


GROUP_NAME = "SS512"
#GROUP_NAME = "SS_e_R224Q1024"
#GROUP_NAME = "SS_e_R224Q2048"

# attribute universe
ATTRIBUTES = get_attribute_universe("def_attributes.txt")
#ATTRIBUTES = ["ATTR1", "ATTR2", "ATTR3", "ATTR4", "ATTR5"]

# user data
USERS_PWD = "123"
USERS = get_users_data(USERS_FILE)

AUTHORITY_NAME = "AUTHORITY"

USERS_ATTR = []
for i in range(len(USERS)):
    USERS_ATTR.append(":".join(USERS[i]["attr"]))

#-----------------------------------------------------------------------------

# -------
# FOLDERS
# -------

# authority's folders
AUTH_FOLDER = os.path.join(os.getcwd(), "authority")
AUTH_MASTER_KEY_FOLDER = os.path.join(os.getcwd(), "authority", "master_keys")
AUTH_SECRET_KEY_FOLDER = os.path.join(os.getcwd(), "authority", "user_data")
AUTH_TEMP_FOLDER = os.path.join(os.getcwd(), "authority", "temp")

# public folders
PUBLIC_PARAMETERS_FOLDER = os.path.join(os.getcwd(), "public_parameters")

# user's folders
USER_FOLDER = os.path.join(os.getcwd(), "users")
USER_SECRET_KEYS = "secret_keys"
USER_AES_KEY = os.path.join("secret_keys","AES_sk")
USER_ABE_KEY = os.path.join("secret_keys", "ABE_sk")
USER_SEARCH_KEY = os.path.join("secret_keys", "SEARCH_sk")
USER_PLAINTEXT = "plaintexts"
USER_CIPHERTEXT = "ciphertexts"

# file extensions
GROUP_EXT = ".g"
KEY_EXT = ".k"
CT_EXT = ".enc"
ENC_KEY_EXT = ".k.enc"

# key and file names
MASTER_KEY = "master" + KEY_EXT
PUBLIC_KEY = "public" + KEY_EXT
SECRET_KEY = "_secret" + KEY_EXT
GROUP = "group" + GROUP_EXT
SYMMETRIC_KEY = "symmetric" + KEY_EXT
SYMMETRIC_ENC_KEY = "enc_symmetric" + KEY_EXT
TIME_COUNTER = "time.t"

#-----------------------------------------------------------------------------

# -------
# SERVERS
# -------

# get info from def_servers.txt
with open(os.getcwd() + os.sep + "def_servers.txt","r") as f:
    lines = f.read().splitlines()
f.close()

# database server
AUTH_SERVER = lines[0].split("=")[1]
AUTH_USER = lines[1].split("=")[1]
AUTH_PASSWORD = lines[2].split("=")[1]
AUTH_NAME = lines[3].split("=")[1]

AUTH_ROOT = lines[4].split("=")[1]
AUTH_ROOTPWD = lines[5].split("=")[1]


# search server
SEARCH_SERVER = lines[6].split("=")[1]
SEARCH_USER = lines[7].split("=")[1]
SEARCH_PASSWORD = lines[8].split("=")[1]
SEARCH_NAME = lines[9].split("=")[1]

SEARCH_ROOT = lines[10].split("=")[1]
SEARCH_ROOTPWD = lines[11].split("=")[1]

# cloud server 
CLOUD_SERVER = lines[12].split("=")[1]
CLOUD_USERNAME = lines[13].split("=")[1]
CLOUD_PASSWORD = lines[14].split("=")[1]


CLOUD_FOLDER = os.path.join("home","cloud")
# must be the same as the one in INSTALL_SERVER.sh


