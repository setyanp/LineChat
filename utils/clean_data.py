'''
CHAT DATA INTO CLEAN DATAFRAME
'''

import pandas as pd
import numpy as np
from dateutil.parser import parse
import datetime

class DataClean:
    def is_timeformat(self,string):
        try: 
            parse(string)
            return True
        except:
            return False

    def is_date(self,string):
        try:
            datetime.datetime.strptime(string, '%Y/%m/%d')
            return True
        except:
            return False
        
    def clean_dataframe(self,msg_data):
        list_delete = []
        list_day = ["(Sen)", "(Sel)", "(Rab)", "(Kam)", "(Jum)", "(Sab)", "(Min)"]
        last_date_loc = 0
        date_string = ''

        try:
            for x in range(len(msg_data)):
                temp_string = msg_data.iloc[x]['chat_time'].replace("24:", "00:")
                if any(y in temp_string for y in list_day):
                    for y in list_day:
                        temp_string = (temp_string).replace(y, "")

                if (self.is_timeformat(temp_string)==False):
                    msg_data.loc[last_date_loc, 'message'] += " " + temp_string
                    list_delete.append(x)
                else:
                    if (self.is_date(temp_string)==True):
                        list_delete.append(x)
                        date_string = temp_string
                    else:
                        last_date_loc = x
                        msg_data.loc[x, 'chat_time'] = (date_string + ' ' + temp_string)
            
            return msg_data.drop(list_delete).reset_index(drop=True)
            
        except Exception as e:
            print(e)