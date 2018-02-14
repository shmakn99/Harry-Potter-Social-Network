# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 02:24:14 2018

@author: Manik Sharma
"""

import re
import networkx as nx
#from matplotlib import pyplot as plt
import operator

def fix(lst,itm):
    lst.remove(itm)
    itm.reverse()
    lst.append(itm)
    return lst

def rank(dic,n):
    sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))
    sorted_dic.reverse()
    return(sorted_dic[:n])
    

def extrax(lst):
    ret=[]
    with open('TotChar.txt',encoding='utf-8') as f:
        p=re.compile('>(\w+) (\w+)</a> ')
        s=''  
        while True:
            s=f.readline()
            if s=='':
                break
            cht=''
            for m in p.finditer(s):
                cht=m.group().strip()
                ret.append(cht[1:len(cht)-4].upper())
                
    ret=list(set(ret))
    ret=[i.split() for i in ret]
    ret=sorted(ret,key=lambda x:x[0][0])
    fix(ret,['LUNA', 'LOVEGOOD'])
    fix(ret,['GELLERT', 'GRINDELWALD'])
    
    hp=''
    
    for i in lst:
        with open('HP'+str(i)+'.txt',encoding="utf-8") as f:
            hp+=f.read()

    p=re.compile('INT|EXT')
    scene=[]
    for m in p.finditer(hp[:]):
        scene.append(m.start()+3)
    
    return ret,scene,hp

def init(charax):
    ret={}
    for ci in charax:
        ret[ci[0]]=0
    return ret

def shorten(dic):
    return ({x:y for x,y in dic.items() if y!=0})

def update(G,dic):
    k=list(dic.keys())
    
    for i in range(len(k)):
        for j in range(i+1,len(k)):
            if (k[i],k[j]) in G.edges():
                G[k[i]][k[j]]['weight']+=(dic[k[i]]+dic[k[j]])
            else:
                G.add_edge(k[i],k[j],weight=0)
                G.add_edge(k[j],k[i],weight=(dic[k[i]]+dic[k[j]]))
    return G
        
def social_net(lst):
    #print (scene)
        
    net=nx.Graph()    
        
    characters,scene,script=extrax(lst)
    #print (extrax())
    i=0
    for j in scene:
    #    print (j)
        chr_frq=init(characters)
        for ci in characters:
            if len(re.findall(ci[0],script[i:j]))>0:
                chr_frq[ci[0]]+=len(re.findall(ci[0],script[i:j]))
                #print (i,ci,re.findall(ci[0],script[i:j]))
            else:
                if len(re.findall(ci[1],script[i:j]))>0 and ci[1]!='POTTER':
                    chr_frq[ci[0]]+=len(re.findall(ci[1],script[i:j]))
        net=update(net,shorten(chr_frq))
        i=j
        
    print (len(net.nodes()))
    print (len(net.edges()))
    
    return (net)

deg=nx.degree_centrality(social_net([2,3,4,5,6,71]))
#bet=nx.betweenness_centrality(social_net([2,3,4,5,6,71]))
#cls=nx.closeness_centrality(net)
#edg=nx.edge_betweenness_centrality(net)

#print (rank(deg,5))
print (rank(deg,20))