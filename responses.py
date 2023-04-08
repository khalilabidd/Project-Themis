import pandas as pd
from settings import RESPONSES_URL
from random import randint

def handle_response(ref,default_response=''):
    df = pd.read_csv(RESPONSES_URL)
    df = df[df['Reference']==ref]
    df = df.fillna('')
    if len(df) and (message := df['Message'].iloc[randint(0,len(df)-1)]):
        return message
    return default_response
        