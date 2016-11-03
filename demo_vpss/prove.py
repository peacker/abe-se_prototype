import os
# get users
def get_users_data(filename):
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
    print users

# get attributes
def get_attribute_universe(filename):
    with open(os.getcwd() + os.sep + filename,"r") as f:
        s = f.read().splitlines()[0]
    f.close()
    return s.split(",")

# -----------------------------------------------------------------------

print get_attribute_universe("attributes.txt")

get_users_data("users.txt")


"""
USERS = [ 
          { "name":"utente1",
            "pwd":"123",
            "attr":[ATTRIBUTES[0]] },
          { "name":"utente2",
            "pwd":"123",
            "attr":[ATTRIBUTES[0],ATTRIBUTES[1]] },
          { "name":"utente3",
            "pwd":"123",
            "attr":[ATTRIBUTES[0], ATTRIBUTES[1], ATTRIBUTES[2], ATTRIBUTES[3]] },
          { "name":"AUTHORITY",
            "pwd":"123",
            "attr": ATTRIBUTES }
        ]
"""
