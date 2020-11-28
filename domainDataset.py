import pandas as pd
from zxcvbn import zxcvbn

df=pd.read_csv("top10milliondomains.csv")

data=[]

columns=["Domain", "Start", "End","guesses","matched_word","calc_time","score","feedback_warning"]

for index,row in df.iloc[0:9999999].iterrows():
    domain=row["Domain"]
    
    start=""
    end=""
    
    result=zxcvbn(domain)
    
    guesses=result["guesses"]
    
    if "matched_word" in result["sequence"][0]:
        matchedword=result["sequence"][0]["matched_word"]
    else:
        matchedword=""
        
        
    calc_time=result["calc_time"]
    score=result["score"]
    warning=result["feedback"]["warning"]
    data.append([domain,start,end,guesses,matchedword,calc_time,score,warning])
       
dataframe = pd.DataFrame(data, columns=["Domain", "Start", "End","guesses","matched_word","calc_time","score","feedback_warning"])  

dataframe.to_csv("domainDataset.csv",index=False)