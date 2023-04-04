import pandas as pd
import re
def get_alias_or_not(res):
    if ' as ' in res.lower():
        index=res.lower().find(' as ')
        return res[index+4:]
    return res

sql="""SELECT CUS_GEN, count(*) as total, 
    round(count(*) * 100.0 / sum(count(*)) over(), 2) as percent
FROM data_sample
GROUP BY CUS_GEN"""
nb_rep = 1

index2=sql.rfind('FROM')
list_col=(sql[7:index2].split(', '))
headers=[]
for col in list_col:
    headers.append(get_alias_or_not(col))
print(headers)