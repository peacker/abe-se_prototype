#!/usr/bin/python

# to set a new def_users.txt type
# python SET_FILES.py

import os   # operating system functions
import sys
import shutil

# definitions
from vpss_def import *
from vpss_func import *

# ----------------------------------------------------------------------------

ATTRIBUTES = ["ESERCITO","MARINA","AERONAUTICA","CARABINIERI",    # 0,1,2,3
              "REPARTO1","REPARTO2","REPARTO3","REPARTO4",        # 4,5,6,7
              "REPARTO5","REPARTO6","REPARTO7","REPARTO8",        # 8,9,10,11
              "UFFICIO1","UFFICIO2","UFFICIO3","UFFICIO4",        #12,13,14,15
              "UFFICIO5","UFFICIO6","UFFICIO7","UFFICIO8",        #16,17,18,19
              "SEZIONE1","SEZIONE2","SEZIONE3","SEZIONE4",        #20,21,22,23
              "NOSSEGRETO","NOSSEGRETISSIMO",                     #24,25
              "NOSRISERVATO","NOSRISERVATISSIMO",                 #26,27
              "QNAZIONALE","QNATO","QUE",                         #28,29,30
              "ACCESSOCIFRA",                                     #31
              "OPERANTENEL2010","OPERANTENEL2011","OPERANTENEL2012", #32,33,34
              "OPERANTENEL2013","OPERANTENEL2014","OPERANTENEL2015"  #35,36,37
             ]

POLICIES = ATTRIBUTES + [
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
           ]

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


