import random
import json
from datetime import date

model = input("Enter number for access control model \n1. ABAC \n2. RBAC \n3. CT-RBAC \n4. OT-ABAC 5. PBAC\n")
subjectAttributes = {"name": ["Emma Johnson", "Sophia Martinez", "Liam Brown", "Olivia Garcia", "Noah Taylor", "Isabella Anderson", "Mason Moore", "Charlotte Thompson", "Elijah Wilson", 
                              "Amelia Hernandez", "Harper Davis", "James Rodriguez", "Ava White", "Benjamin Lewis", "Mia Clark", "Alexander Lee", "Evelyn Hall", "Jacob Allen", "Avery Young", 
                              "Ethan Hill", "Scarlett Turner", "Michael Scott", "Abigail Harris", "Emily King", "Daniel Nelson", "Madison Miller", "Chloe Adams", "Samuel Martinez", "Elizabeth Brown", 
                              "David Taylor", "Natalie Walker", "Landon Wright", "Victoria Reed", "Lucas Roberts", "Grace Kelly", "Mason Carter", "William Rivera", "Charlotte Green", "Aria Perez", 
                              "Matthew Brooks", "Audrey Baker", "Gabriel Flores", "Zoe Evans", "William Cox", "Sophie Reed", "Lucas King", "Ella Lee", "Lily Murphy", "Jack Phillips", "Grace Cooper",
                              "Nathan Howard", "Grace Jenkins", "Ethan Powell", "Scarlett Richardson", "Daniel Russell", "Zoey Martin", "Matthew Thompson", "Grace Carter", "Aidan Scott", "Madeline Smith", 
                              "Owen Myers", "Charlotte Gonzalez", "David Hill", "Elizabeth Griffin", "Eli Campbell", "Olivia Stewart", "Brooklyn Evans", "Wyatt Parker", "Peyton Morris", "Aiden Ramirez", 
                              "Arianna Thompson", "Hannah Ward", "Aiden Coleman", "Sophie Gonzalez", "Ava Foster", "Lily Murphy", "Mia Hayes", "Jacob Martin", "Sophia Coleman", "Lucas Jackson", "Abigail White", 
                              "Oliver Baker", "Avery Morgan", "Sophia Collins", "Elijah Adams", "Ella Edwards", "Benjamin Stewart", "Samantha Rivera", "Daniel Martinez", "Aiden Bell"],
                     "job title": ["ceo", "supervisor", "IT specialist", "engineer", "hr", "investor", "labor", "customer", "supplier", "financial advisor", "marketing specialist"], 
                     "clearance":["none", "confidential", "secret", "top secret"],
                     "account id":[8743291, 2157864, 5692148, 7326489, 9815472, 3658921, 4791263, 8254367, 6138952, 2471968, 5987132, 4613978, 7328416, 9851732, 6749213, 5286174, 
                                   3812976, 9162358, 7421863, 8591732, 3159724, 6189274, 2546871, 7139286, 8549162, 6248913, 1593247, 7389652, 4912873, 6372981, 2159378, 8764129, 4921758, 
                                   7684512, 3248976, 9167542, 5874321, 4293187, 8152976, 2475931, 3892157, 6729831, 5319786, 7942168, 2687913, 8796132, 5412897, 6729513, 3186724, 5694127, 
                                   8275614, 7398612, 5419673, 9263178, 2817943, 9748621, 3162897, 7482135, 6517892, 3879162, 5263197, 7839156, 4298167, 1637982, 2879613, 5162793, 7648291, 
                                   8237491, 1983275, 6593812, 8412967, 5724918, 3816479, 1952837, 7614982, 4287193, 6758129, 9138726, 2547183, 6978142, 5861297, 4215893, 7982163, 3658917, 
                                   8192657, 9421867, 5713928, 2684713, 8751946, 4968123, 3846519, 9264713, 1579823, 7298516, 5814729, 9361857, 2748193]}
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
                    "networkSec":[1, 2, 3]}

roles = ["ceo", "supervisor", "IT specialist", "engineer", "investor", "labor", "customer", "supplier", "financial advisor", "marketing specialist"]
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

def getResource(addedAttributes):
    resource = None
    table = random.randint(0, 7)
    while added(table, numColumns[table], addedAttributes):
        table = random.randint(0, 7)
    if table == 0:
        attribute = random.randint(0, 8)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 8)
            pair = [table, attribute]
        resource = pair
    elif table == 1:
        attribute = random.randint(0, 6)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 6)
            pair = [table, attribute]
        resource = pair
    elif table == 2:
        attribute = random.randint(0, 4)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 4)
            pair = [table, attribute]
        resource = pair
    elif table == 3:
        attribute = random.randint(0, 7)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 7)
            pair = [table, attribute]
        resource = pair
    elif table == 4:
        attribute = random.randint(0, 3)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 3)
            pair = [table, attribute]
        resource = pair
    elif table == 5:
        attribute = random.randint(0, 15)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 15)
            pair = [table, attribute]
        resource = pair
    elif table == 6:
        attribute = random.randint(0, 2)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 2)
            pair = [table, attribute]
        resource = pair
    elif table == 7:
        attribute = random.randint(0, 9)
        pair = [table, attribute]
        while pair in addedAttributes:
            attribute = random.randint(0, 9)
            pair = [table, attribute]
        resource = pair
    return resource

if model == 1: 
    #randomize number of attributes to combine
    #randomize which attributes to choose
    numObject = random.randint(1, 61)
    numEnvir = random.randint(1, 3)
    subjects = []
    objects = []
    envir = []
    attributeO = []
    attributeE = []

    randSubject = random.randint(0, 3)
    count = 0
    for aSubject in subjectAttributes.keys():
        if count == randSubject and count == 0:
            numSubject = random.randint(1, 100)
            for name in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 99)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 99)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        elif count == randSubject and count == 1:
            numSubject = random.randint(1, 11)
            for title in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 10)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 10)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        elif count == randSubject and count == 2:
            numSubject = random.randint(1, 4)
            for clearance in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 3)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 3)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        elif count == randSubject and count == 3:
            numSubject = random.randint(1, 100)
            for id in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 99)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 99)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        
    for object in range(numObject):
        resourcePair = getResource(attributeO)
        resource = objectAttributes[resourcePair[0]][resourcePair[1]] 
        objects.append(resource)
        attributeO.append(resourcePair)

    for envir in range(numEnvir):
        attribute = random.randint(0, 2)
        if attribute == 1:
            for pair in attributeE:
                if pair[0] == 1:
                    while attribute == 1:
                        attribute = random.randint(0, 2)
        if attribute == 0:
            randomTime = random.randint(0, 3)
            pair = [attribute, randomTime]
            while pair in attributeE:
                randomTime = random.randint(0, 3)
            attributeE.append(pair)
            envir.append(envirAttributes["time"][randomTime])
        elif attribute == 1:
            pair = [attribute, 0]
            attributeE.append(pair)
            envir.append(envirAttributes["date"])
        elif attribute == 2:
            randomLvl = random.randint(0, 2)
            pair = [attribute, randomLvl]
            while pair in attributeE:
                randomLvl = random.randint(0, 2)
            attributeE.append(pair)
            envir.append(envirAttributes["networkSec"][randomLvl])
        
    policyDict = {"model":"ABAC",
                  "subject attributes": subjects,
                  "object attributes": objects,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

elif model == 2:
    roleIndex = random.randint(0, 10)
    numResources = random.randint(1, 61)
    usedResources = []
    resources = []
    for object in range(numResources):
        resourcePair = getResource(usedResources)
        resource = objectAttributes[resourcePair[0]][resourcePair[1]] 
        resources.append(resource)
        usedResources.append(resourcePair)
    policyDict = {"model":"RBAC",
                  "role": roles[roleIndex],
                  "resources": resources}
    policy = json.dumps(policyDict)

elif model == 3:
    roleIndex = random.randint(0, 10)
    numTags = random.randint(1, 6)
    usedTags = []
    tag = []
    count = 0
    for randTag in range(numTags):
        tagIndex = random.randint(0, 5)
        while tagIndex in usedTags:
            tagIndex = random.randint(0, 5)
        for category in tags.keys():
            if count == tagIndex:
                tag.append(tags[category])
            count += 1
    policyDict = {"model":"CT-RBAC",
                  "role": roles[roleIndex],
                  "column tags": tag}
    policy = json.dumps(policyDict)

elif model == 4:
    numTags = random.randint(1, 6)
    numEnvir = random.randint(1, 3)
    subjects = []
    tag = []
    envir = []
    usedTags = []
    attributeE = []

    randSubject = random.randint(0, 3)
    count = 0
    for aSubject in subjectAttributes.keys():
        if count == randSubject and count == 0:
            numSubject = random.randint(1, 100)
            for name in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 99)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 99)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        elif count == randSubject and count == 1:
            numSubject = random.randint(1, 11)
            for title in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 10)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 10)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        elif count == randSubject and count == 2:
            numSubject = random.randint(1, 4)
            for clearance in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 3)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 3)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        elif count == randSubject and count == 3:
            numSubject = random.randint(1, 100)
            for id in range(numSubject):
                usedSubject = []
                randSubject2 = random.randint(0, 99)
                while randSubject2 in usedSubject:
                    randSubject2 = random.randint(0, 99)
                subjects.append(subjectAttributes[aSubject])
                usedSubject.append(randSubject2)
        
    count2 = 0
    for randTag in range(numTags):
        tagIndex = random.randint(0, 5)
        while tagIndex in usedTags:
            tagIndex = random.randint(0, 5)
        for category in tags.keys():
            if count == tagIndex:
                tag.append(tags[category])
            count2 += 1

    for envir in range(numEnvir):
        attribute = random.randint(0, 2)
        if attribute == 1:
            for pair in attributeE:
                if pair[0] == 1:
                    while attribute == 1:
                        attribute = random.randint(0, 2)
        if attribute == 0:
            randomTime = random.randint(0, 3)
            pair = [attribute, randomTime]
            while pair in attributeE:
                randomTime = random.randint(0, 3)
            attributeE.append(pair)
            envir.append(envirAttributes["time"][randomTime])
        elif attribute == 1:
            pair = [attribute, 0]
            attributeE.append(pair)
            envir.append(envirAttributes["date"])
        elif attribute == 2:
            randomLvl = random.randint(0, 2)
            pair = [attribute, randomLvl]
            while pair in attributeE:
                randomLvl = random.randint(0, 2)
            attributeE.append(pair)
            envir.append(envirAttributes["networkSec"][randomLvl])
    policyDict = {"model":"OT-ABAC",
                  "subject attributes": subjects,
                  "object tags": tag,
                  "environment attributes": envir}
    policy = json.dumps(policyDict)

elif model == 5:
    purposeIndex = random.randint(0, 5)
    count = 0
    purpose = None
    resources = None
    for key in purposes.keys():
        if count == purposeIndex:
            purpose = key
            resources = purposes[key]
        count += 1
    policyDict = {"model":"PBAC",
                  "purpose": purpose,
                  "resources": resources}
    policy = json.dumps(policyDict)

else:
    print("Invalid input, try again")

print(policy)