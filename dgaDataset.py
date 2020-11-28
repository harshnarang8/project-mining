import pandas as pd
from zxcvbn import zxcvbn

header_list=["DGA_Family","Domain","Start","End"]

df1=pd.read_csv("DGA_Netlab360.txt", sep="\t",comment='#',header=None,names=header_list)

data=[]

columns=["Domain", "Start", "End","guesses","matched_word","calc_time","score","feedback_warning"]

for index,row in df1.iloc[0:202257].iterrows():
    domain=row["Domain"]
    
    start=row["Start"]
    end=row["End"]
    
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
dataframe.to_csv("dgaDataset.csv",index=False)