#!/usr/bin/env python
# coding: utf-8

# In[21]:


import whois
domain =whois.whois('facebook.com')


# In[22]:


print(domain)


# In[14]:


import datetime
now=datetime.datetime.now()
## Define Upated Date Function
def get_updated_date(sample):
    try:
            whoistuple=whois.whois(sample)
            if whoistuple['updated_date'] is None:
                return 0
            else:
                if type(whoistuple["updated_date"]) is list:
                    d1=whoistuple["updated_date"][0]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    return (d2-d1).days
                elif type(whoistuple["updated_date"]) is datetime.datetime:
                    d1=whoistuple["updated_date"]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    return (d2-d1).days
                else:
                    return 0                       
    except (whois.parser.PywhoisError, whois.parser.ConnectionResetError,whois.parser.KeyError):
        print("No data Available For: " + sample)
        return 0
    except (socket.gaierror):
        print("No data Available For : " + sample)
        return 0


# In[17]:


## Define Created Date Function
def get_created_date(sample):
    try:
            whoistuple=whois.whois(sample)
            if whoistuple['creation_date'] is None:
                return 0
            else:
                if type(whoistuple["creation_date"]) is list:
                    d1=whoistuple["creation_date"][0]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    return (d2-d1).days
                elif type(whoistuple["creation_date"]) is datetime.datetime:
                    d1=whoistuple["creation_date"]
                    d2=datetime.datetime.strptime(now.strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')
                    return (d2-d1).days
                else:
                    return 0                       
    except (whois.parser.PywhoisError, whois.parser.ConnectionResetError,whois.parser.KeyError):
        print("No data Available For: " + sample)
        return 0
    except (socket.gaierror):
        print("No data Available For : " + sample)
        return 0


# In[18]:


print(get_created_date('google.com'))


# In[19]:


## Has Registar 
def has_registrar(sample):
    try:
        whoistuple=whois.whois(sample)
        if whoistuple["registrar"] is None:
            return 0
        else:
            return 1
    except (whois.parser.PywhoisError, whois.parser.ConnectionResetError,whois.parser.KeyError):
        print("No data : " + str(i))
        return 0
    except (socket.gaierror):
        print("No data : " + str(i))
        return 0


# In[20]:


print(has_registrar('google.com'))


# In[23]:


## Email Server Server Attached  
def check_email(sample):
    try:
        whoistuple=whois.whois(sample)
        if whoistuple["emails"] is None:
            return 0
        else:
            return 1
    except (whois.parser.PywhoisError, whois.parser.ConnectionResetError,whois.parser.KeyError):
        print("No data : " + str(i))
        return 0
    except (socket.gaierror):
        print("No data : " + str(i))
        return 0


# In[24]:


print(check_email('google.com'))


# In[25]:


print(check_email('syhbih.com'))


# In[ ]:




