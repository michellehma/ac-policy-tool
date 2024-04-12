from sqlalchemy import create_engine, text
import re

queryList = ["select l_returnflag, l_linestatus, sum(l_quantity) as sum_qty, sum(l_extendedprice) as sum_base_price, sum(l_extendedprice*(1-l_discount)) as sum_disc_price, sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge, avg(l_quantity) as avg_qty, avg(l_extendedprice) as avg_price, avg(l_discount) as avg_disc, count(*) as count_order from business.lineitem where l_shipdate <= '1998-12-01' - interval 90 day group by l_returnflag, l_linestatus order by l_returnflag, l_linestatus",
             "select s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment from part, supplier, partsupp, nation, region where p_partkey = ps_partkey and s_suppkey = ps_suppkey and p_size = 15 and p_type like '%BRASS' and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'EUROPE' and ps_supplycost = ( select min(ps_supplycost) from partsupp, supplier, nation, region where p_partkey = ps_partkey and s_suppkey = ps_suppkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'EUROPE' ) order by s_acctbal desc, n_name, s_name, p_partkey limit 100;",
             "select l_orderkey, sum(l_extendedprice*(1-l_discount)) as revenue, o_orderdate, o_shippriority from customer, orders, lineitem where c_mktsegment = 'BUILDING' and c_custkey = o_custkey and l_orderkey = o_orderkey and o_orderdate < '1995-03-15' and l_shipdate > '1995-03-15' group by l_orderkey, o_orderdate, o_shippriority order by revenue desc, o_orderdate limit 10;",
             "select o_orderpriority, count(*) as order_count from orders where o_orderdate >= '1993-07-01' and o_orderdate < '1993-07-01' + interval 3 month and exists ( select * from lineitem where l_orderkey = o_orderkey and l_commitdate < l_receiptdate ) group by o_orderpriority order by o_orderpriority;",
             "select n_name, sum(l_extendedprice * (1 - l_discount)) as revenue from customer, orders, lineitem, supplier, nation, region where c_custkey = o_custkey and l_orderkey = o_orderkey and l_suppkey = s_suppkey and c_nationkey = s_nationkey and s_nationkey = n_nationkey and n_regionkey = r_regionkey and r_name = 'ASIA' and o_orderdate >= '1994-01-01' and o_orderdate < '1994-01-01' + interval 1 year group by n_name order by revenue desc;",
             "select sum(l_extendedprice*l_discount) as revenue from lineitem where l_shipdate >= '1994-01-01' and l_shipdate < '1994-01-01' + interval 1 year and l_discount between 0.06 - 0.01 and 0.06 + 0.01 and l_quantity < 24;",
             "select supp_nation, cust_nation, l_year, sum(volume) as revenue from ( select n1.n_name as supp_nation, n2.n_name as cust_nation, extract(year from l_shipdate) as l_year, l_extendedprice * (1 - l_discount) as volume from supplier, lineitem, orders, customer, nation n1, nation n2 where s_suppkey = l_suppkey and o_orderkey = l_orderkey and c_custkey = o_custkey and s_nationkey = n1.n_nationkey and c_nationkey = n2.n_nationkey and ( (n1.n_name = 'FRANCE' and n2.n_name = 'GERMANY') or (n1.n_name = 'GERMANY' and n2.n_name = 'FRANCE') ) and l_shipdate between '1995-01-01' and '1996-12-31' ) as shipping group by supp_nation, cust_nation, l_year order by supp_nation, cust_nation, l_year;",
             "select o_year, sum(case when nation = 'BRAZIL' then volume else 0 end) / sum(volume) as mkt_share from ( select extract(year from o_orderdate) as o_year, l_extendedprice * (1-l_discount) as volume, n2.n_name as nation from part, supplier, lineitem, orders, customer, nation n1, nation n2, region where p_partkey = l_partkey and s_suppkey = l_suppkey and l_orderkey = o_orderkey and o_custkey = c_custkey and c_nationkey = n1.n_nationkey and n1.n_regionkey = r_regionkey and r_name = 'AMERICA' and s_nationkey = n2.n_nationkey and o_orderdate between '1995-01-01' and '1996-12-31' and p_type = 'ECONOMY ANODIZED STEEL' ) as all_nations group by o_year order by o_year;",
             "select nation, o_year, sum(amount) as sum_profit from ( select n_name as nation, extract(year from o_orderdate) as o_year, l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount from part, supplier, lineitem, partsupp, orders, nation where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey and p_partkey = l_partkey and o_orderkey = l_orderkey and s_nationkey = n_nationkey and p_name like '%green%' ) as profit group by nation, o_year order by nation, o_year desc;",
             "select c_custkey, c_name, sum(l_extendedprice * (1 - l_discount)) as revenue, c_acctbal, n_name, c_address, c_phone, c_comment from customer, orders, lineitem, nation where c_custkey = o_custkey and l_orderkey = o_orderkey and o_orderdate >= '1993-10-01' and o_orderdate < '1993-10-01' + interval 3 month and l_returnflag = 'R' and c_nationkey = n_nationkey group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment order by revenue desc limit 20;",
             "select ps_partkey, sum(ps_supplycost * ps_availqty) as value from partsupp, supplier, nation where ps_suppkey = s_suppkey and s_nationkey = n_nationkey and n_name = 'GERMANY' group by ps_partkey having sum(ps_supplycost * ps_availqty) > ( select sum(ps_supplycost * ps_availqty) * 0.0001 from partsupp, supplier, nation where ps_suppkey = s_suppkey and s_nationkey = n_nationkey and n_name = 'GERMANY' ) order by value desc;",
             "select l_shipmode, sum(case when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1 else 0 end) as high_line_count, sum(case when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1 else 0 end) as low_line_count from orders, lineitem where o_orderkey = l_orderkey and l_shipmode in ('MAIL', 'SHIP') and l_commitdate < l_receiptdate and l_shipdate < l_commitdate and l_receiptdate >= '1994-01-01' and l_receiptdate < '1994-01-01' + interval 1 year group by l_shipmode order by l_shipmode;",
             "select c_count, count(*) as custdist from ( select c_custkey, count(o_orderkey) from customer left outer join orders on c_custkey = o_custkey and o_comment not like '%special%requests%' group by c_custkey )as c_orders (c_custkey, c_count) group by c_count order by custdist desc, c_count desc;",
             "select 100.00 * sum(case when p_type like 'PROMO%' then l_extendedprice*(1-l_discount) else 0 end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue from lineitem, part where l_partkey = p_partkey and l_shipdate >= '1995-09-01' and l_shipdate < '1995-09-01' + interval 1 month;",
             "create view revenue0 (supplier_no, total_revenue) as select l_suppkey, sum(l_extendedprice * (1 - l_discount)) from lineitem where l_shipdate >= '1996-01-01' and l_shipdate < '1996-01-01' + interval 3 month group by l_suppkey; select s_suppkey, s_name, s_address, s_phone, total_revenue from supplier, revenue0 where s_suppkey = supplier_no and total_revenue = ( select max(total_revenue) from revenue0 ) order by s_suppkey; drop view revenue0;",
             "select p_brand, p_type, p_size, count(distinct ps_suppkey) as supplier_cnt from partsupp, part where p_partkey = ps_partkey and p_brand <> 'Brand#45' and p_type not like 'MEDIUM POLISHED%' and p_size in (49, 14, 23, 45, 19, 3, 36, 9) and ps_suppkey not in ( select s_suppkey from supplier where s_comment like '%Customer%Complaints%' ) group by p_brand, p_type, p_size order by supplier_cnt desc, p_brand, p_type, p_size;",
             "select sum(l_extendedprice) / 7.0 as avg_yearly from lineitem, part where p_partkey = l_partkey and p_brand = 'Brand#23' and p_container = 'MED BOX' and l_quantity < ( select 0.2 * avg(l_quantity) from lineitem where l_partkey = p_partkey );",
             "select c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) from customer, orders, lineitem where o_orderkey in ( select l_orderkey from lineitem group by l_orderkey having sum(l_quantity) > 300 ) and c_custkey = o_custkey and o_orderkey = l_orderkey group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice order by o_totalprice desc, o_orderdate limit 100;",
             "select sum(l_extendedprice * (1 - l_discount) ) as revenue from lineitem, part where ( p_partkey = l_partkey and p_brand = 'Brand#12' and p_container in ( 'SM CASE', 'SM BOX', 'SM PACK', 'SM PKG') and l_quantity >= 1 and l_quantity <= 1 + 10 and p_size between 1 and 5 and l_shipmode in ('AIR', 'AIR REG') and l_shipinstruct = 'DELIVER IN PERSON' ) or ( p_partkey = l_partkey and p_brand = 'Brand#23' and p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK') and l_quantity >= 10 and l_quantity <= 10 + 10 and p_size between 1 and 10 and l_shipmode in ('AIR', 'AIR REG') and l_shipinstruct = 'DELIVER IN PERSON' ) or ( p_partkey = l_partkey and p_brand = 'Brand#34' and p_container in ( 'LG CASE', 'LG BOX', 'LG PACK', 'LG PKG') and l_quantity >= 20 and l_quantity <= 20 + 10 and p_size between 1 and 15 and l_shipmode in ('AIR', 'AIR REG') and l_shipinstruct = 'DELIVER IN PERSON');",
             "select s_name, s_address from supplier, nation where s_suppkey in ( select ps_suppkey from partsupp where ps_partkey in ( select p_partkey from part where p_name like 'forest%' ) and ps_availqty > ( select 0.5 * sum(l_quantity) from lineitem where l_partkey = ps_partkey and l_suppkey = ps_suppkey and l_shipdate >= '1994-01-01' and l_shipdate < '1994-01-01' + interval 1 year ) ) and s_nationkey = n_nationkey and n_name = 'CANADA' order by s_name;",
             "select s_name, count(*) as numwait from supplier, lineitem l1, orders, nation where s_suppkey = l1.l_suppkey and o_orderkey = l1.l_orderkey and o_orderstatus = 'F' and l1.l_receiptdate > l1.l_commitdate and exists ( select * from lineitem l2 where l2.l_orderkey = l1.l_orderkey and l2.l_suppkey <> l1.l_suppkey ) and not exists ( select * from lineitem l3 where l3.l_orderkey = l1.l_orderkey and l3.l_suppkey <> l1.l_suppkey and l3.l_receiptdate > l3.l_commitdate ) and s_nationkey = n_nationkey and n_name = 'SAUDI ARABIA' group by s_name order by numwait desc, s_name limit 100;",
             "select cntrycode, count(*) as numcust, sum(c_acctbal) as totacctbal from ( select substring(c_phone from 1 for 2) as cntrycode, c_acctbal from customer where substring(c_phone from 1 for 2) in ('13','31','23','29','30','18','17') and c_acctbal > ( select avg(c_acctbal) from customer where c_acctbal > 0.00 and substring(c_phone from 1 for 2) in ('13','31','23','29','30','18','17') ) and not exists ( select * from orders where o_custkey = c_custkey ) ) as custsale group by cntrycode order by cntrycode;"]
permissionList = [["l_returnflag", "l_linestatus", "sum(l_quantity)", "sum(l_extendedprice)", "sum(l_discount)", "sum(l_tax)", "avg(l_quantity)", "avg(l_extendedprice)", "avg(l_discount)", "count(lineitem)"],
                  ["s_acctbal", "s_name", "n_name", "p_partkey", "p_mfgr", "s_address", "s_phone", "s_comment"],
                  ["l_orderkey", "sum(l_extendedprice)", "sum(l_discount)", "o_orderdate", "o_shippriority"],
                  ["o_orderpriority", "count(orders)"],
                  ["n_name", "sum(l_extendedprice)", "sum(l_discount)"],
                  ["sum(l_extendedprice)", "sum(l_discount)"],
                  ["n_name", "l_shipdate", "sum(l_extendedprice)", "sum(l_discount)"],
                  ["o_orderdate", "sum(l_extendedprice)", "sum(l_discount)"],
                  ["n_name", "o_orderdate", "sum(l_extendedprice)", "sum(l_discount)", "sum(ps_supplycost)", "sum(l_quantity)"],
                  ["c_custkey", "c_name", "sum(l_extendedprice)", "sum(l_discount)", "c_acctbal", "n_name", "c_address", "c_phone", "c_comment"],
                  ["ps_partkey", "sum(ps_supplycost)", "sum(ps_availqty)"],
                  ["l_shipmode", "sum(o_orderpriority)"],
                  ["c_count", "count(o_orderkey)", "count(c_custkey)"],
                  ["sum(p_type)", "sum(l_extendedprice)", "sum(l_discount)"],
                  ["l_suppkey", "sum(l_extendedprice)", "sum(l_discount)", "s_suppkey", "s_name", "s_address", "s_phone"],
                  ["p_brand", "p_type", "p_size", "count(ps_suppkey)"],
                  ["sum(l_extendedprice)"],
                  ["c_name", "c_custkey", "o_orderkey", "o_orderdate", "o_totalprice", "sum(l_quantity)"],
                  ["sum(l_extendedprice)", "sum(l_discount)"],
                  ["s_name", "s_address"],
                  ["s_name", "count(supplier)", "count(lineitem)", "count(orders)", "count(nation)"],
                  ["c_phone", "count(customer)", "sum(c_acctbal)"]]
selectList = [["l_returnflag, ", "l_linestatus, ", "sum(l_quantity) as sum_qty, ", "sum(l_extendedprice) as sum_base_price, sum(l_extendedprice*(1-l_discount)) as sum_disc_price, sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge, ", "sum(l_extendedprice*(1-l_discount)) as sum_disc_price, sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge, ", "sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge, ", "avg(l_quantity) as avg_qty, ", "avg(l_extendedprice) as avg_price, ", "avg(l_discount) as avg_disc, ", "count(*) as count_order "],
              ["s_acctbal, ", "s_name, ", "n_name, ", "p_partkey, ", "p_mfgr, ", "s_address, ", "s_phone, ", "s_comment "],
              ["l_orderkey, ", "sum(l_extendedprice*(1-l_discount)) as revenue, ", "sum(l_extendedprice*(1-l_discount)) as revenue, ", "o_orderdate, ", "o_shippriority "],
              ["o_orderpriority, ", "count(*) as order_count "],
              ["n_name, ", "sum(l_extendedprice * (1 - l_discount)) as revenue, ", "sum(l_extendedprice * (1 - l_discount)) as revenue "],
              ["sum(l_extendedprice * (1 - l_discount)) as revenue, ", "sum(l_extendedprice * (1 - l_discount)) as revenue "],
              ["supp_nation, cust_nation, ", "l_year, ", "sum(volume) as revenue ", "sum(volume) as revenue "],
              ["o_year, ", "sum(case when nation = 'BRAZIL' then volume else 0 end) / sum(volume) as mkt_share ", "sum(case when nation = 'BRAZIL' then volume else 0 end) / sum(volume) as mkt_share "],
              ["nation, ", "o_year, ", "sum(amount) as sum_profit ", "sum(amount) as sum_profit ", "sum(amount) as sum_profit ", "sum(amount) as sum_profit "],
              ["c_custkey, ", "c_name, ", "sum(l_extendedprice * (1 - l_discount)) as revenue, ", "sum(l_extendedprice * (1 - l_discount)) as revenue, ", "c_acctbal, ", "n_name, ", "c_address, ", "c_phone, ", "c_comment "],
              ["ps_partkey, ", "sum(ps_supplycost * ps_availqty) as value ", "sum(ps_supplycost * ps_availqty) as value "],
              ["l_shipmode, ", "sum(case when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1 else 0 end) as high_line_count, sum(case when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1 else 0 end) as low_line_count "],
              ["c_count, ", "count(*) as custdist ", "count(*) as custdist "],
              ["100.00 * sum(case when p_type like 'PROMO%' then l_extendedprice*(1-l_discount) else 0 end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue ", "100.00 * sum(case when p_type like 'PROMO%' then l_extendedprice*(1-l_discount) else 0 end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue ", "100.00 * sum(case when p_type like 'PROMO%' then l_extendedprice*(1-l_discount) else 0 end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue "],
              ["l_suppkey, ", "sum(l_extendedprice * (1 - l_discount)) ", "sum(l_extendedprice * (1 - l_discount)) ", "s_suppkey, ", "s_name, ", "s_address, ", "s_phone, ", "total_revenue "],
              ["p_brand, ", "p_type, ", "p_size, ", "count(distinct ps_suppkey) as supplier_cnt "],
              ["sum(l_extendedprice) / 7.0 as avg_yearly "],
              ["c_name, ", "c_custkey, ", "o_orderkey, ", "o_orderdate, ", "o_totalprice, ", "sum(l_quantity) "],
              ["sum(l_extendedprice * (1 - l_discount) ) as revenue ", "sum(l_extendedprice * (1 - l_discount) ) as revenue "],
              ["s_name, ", "s_address "],
              ["s_name, ", "count(*) as numwait ", "count(*) as numwait ", "count(*) as numwait ", "count(*) as numwait "],
              ["cntrycode, ", "count(*) as numcust, ", "sum(c_acctbal) as totacctbal "]]

#resultList = ["\nl_returnflag: {}  l_linestatus: {}  sum_qty: {}  sum_base: {}  \nsum_disc: {}  sum_charge: {}  avg_qty: {}  avg_price: {}  \navg_disc: {}  count: {}\n",]

engine1 = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/business", echo=True)

model = input("Enter number for access control model \n1. ABAC \n2. RBAC \n3. Contextual RBAC\n4. CT-RBAC \n5. OT-ABAC \n6. PBAC\n")
while model != '1' and model != '2' and model != '3' and model != '4' and model != '5' and model != '6':
    model = input("Enter number for access control model \n1. ABAC \n2. RBAC \n3. Contextual RBAC\n4. CT-RBAC \n5. OT-ABAC \n6. PBAC\n")
statement = ""
if model == '1':
    statement = "mysql+pymysql://root:root@127.0.0.1:3306/abac"
elif model == '2':
    statement = "mysql+pymysql://root:root@127.0.0.1:3306/rbac"
elif model == '3':
    statement = "mysql+pymysql://root:root@127.0.0.1:3306/crbac"
elif model == '4':
    statement = "mysql+pymysql://root:root@127.0.0.1:3306/ctrbac"
elif model == '5':
    statement = "mysql+pymysql://root:root@127.0.0.1:3306/otabac"
elif model == '6':
    statement = "mysql+pymysql://root:root@127.0.0.1:3306/pbac"

engine2 = create_engine(statement, echo=True)

def checkABAC(listCol):
    notAllowed = []
    allowed = ""
    with engine2.connect() as conn:
        subject = input("Enter subject: ")
        environment = input("Enter environment attributes (if more than one, separate with a comma and a space): ")
        query1 = "select s_attribute from s_assignment where s_name='{}'".format(subject)
        result1 = conn.execute(text(query1))
        setResult1 = set(result1)
        strResult1 = str(setResult1)
        strResult1 = strResult1.replace("{(", "").replace(",)}", "").replace(",)", "").replace(" (", "")
        listResult1 = strResult1.split(",")
        listResult2 = []
        listResult3 = environment.split(", ")

        for object in listCol:
            query2 = "select o_attribute from o_assignment where o_name='{}'".format(object)
            result2 = conn.execute(text(query2))
            setResult2 = set(result2)
            if setResult2:
                strResult2 = str(setResult2)
                strResult2 = strResult2.replace("{(", "").replace(",)}", "").replace(",)", "").replace(" (", "")
                list = strResult2.split(",")
                listResult2 = listResult2 + list

        if listResult1 and listResult2 and listResult3: 
            for s in range(len(listResult1)):
                for o in range(len(listResult2)):
                    for e in range(len(listResult3)):
                        if listResult1[s] and listResult2[o] and listResult3[e]:
                            query4 = "select p_name from p_assignment where s_attribute={} and o_attribute={} and e_attribute='{}'".format(listResult1[s], listResult2[o], listResult3[e])
                            result4 = conn.execute(text(query4))
                            setResult4 = set(result4)
                            if setResult4:
                                strResult4 = str(setResult4)
                                allowed = allowed + strResult4                            

            if allowed:
                print(allowed)
                for permission in listCol:
                    if permission not in allowed:
                        notAllowed.append(permission)
            else:
                return listCol
        else:
            return listCol
    return notAllowed

def checkRBAC(listCol):
    notAllowed = []
    with engine2.connect() as conn:
        user = input("Enter your user/name: ")
        query2 = "select r_name from assignment where u_name='{}'".format(user)
        result2 = conn.execute(text(query2))
        setResult2 = set(result2)
        if setResult2:
            query3 = "select p_name from role_permission where"
            count = 0
            for r in setResult2:
                r2 = str(r)
                r2 = re.sub('[(),]', '', r2)
                if count == 0:
                    query3 = query3 + " r_name={}".format(r2)
                else:
                    query3 = query3 + ", r_name={}".format(r2)
                count += 1
            result3 = conn.execute(text(query3))
            setResult3 = set(result3)

            if setResult3:
                strResult3 = str(setResult3)
                for permission in listCol:
                    if permission not in strResult3:
                        notAllowed.append(permission)
            else:
                return listCol
        else:
            return listCol
    return notAllowed

def checkCRBAC(listCol):
    return []

def checkCTRBAC(listCol):
    return []

def checkOTABAC(listCol):
    return []

#NOT FINISHED YET
def checkPBAC(listCol):
    notAllowed = []
    with engine2.connect() as conn:
        query = "select p_name from p_assignment where p_attribute='{}'".format()
        return
    return []

def getNotAllowed(model, listCol):
    if model == '1':
        return checkABAC(listCol)
    elif model == '2':
        return checkRBAC(listCol)
    elif model == '3':
        return checkCRBAC(listCol)
    elif model == '4':
        return checkCTRBAC(listCol)
    elif model == '5':
        return checkOTABAC(listCol)
    elif model == '6':
        return checkPBAC(listCol)
    else:
        return []

#run without access control
def run():
    with engine1.connect() as conn:
        for i in range(22):       
            result = conn.execute(text(queryList[i]))
            print(f"\nQUERY NUMBER: {i + 1}")
            count = 0
            for row in result:
                print(row)
                count += 1
            print(f"\nNUMBER OF ROWS RETURNED: {count}\n")

#run with access control
def runAC():
    with engine1.connect() as conn:
        for i in range(12, 13):
            if i == 14:
                notAllowed = getNotAllowed(model, permissionList[i])
                if notAllowed:
                    newQuery = queryList[i]
                    for x in range(len(permissionList[i])):
                        if permissionList[i][x] in notAllowed and selectList[i][x] in newQuery:
                            newQuery = newQuery.replace(selectList[i][x], "", 1)
                            print(newQuery)
                    if "sum(l_extendedprice * (1 - l_discount)) " not in newQuery:
                        newQuery = newQuery.replace(selectList[i][7], "", 1)
                        newQuery = newQuery.replace(", total_revenue", "", 1)
                        newQuery = newQuery.replace("and total_revenue = ( select max(total_revenue) from revenue0 )", "", 1)
                        print(newQuery)
                    if "l_suppkey, " not in newQuery:
                        newQuery = newQuery.replace("supplier_no, ", "", 1)
                        newQuery = newQuery.replace(" group by l_suppkey;", ";", 1)
                        newQuery = newQuery.replace("s_suppkey = supplier_no and ", "", 1)
                    newQueryList = list(newQuery)
                    if newQuery[newQuery.index("from")-2] == ",":
                        newQueryList[newQuery.index("from")-2] = ""
                    newQuery = "".join(newQueryList)
                    if newQuery.index("from") - newQuery.index("select") == 7:
                        print("You do not have permission to make that query")
                    else:
                        splitQuery = newQuery.split("; ")
                        print(splitQuery)
                        result = conn.execute(text(splitQuery[0]))
                        result2 = conn.execute(text(splitQuery[1]))
                        print(f"\nQUERY NUMBER: {i + 1}")
                        count1 = 0
                        for row in result2:
                            print(row)
                            count1 += 1
                        print(f"\nNUMBER OF ROWS RETURNED: {count1}\n")
                        conn.execute(text(splitQuery[2]))
                        conn.commit()
                else:
                    result = conn.execute(text("create view revenue0 (supplier_no, total_revenue) as select l_suppkey, sum(l_extendedprice * (1 - l_discount)) from lineitem where l_shipdate >= '1996-01-01' and l_shipdate < '1996-01-01' + interval 3 month group by l_suppkey;"))
                    result2 = conn.execute(text("select s_suppkey, s_name, s_address, s_phone, total_revenue from supplier, revenue0 where s_suppkey = supplier_no and total_revenue = ( select max(total_revenue) from revenue0 ) order by s_suppkey;"))
                    print(f"\nQUERY NUMBER: {i + 1}")
                    count = 0
                    for row in result2:
                        print(row)
                        count += 1
                    print(f"\nNUMBER OF ROWS RETURNED: {count}\n")
                    conn.execute(text("drop view revenue0;"))
                    conn.commit()
            else:
                notAllowed = getNotAllowed(model, permissionList[i])
                print(notAllowed)
                if notAllowed:
                    newQuery = queryList[i]
                    for x in range(len(permissionList[i])):
                        if permissionList[i][x] in notAllowed and selectList[i][x] in newQuery:
                            newQuery = newQuery.replace(selectList[i][x], "", 1)
                            print(newQuery)
                    newQueryList = list(newQuery)
                    if newQuery[newQuery.index("from")-2] == ",":
                        newQueryList[newQuery.index("from")-2] = ""
                    newQuery = "".join(newQueryList)
                    if newQuery.index("from") - newQuery.index("select") == 7:
                        print("You do not have permission to make that query")
                    else:
                        if (i == 4 or i == 9) and "sum(l_extendedprice * (1 - l_discount)) as revenue" not in newQuery:
                            newQuery = newQuery.replace(" order by revenue desc", "", 1)
                        elif (i == 2) and "sum(l_extendedprice * (1 - l_discount)) as revenue" not in newQuery:
                             newQuery = newQuery.replace(" revenue desc,", "", 1)
                        elif (i == 10) and "sum(ps_supplycost * ps_availqty) as value" not in newQuery:
                            newQuery = newQuery.replace(" order by value desc", "", 1)
                        elif (i == 12) and "count(*) as custdist" not in newQuery:
                            newQuery = newQuery.replace(" custdist desc,", "", 1)
                        elif (i == 15) and "count(distinct ps_suppkey) as supplier_cnt" not in newQuery:
                            newQuery = newQuery.replace(" supplier_cnt desc,", "", 1)
                        elif (i == 20) and "count(*) as numwait" not in newQuery:
                            newQuery = newQuery.replace(" numwait desc,", "", 1)
                        result = conn.execute(text(newQuery))
                        print(f"\nQUERY NUMBER: {i + 1}")
                        count1 = 0
                        for row in result:
                            print(row)
                            count1 += 1
                        print(f"\nNUMBER OF ROWS RETURNED: {count1}\n")

                else:
                    result = conn.execute(text(queryList[i]))
                    print(f"\nQUERY NUMBER: {i + 1}")
                    count = 0
                    for row in result:
                        print(row)
                        count += 1
                    print(f"\nNUMBER OF ROWS RETURNED: {count}\n")


runAC()
