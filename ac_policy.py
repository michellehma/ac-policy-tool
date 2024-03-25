import random
import json
from datetime import date

model = input("Enter number for access control model \n1. ABAC \n2. RBAC \n3. CT-RBAC \n4. OT-ABAC 5. PBAC\n")
subjectAttributes = {"name": [],
                     "organization": [], 
                     "job title": [], 
                     "account ID": []}
objectAttributes = {0:["partkey", "name", "mfgr", "brand", "type" , "size", "container", "retailprice", "comment"],
                    1:["suppkey", "name", "address", "nationkey", "phone", "acctbal", "comment"],
                    2:["partkey", "suppkey", "availqty", "supplycost", "comment"],
                    3:["custkey", "name", "address", "nationkey", "phone", "acctbal", "mktsegment", "comment"],
                    4:["nationkey", "name", "regionkey", "comment"],
                    5:["orderkey", "partkey", "suppkey", "linenumber", "quantity", "extendedprice",
                                "discount", "tax", "returnflag", "linestatus", "shipdate", "commitdate", "receiptdate",
                                "shipinstruct", "shipmode", "comment"],
                    6:["regionkey", "name", "comment"],
                    7:["orderkey", "custkey", "orderstatus", "totalprice", "orderdate", "order-priority", "clerk", "ship-priority", "comment"]}
numColumns = {0:9, 1:7, 2:5, 3:8, 4:4, 5:16, 6:3, 7:9}
envirAttributes = {"time":["morning", "afternoon", "evening", "night"],
                    "date": date.today(),
                    "networkSec":[1, 2, 3],
                    "services":[]}

roles = ["ceo", "supervisor", "engineer", "investor", "labor", "customer", "supplier", "financial advisor", "marketing specialist"]
resources = {"part":[ "partkey", "name", "mfgr", "brand", "type" , "size", "container", "retailprice", "comment"],
             "supplier":["suppkey", "name", "address", "nationkey", "phone", "acctbal", "comment"],
             "partsupp":["partkey", "suppkey", "availqty", "supplycost", "comment"],
             "customer":["custkey", "name", "address", "nationkey", "phone", "acctbal", "mktsegment", "comment"],
             "nation":["nationkey", "name", "regionkey", "comment"],
             "lineitem":["orderkey", "partkey", "suppkey", "linenumber", "quantity", "extendedprice",
                         "discount", "tax", "returnflag", "linestatus", "shipdate", "commitdate", "receiptdate",
                         "shipinstruct", "shipmode", "comment"],
             "region":["regionkey", "name", "comment"],
             "orders":["orderkey", "custkey", "orderstatus", "totalprice", "orderdate", "order-priority", "clerk", "ship-priority", "comment"]}
tags = {"finance":["retailprice", "supplycost", "extendedprice", "acctbal", "discount", "tax", "totalprice"],
        "order management":["orderkey", "orderstatus", "orderdate", "order-priority", "ship-priority", "linestatus", "shipdate", "commitdate", "receiptdate",
                            "shipinstruct", "shipmode"],
        "inventory":["partkey", "suppkey", "orderkey" "availqty", "quantity"],
        "communication":["suppkey", "custkey", "name", "phone", "address"],
        "location":["address", "nationkey", "regionkey"],
        "shipping":["shipdate", "shipinstruct", "shipmode", "ship-priority"]}

purposes = {"keep inventory":["partkey", "suppkey", "orderkey" "availqty", "quantity"],
            "calculate profit/cost":["partkey", "suppkey", "orderkey", "custkey", "retailprice", "supplycost", "extendedprice", "acctbal", "discount", "tax", "totalprice"],
            "prepare order":["partkey", "suppkey", "orderkey", "orderstatus", "orderdate", "order-priority", "ship-priority", "linestatus", "shipdate", "commitdate", "receiptdate",
                            "shipinstruct", "shipmode", "quantity"],
            "contact customer":["custkey", "name", "address", "phone"],
            "contact supplier":["suppkey", "name", "address", "phone"],
            "handle shipping":["orderkey", "partkey", "suppkey", "linestatus", "orderstatus", "orderdate", "address", "nationkey", "shipdate", "shipinstruct", "shipmode", "ship-priority"]}

policy = None

def added(tableNum, numInTable, list):
    count = 0
    for element in list:
        if element[0] == tableNum:
            count += 1
    if count >= numInTable:
        return True
    return False

if model == 1: 
    #randomize number of attributes to combine
    #randomize which attributes to choose
    numSubject = random.randint(1, 4)
    numObject = random.randint(1, 61)
    numEnvir = random.randint(1, 4)
    subjects = []
    objects = []
    envir = []
    attributeS = []
    attributeO = []
    attributeE = []
    for subject in range(numSubject):
        category = random.randint(0, 3)
        while added(category, numColumns[table], attributeS):
            attribute = random.randint(0, 3)
        if attribute == 0:
            name = random.randint(0, 50)
            subjects.append(subjectAttributes[subject])
            attributeS.append(attribute)
        elif attribute == 1:
            subjects.append(subjectAttributes[subject])
            attributeS.append(attribute)
        elif attribute == 2:
            subjects.append(subjectAttributes[subject])
            attributeS.append(attribute)
        elif attribute == 3:   
            subjects.append(subjectAttributes[subject])
            attributeS.append(attribute) 
        
    for object in range(numObject):
        table = random.randint(0, 7)
        while added(table, numColumns[table], attributeO):
            table = random.randint(0, 7)
        if table == 0:
            attribute = random.randint(0, 8)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 8)
                pair = [table, attribute]
            objects.append(objectAttributes[0][attribute])
            attributeO.append(pair)
        elif table == 1:
            attribute = random.randint(0, 6)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 6)
                pair = [table, attribute]
            objects.append(objectAttributes[1][attribute])
            attributeO.append(pair)
        elif table == 2:
            attribute = random.randint(0, 4)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 4)
                pair = [table, attribute]
            objects.append(objectAttributes[2][attribute])
            attributeO.append(pair)
        elif table == 3:
            attribute = random.randint(0, 7)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 7)
                pair = [table, attribute]
            objects.append(objectAttributes[3][attribute])
            attributeO.append(pair)
        elif table == 4:
            attribute = random.randint(0, 3)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 3)
                pair = [table, attribute]
            objects.append(objectAttributes[4][attribute])
            attributeO.append(pair)
        elif table == 5:
            attribute = random.randint(0, 15)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 15)
                pair = [table, attribute]
            objects.append(objectAttributes[5][attribute])
            attributeO.append(pair)
        elif table == 6:
            attribute = random.randint(0, 2)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 2)
                pair = [table, attribute]
            objects.append(objectAttributes[6][attribute])
            attributeO.append(pair)
        elif table == 7:
            attribute = random.randint(0, 9)
            pair = [table, attribute]
            while pair in attributeO:
                attribute = random.randint(0, 9)
                pair = [table, attribute]
            objects.append(objectAttributes[7][attribute])
            attributeO.append(pair)

    for envir in range(numEnvir):
        attribute = random.randint(0, 3)
        while attribute in attributeE:
            attribute = random.randint(0, 3)
        if attribute == 0:
            randomTime = random.randint(0, 3)
            envir.append(envirAttributes["time"][randomTime])
        elif attribute == 1:
            envir.append(envirAttributes["date"])
        elif attribute == 2:
            randomLvl = random.randint(0, 2)
            envir.append(envirAttributes["networkSec"][randomLvl])
        elif attribute == 3:
            envir.append(envirAttributes["services"])
        
    policyDict = {"model":"ABAC",
                  "subject attributes": subjects,
                  "object attributes": objects,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

elif model == 2:
    policyDict = {"model":"RBAC",
                  "subject attributes": subjects,
                  "object attributes": objects,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

elif model == 3:
    policyDict = {"model":"CT-RBAC",
                  "subject attributes": subjects,
                  "object attributes": objects,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

elif model == 4:
    policyDict = {"model":"OT-ABAC",
                  "subject attributes": subjects,
                  "object attributes": objects,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

elif model == 5:
    policyDict = {"model":"PBAC",
                  "subject attributes": subjects,
                  "object attributes": objects,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

else:
    print("Invalid input, try again")

print(policy)