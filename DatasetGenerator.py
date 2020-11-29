#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
from zxcvbn import zxcvbn
import math
from collections import Counter
import statistics
import whois
from socket import *
import datetime


# In[42]:


df1=pd.read_csv("top10milliondomains.csv")


# In[43]:


df1


# In[17]:


####### No of characters #######
def fnd_nch(strn):
    return len(strn)

#fnd_nch("google.com")



###### Entropy Calculation ######
import math
from collections import Counter

def entropy(s):
     p, lns = Counter(s), float(len(s))
     return -sum( count/lns * math.log(count/lns, 2) for count in p.values())
 
#entropy("00")


######## Unique Characters in a String ####
def Uchar(s):
    return len(set(s))

#Uchar("google.com")



####### No of Consonants #######
def ConCount(str):
    vowels = 0
    digits = 0
    consonants = 0
    spaces = 0
    symbols = 0
    str = str.lower()
    for i in range(0, len(str)):
        if(str[i] == 'a' or str[i] == 'e' or str[i] == 'i' or str[i] == 'o' or str[i] == 'u'):
            vowels = vowels + 1
        elif((str[i] >= 'a' and str[i] <= 'z')):
            consonants = consonants + 1
        elif( str[i] >= '0' and str[i] <= '9'):
            digits = digits + 1
        elif (str[i] ==' '):
            spaces = spaces + 1
        else:
            symbols = symbols + 1
    return consonants
            

#ConCount("aeiou")



####### No of Vowels #######

def VowCount(s):
    vowels = 0
    consonants = 0
    for i in s:
        if(i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u' or i == 'A' or i == 'E' or i == 'I' or i == 'O' or i == 'U'):
            vowels = vowels + 1
        else:
            consonants = consonants + 1
    return vowels
            

#VowCount("aeiou")


####### No of special characters #######
def SpCount(s):
    schar = 0
    for i in s:
        if(i == '_' or i == '-' or i == '.'):
            schar = schar + 1
    return schar
            

#SpCount("ae-iou.com")


####### No of Numericals characters #######
def NCount(s):
    Num = 0
    for i in s:
        if(i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i=='9'):
            Num = Num + 1
    return Num
            

#NCount("ae-i12ou.com")


##### Count of N-gram Occurences ####
def CountNgram(b,n):
    lst=[b[i:i+n] for i in range(len(b)-n+1)]
    res=dict((x,lst.count(x)) for x in set(lst))
    return res
#CountNgram("google.com",3)


###### Getting Mean for 1-Gram Occurences ##### 
def getmean1(s):
    ng1_result=CountNgram(s,1)
    mean1 = sum(ng1_result.values()) / len(ng1_result)  
    return mean1  

#getmean1("facebook.com")


###### Getting Variance for 1-Gram Occurences ##### 
import statistics
def getvar1(s):
    ng1_result=CountNgram(s,1)
    ng1_result_list = list(ng1_result.values()) ## Storing values of dictionary in python list format
    return statistics.variance(ng1_result_list)

#getvar1("facebook.com")


###### Getting Standard Deviation for 1-Gram Occurences ##### 
import statistics
def getstdev1(s):
    ng1_result=CountNgram(s,1)
    ng1_result_list = list(ng1_result.values()) ## Storing values of dictionary in python list format
    return statistics.stdev(ng1_result_list)

#getstdev1("facebook.com")


###### Getting Mean for 2-Gram Occurences ##### 
def getmean2(s):
    ng2_result=CountNgram(s,2)
    ng2_result_list=list(ng2_result.values())
    return statistics.mean(ng2_result_list)  

#getmean2("abab")


###### Getting Variance for 2-Gram Occurences ##### 
def getvar2(s):
    ng2_result=CountNgram(s,2)
    ng2_result_list=list(ng2_result.values())
    return statistics.variance(ng2_result_list)  

#getvar2("facebook.com")


###### Getting Standard Deviation for 2-Gram Occurences ##### 
def getstdev2(s):
    ng2_result=CountNgram(s,2)
    ng2_result_list=list(ng2_result.values())
    return statistics.stdev(ng2_result_list)  

#getstdev2("facebook.com")



def listToString(s):  
    str1 = " "  
    return (str1.join(s))

def removesp(string): 
    return "".join(string.split())

import re
def masknames(s):
    strings=s
    cs=listToString([re.sub("b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|x|z|y|w", "c", x) for x in strings])
    str1=removesp(cs)
    #print(str1)
    cs=listToString([re.sub("a|e|i|o|u", "v", x) for x in str1])
    str2=removesp(cs)
    #print(str2)
    cs=listToString([re.sub("0|1|2|3|4|5|6|7|8|9", "n", x) for x in str2])
    str3=removesp(cs)
    #print(str3)
    cs=listToString([re.sub("\\.|\\-|\\_", "s", x) for x in str3])
    str4=removesp(cs)
    return str4



############# cc #########
def get_cc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['cc'])
    except: 
        return(0)

#get_cc("bcd")


############# cv #########
def get_cv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['cv'])
    except: 
        return(0)

#get_cv("bacd")


############# vc #########
def get_vc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['vc'])
    except: 
        return(0)

#get_vc("abacd")



############# vv #########
def get_vv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['vv'])
    except: 
        return(0)

#get_vv("abacd")



############# nc #########
def get_nc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['nc'])
    except: 
        return(0)

#get_nc("a9bacd")



############# cn #########
def get_cn(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['cn'])
    except: 
        return(0)

#get_cn("a9b8acd")


############# sc #########
def get_sc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['sc'])
    except: 
        return(0)

#get_sc("a9b8a.cd")



############# cs #########
def get_cs(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['cs'])
    except: 
        return(0)

#get_sc("a9b8ab.cd")


############# nv #########
def get_nv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['nv'])
    except: 
        return(0)

#get_nv("a9b8ab.cd")


############# vn #########
def get_vn(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,2)
    try:
        return(nres['vn'])
    except: 
        return(0)

#get_vn("a9b8ab.cd")


############# ccc #########
def get_ccc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['ccc'])
    except: 
        return(0)

#get_ccc("cdr")


############# ccc #########
def get_ccc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['ccc'])
    except: 
        return(0)

#get_ccc("cdr")



############# cvc #########
def get_cvc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['cvc'])
    except: 
        return(0)

#get_cvc("car")



############# vcc #########
def get_vcc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['vcc'])
    except: 
        return(0)

#get_vcc("adr")



############# vcv #########
def get_vcv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['vcv'])
    except: 
        return(0)

#get_vcv("aca")


############# ccv #########
def get_ccv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['ccv'])
    except: 
        return(0)

#get_ccv("cda")


############# vvv #########
def get_vvv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['vvv'])
    except: 
        return(0)

#get_vvv("aaa")


############# cvv #########
def get_cvv(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['cvv'])
    except: 
        return(0)

#get_cvv("caa")


############# vvc #########
def get_vvc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['vvc'])
    except: 
        return(0)

#get_vvc("aab")


############# ncc #########
def get_ncc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['ncc'])
    except: 
        return(0)

#get_ncc("9fb")


############# nvc #########
def get_nvc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['nvc'])
    except: 
        return(0)

#get_nvc("9ab")


############# csc #########
def get_csc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['csc'])
    except: 
        return(0)

#get_csc("b.v")


############# cnc #########
def get_cnc(s):
    Mstring=masknames(s)
    nres=CountNgram(Mstring,3)
    try:
        return(nres['cnc'])
    except: 
        return(0)

#get_cnc("t9b")


# In[18]:


### Benign Dataset Generation
data=[]

columns=["Domain","guesses","matched_word","calc_time","score","feedback_warning","nch","entropy","Uchar","ConCount","VowCount","SpCount","NCount","mean1","var1","sd1","mean2","var2","sd2","cc","cv","vc","vv","nc","cn","sc","cs","nv","vn","ccc","cvc","vcc","vcv","ccv","vvv","cvv","vvc","ncc","nvc","csc","cnc"]

for index,row in df1.iloc[0:199999].iterrows():
    print(index)
    domain=row["Domain"]
    result=zxcvbn(domain)
    guesses=result["guesses"]
    if "matched_word" in result["sequence"][0]:
        matchedword=result["sequence"][0]["matched_word"]
    else:
        matchedword=""    
    calc_time=result["calc_time"]
    score=result["score"]
    warning=result["feedback"]["warning"]
    s=domain
    data.append([domain,guesses,matchedword,calc_time,score,warning,fnd_nch(s),entropy(s),Uchar(s),ConCount(s),VowCount(s),SpCount(s),NCount(s),getmean1(s),getvar1(s),getstdev1(s),getmean2(s),getvar2(s),getstdev2(s),get_cc(s),get_cv(s),get_vc(s),get_vv(s),get_nc(s),get_cn(s),get_sc(s),get_cs(s),get_nv(s),get_vn(s),get_ccc(s),get_cvc(s),get_vcc(s),get_vcv(s),get_ccv(s),get_vvv(s),get_cvv(s),get_vvc(s),get_ncc(s),get_nvc(s),get_csc(s),get_cnc(s)])
       
            


# In[19]:


dataframe = pd.DataFrame(data, columns=["Domain","guesses","matched_word","calc_time","score","feedback_warning","nch","entropy","Uchar","ConCount","VowCount","SpCount","NCount","mean1","var1","sd1","mean2","var2","sd2","cc","cv","vc","vv","nc","cn","sc","cs","nv","vn","ccc","cvc","vcc","vcv","ccv","vvv","cvv","vvc","ncc","nvc","csc","cnc"])  
dataframe.to_csv("benign2lakh.csv",index=False)


# In[44]:


#### DGA Domain Names
header_list=["DGA_Family","Domain","Start","End"]
df2=pd.read_csv("DGA_Netlab360.txt", sep="\t",comment='#',header=None,names=header_list)


# In[24]:


### DGA Dataset Generation
data=[]

columns=["Domain","guesses","matched_word","calc_time","score","feedback_warning","nch","entropy","Uchar","ConCount","VowCount","SpCount","NCount","mean1","var1","sd1","mean2","var2","sd2","cc","cv","vc","vv","nc","cn","sc","cs","nv","vn","ccc","cvc","vcc","vcv","ccv","vvv","cvv","vvc","ncc","nvc","csc","cnc"]

for index,row in df2.iloc[0:199999].iterrows():
    print(index)
    domain=row["Domain"]
    result=zxcvbn(domain)
    guesses=result["guesses"]
    if "matched_word" in result["sequence"][0]:
        matchedword=result["sequence"][0]["matched_word"]
    else:
        matchedword=""    
    calc_time=result["calc_time"]
    score=result["score"]
    warning=result["feedback"]["warning"]
    s=domain
    data.append([domain,guesses,matchedword,calc_time,score,warning,fnd_nch(s),entropy(s),Uchar(s),ConCount(s),VowCount(s),SpCount(s),NCount(s),getmean1(s),getvar1(s),getstdev1(s),getmean2(s),getvar2(s),getstdev2(s),get_cc(s),get_cv(s),get_vc(s),get_vv(s),get_nc(s),get_cn(s),get_sc(s),get_cs(s),get_nv(s),get_vn(s),get_ccc(s),get_cvc(s),get_vcc(s),get_vcv(s),get_ccv(s),get_vvv(s),get_cvv(s),get_vvc(s),get_ncc(s),get_nvc(s),get_csc(s),get_cnc(s)])


# In[25]:


dataframe1 = pd.DataFrame(data, columns=["Domain","guesses","matched_word","calc_time","score","feedback_warning","nch","entropy","Uchar","ConCount","VowCount","SpCount","NCount","mean1","var1","sd1","mean2","var2","sd2","cc","cv","vc","vv","nc","cn","sc","cs","nv","vn","ccc","cvc","vcc","vcv","ccv","vvv","cvv","vvc","ncc","nvc","csc","cnc"])  
dataframe1.to_csv("dga2lakh.csv",index=False)


# In[ ]:


### who is for benign domain names
now=datetime.datetime.now()
dname = ['c'] *10000
list1 = [0] * 10000 #Updated date
list2 = [0] * 10000 #Created date
list3 = [0] * 10000 #registrar
list4 = [0] * 10000 #name
list5 = [0] * 10000 #address
list6 = [0] * 10000 #zipcode

for index,row in df1.iloc[0:9999].iterrows():
    print(index)
    try:
            sample=row["Domain"]
            dname[index]=sample
            whoistuple=whois.whois(sample)
            if whoistuple['updated_date'] is None:
                list1[index]=0
            else:
                if type(whoistuple["updated_date"]) is list:
                    d1=whoistuple["updated_date"][0]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    list1[index]=(d2-d1).days
                elif type(whoistuple["updated_date"]) is datetime.datetime:
                    d1=whoistuple["updated_date"]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    list1[index]=(d2-d1).days
                else:
                    list1[index]=0
                    
            if whoistuple['creation_date'] is None:
                list2[index]=0
            else:
                if type(whoistuple["creation_date"]) is list:
                    d1=whoistuple["creation_date"][0]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    if(type(d1) != str):
                        list2[index]=(d2-d1).days
                elif type(whoistuple["creation_date"]) is datetime.datetime:
                    d1=whoistuple["creation_date"]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    list2[index]=(d2-d1).days
                else:
                    list2[index]=0
                    
            if whoistuple["registrar"] is None:
                list3[index]=0
            else:
                list3[index]=1
            
            if whoistuple["name"] is None:
                list4[index]=0
            else:
                list4[index]=1
            
            if whoistuple["address"] is None:
                list5[index]=0
            else:
                list5[index]=1
            
            if whoistuple["zipcode"] is None:
                list6[index]=0
            else:
                list6[index]=1
                
    except (whois.parser.PywhoisError,whois.parser.KeyError):
        continue
    except(whois.parser.ConnectionResetError,socket.gaierror,socket.error):
        index=index-1
        
benignwhois = pd.DataFrame(list(zip(dname,list1,list2,list3,list4,list5,list6)), 
               columns =['Domain','UpdatedDate', 'CreatedDate','Registrar','name','address','zipcode']) 
benignwhois.to_csv("benignwhois.csv",index=False)

### who is for DGA domain names
now=datetime.datetime.now()
dname1 = ['c'] *10000
list11 = [0] * 10000 #Updated date
list21 = [0] * 10000 #Created date
list31 = [0] * 10000 #registrar
list41 = [0] * 10000 #name
list51 = [0] * 10000 #address
list61 = [0] * 10000 #zipcode

for index,row in df2.iloc[0:9999].iterrows():
    print(index)
    try:
            sample=row["Domain"]
            dname1[index]=sample
            whoistuple=whois.whois(sample)
            if whoistuple['updated_date'] is None:
                list11[index]=0
            else:
                if type(whoistuple["updated_date"]) is list:
                    d1=whoistuple["updated_date"][0]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    list11[index]=(d2-d1).days
                elif type(whoistuple["updated_date"]) is datetime.datetime:
                    d1=whoistuple["updated_date"]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    list11[index]=(d2-d1).days
                else:
                    list11[index]=0
                    
            if whoistuple['creation_date'] is None:
                list21[index]=0
            else:
                if type(whoistuple["creation_date"]) is list:
                    d1=whoistuple["creation_date"][0]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    if(type(d1) != str):
                        list21[index]=(d2-d1).days
                elif type(whoistuple["creation_date"]) is datetime.datetime:
                    d1=whoistuple["creation_date"]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    list21[index]=(d2-d1).days
                else:
                    list21[index]=0
                    
            if whoistuple["registrar"] is None:
                list31[index]=0
            else:
                list31[index]=1
            
            if whoistuple["name"] is None:
                list41[index]=0
            else:
                list41[index]=1
            
            if whoistuple["address"] is None:
                list51[index]=0
            else:
                list51[index]=1
            
            if whoistuple["zipcode"] is None:
                list61[index]=0
            else:
                list61[index]=1
                
    except (whois.parser.PywhoisError,whois.parser.KeyError):
        continue
    except(whois.parser.ConnectionResetError,socket.gaierror,socket.error):
        index=index-1

dgawhois = pd.DataFrame(list(zip(dname1,list11,list21,list31,list41,list51,list61)), 
               columns =['Domain','UpdatedDate', 'CreatedDate','Registrar','name','address','zipcode']) 
dgawhois.to_csv("dgawhois.csv",index=False)


# In[69]:


#list1


# In[70]:


#list2


# In[71]:


#list3


# In[72]:


#dname


# In[73]:


#list4


# In[74]:


#list5


# In[75]:


#list6


# In[54]:


#whois.whois("jbusvjp.org")


# In[55]:


#whois.whois("facebook.com")


# In[76]:


#benignwhois = pd.DataFrame(list(zip(dname,list1,list2,list3,list4,list5,list6)), 
#               columns =['Domain','UpdatedDate', 'CreatedDate','Registrar','name','address','zipcode']) 


# In[77]:


benignwhois


# In[ ]:




