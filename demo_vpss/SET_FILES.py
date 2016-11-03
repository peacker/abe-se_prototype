#!/usr/bin/python

# to set a new def_users.txt type
# python SET_FILES.py

import os   # operating system functions
import sys
import shutil
import random

# definitions
from vpss_def import *
from vpss_func import *

# ----------------------------------------------------------------------------

ATTRIBUTES = ["ROMA","MILANO","TORINO","NAPOLI",    # 0,1,2,3
              "MANAGER","BUSINESS","MARKETING","IT",        # 4,5,6,7
              "FINANCE","ADMINISTRATION","CONSULING","CALLCENTER",        # 8,9,10,11
              "UFFICIO1","UFFICIO2","UFFICIO3","UFFICIO4",        #12,13,14,15
              "UFFICIO5","UFFICIO6","UFFICIO7","UFFICIO8",        #16,17,18,19
              "FILIALE1","FILIALE2","FILIALE3","FILIALE4",        #20,21,22,23
              "GROUP1","GROUP2","GROUP3","GROUP4",                     #24,25, 26,27
              "GROUP5","GROUP6","GROUP7","GROUP8", #28,29,30,31
              "OPERANTENEL2010","OPERANTENEL2011","OPERANTENEL2012", #32,33,34
              "OPERANTENEL2013","OPERANTENEL2014","OPERANTENEL2015"  #35,36,37
             ]

POLICIES = [
            "(" + ATTRIBUTES[0] + " or " + ATTRIBUTES[1] + " or " + \
            ATTRIBUTES[2] + " ) and " + ATTRIBUTES[31] 
            ,
            "(" + ATTRIBUTES[0] + " or " + ATTRIBUTES[1] + ") and " + \
            ATTRIBUTES[26] + " and " + ATTRIBUTES[28]
            ,
            ATTRIBUTES[0] + " and " + ATTRIBUTES[4] + " and (" + \
            ATTRIBUTES[12] + " or " + ATTRIBUTES[13] + ") and " + \
            ATTRIBUTES[24] + " and " + ATTRIBUTES[25] + " and " + \
            ATTRIBUTES[26] + " and " + ATTRIBUTES[27] + " and " + \
            ATTRIBUTES[37]
           ] + ATTRIBUTES

USERS = [ 
          { "name":"GiuseppeVerdi",
            "pwd":"123",
            "attr":[ATTRIBUTES[0], 
                    ATTRIBUTES[4], 
                    ATTRIBUTES[12],  
                    ATTRIBUTES[20],
                    ATTRIBUTES[24], ATTRIBUTES[25], ATTRIBUTES[26], ATTRIBUTES[27],
                    ATTRIBUTES[28], ATTRIBUTES[29], ATTRIBUTES[30],
                    ATTRIBUTES[31],
                    ATTRIBUTES[34], ATTRIBUTES[35], ATTRIBUTES[36], ATTRIBUTES[37]
                   ]
          },
          { "name":"MarioRossi",
            "pwd":"123",
            "attr":[ATTRIBUTES[0], 
                    ATTRIBUTES[5], 
                    ATTRIBUTES[13], ATTRIBUTES[14],
                    ATTRIBUTES[21],
                    ATTRIBUTES[26], ATTRIBUTES[27],
                    ATTRIBUTES[28], 
                    ATTRIBUTES[35], ATTRIBUTES[36], ATTRIBUTES[37]
                   ]
          },
          { "name":"GennaroEsposito",
            "pwd":"123",
            "attr":[ATTRIBUTES[0], 
                    ATTRIBUTES[5], 
                    ATTRIBUTES[13],  
                    ATTRIBUTES[20],
                    ATTRIBUTES[25], ATTRIBUTES[26], ATTRIBUTES[27],
                    ATTRIBUTES[28], ATTRIBUTES[30],
                    ATTRIBUTES[31],
                    ATTRIBUTES[36], ATTRIBUTES[37]
                   ]
          },
          { "name":"MarcoBianchi",
            "pwd":"123",
            "attr":[ATTRIBUTES[0], ATTRIBUTES[1],
                    ATTRIBUTES[4], ATTRIBUTES[5], ATTRIBUTES[6],
                    ATTRIBUTES[12],  
                    ATTRIBUTES[20], ATTRIBUTES[21], ATTRIBUTES[22],
                    ATTRIBUTES[24], ATTRIBUTES[25], ATTRIBUTES[26], ATTRIBUTES[27],
                    ATTRIBUTES[28], ATTRIBUTES[29], ATTRIBUTES[30],
                    ATTRIBUTES[31],
                    ATTRIBUTES[36], ATTRIBUTES[37]
                   ]
          }
          ,
          { "name":"AUTHORITY",
            "pwd":"123",
            "attr": []# ATTRIBUTES 
          }
        ]
for i in range(1,11):
    temp = { "name":"User_"+str(i),
            "pwd":"123",
            "attr":[ATTRIBUTES[random.randrange(0,4)], 
                    ATTRIBUTES[random.randrange(4,12)], 
                    ATTRIBUTES[random.randrange(12,20)],  
                    ATTRIBUTES[random.randrange(20,24)],
                    ATTRIBUTES[random.randrange(24,28)],
                    ATTRIBUTES[random.randrange(28,32)],
                    ATTRIBUTES[random.randrange(32,38)]
                   ]
          }
    USERS.append(temp)

with open(ATTRIBUTES_FILE, "w") as f:            
   f.write(",".join(ATTRIBUTES))
f.closed

with open(POLICIES_FILE, "w") as f:
   for temp in POLICIES:
       f.write(temp + "\n")
f.closed

with open(USERS_FILE, "w") as f:            
   for temp in USERS:
       f.write(temp["name"] + ":" + temp["pwd"] + ":" + ",".join(temp["attr"]) + "\n")
f.closed


