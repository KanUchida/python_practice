import sys
import MeCab
import math


def freq_vector(x,y,freq):
    vector.setdefault(x, {})[y] = freq

def colocation(v1,v2):
    return sum(v1[i]+v2[i]-1 for i in v1 if i in v2)

def sim_cos(v1,v2):
    inner = sum(v1[i]*v2[i] for i in v1 if i in v2)
    denominator = math.sqrt(sum(v1[i]**2 for i in v1)*sum(v2[j]**2 for j in v2))
    return float(inner/denominator) if denominator !=0 else 0

def sim_simpson(v1,v2):
    numerator = sum(i in v1 for i in v2)
    denominator = min(len(v1), len(v2))
    return float(numerator/denominator) if denominator !=0 else 0

accep_f=['感動詞','形容詞','動詞','名詞','未知語','フィラー']
accep_d=['サ変接続','一般','自立']

text=open('text.txt','r')
m = MeCab.Tagger('')

for line in text:
    node = m.parseToNode(line)
    id_doc+=1
    
    while node:
        N+=1
        if(node.feature.split(",")[0] in accep_f and
              node.feature.split(",")[1] in accep_d):
            freq_vector(node.surface,id_doc,line.count(node.surface))
        node=node.next
