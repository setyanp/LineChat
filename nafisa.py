import pandas as pd
import numpy as np
import datetime
from utils.clean_data import DataClean
from utils.visualization import DrawFigure
import os

def count_question(msg_data,name_1,name_2):
    msg_data['chat_time'] = pd.to_datetime(msg_data['chat_time'])
    msg_data['?'] = msg_data['message'].str.contains("""[?]""").astype(int)
    qmarks_counter = msg_data.groupby([msg_data.chat_time.dt.strftime('%D'), 'name'])['?'].sum()\
            .reset_index()\
            .rename(columns={'?': 'total'})
    qmarks_counter['chat_time'] = pd.to_datetime(qmarks_counter['chat_time'])
    qmarks_counter['chat_time'] = qmarks_counter['chat_time'].dt.strftime('%Y-%m-%d')
    qmarks_counter = qmarks_counter.sort_values(by='chat_time',ascending=True)
    question_mark_total = [qmarks_counter[qmarks_counter['name'] == name_1].total.sum(),qmarks_counter[qmarks_counter['name'] == name_2].total.sum()]
    DrawFigure().vertical_bar_graph(question_mark_total,name_1,name_2,'TOTAL QUESTION MARK','#FFEA00','#FFAA00')

def total_message(msg_data,name_1,name_2):
    list_chat_len = [(name_1,len(msg_data[msg_data['name'] == name_1])),(name_2,len(msg_data[msg_data['name'] == name_2]))]
    DrawFigure().horizontal_bar_labels(list_chat_len, 'Jumlah Pesan', '#FFAA00')

def most_used_words(msg_data):
    remove_word = ["yg", "ga", "kan", "dan", "ya", "nan", "kalau", "aja", "ada", "di", 
               "itu", "sama", "ini", "tapi", "kalo", "(laugh)", "(haha)" , 
               "udah","mau", "juga", "bisa", "jadi", "yang", "d", "lagi",
              "with", "laughter", "(crying", "guy)", "kok", "iyaa", "iya", "gitu", "dia", "cha", "mas,",
              "icha", "dia", "[stiker]", "(tertawa)", "wkwkwk", "ke", "sih", "aku",
              "mas", "kamu", "tak", "(catface)", "dari", "apa", "cuman", "cha,", "tau", "kayak", "jangan",
              "(har", "har)", "kayaknya", "?", "wes", "wkwk,", "buat", "emang", "banget", "dulu", "yaa", "biar", "mereka", 
              "banyak", "mas?", "harus", "pake", "gak", "trus", "gimana", "nanti", "e", "bikin", "[foto]", "tadi", "cha?",
              "coba", "kita", "masih", "terus", "pak", "punya", "wkwk",':"',"._.","hahaa","pasti","pernah","orang","(sedih)","pas","tp",
              "padahal","ngga","bukan","soalnya","lebih","k","abis"] ## ADD NECESSARY STOP WORDS

    words_edit = pd.Series(' '.join(msg_data['message']).lower().split())
    words_edit = words_edit[words_edit != "nan"].reset_index(drop=True)

    words_edit = words_edit[~words_edit.isin(remove_word)]
    most_word = words_edit.value_counts()[:10][::-1]
    most_word_list = []

    for i in most_word.index:
        most_word_list.append((i,most_word[i]))

    DrawFigure().horizontal_bar_labels(most_word_list, 'Most Used Word', '#FFAA00')

def total_words(msg_data,name_1,name_2):
    total_words_user1 = len(pd.Series(' '.join(msg_data['message'][msg_data['name'] == name_1]).lower().split()))
    total_words_user2 = len(pd.Series(' '.join(msg_data['message'][msg_data['name'] == name_2]).lower().split()))
    data_total_words = [total_words_user1,total_words_user2]
    DrawFigure().vertical_bar_graph(data_total_words,name_1,name_2,'TOTAL WORDS','#00bcd4','#b2ebf2')

def count_by_period(msg_data,count_params,name_1,name_2):
    period_count_name1 = msg_data[msg_data['name'] == name_1].groupby(msg_data.chat_time.dt.to_period(count_params)).message.size()
    period_count_name1.index = period_count_name1.index.to_timestamp()
    period_count_name2 = msg_data[msg_data['name'] == name_2].groupby(msg_data.chat_time.dt.to_period(count_params)).message.size()
    period_count_name2.index = period_count_name2.index.to_timestamp()

    if count_params in ("W","D"):
        objek1 = list(period_count_name1.index)
        objek2 = list(period_count_name2.index)
        not_in_name_1 = [x for x in objek2 if x not in objek1]
        not_in_name_2 = [x for x in objek1 if x not in objek2]
        for x in range(len(not_in_name_1)):
            period_count_name1.loc[not_in_name_1[x]] = 0
        
        for x in range(len(not_in_name_2)):
            period_count_name2.loc[not_in_name_2[x]] = 0

        period_count_name1.sort_index(inplace=True)
        period_count_name2.sort_index(inplace=True)
    
    periodically_dataframe = pd.DataFrame(period_count_name1).reset_index()
    periodically_dataframe.columns = ['chat_time','total_name1']
    periodically_dataframe['total_name2'] = period_count_name2.values

    stacked_bar_title = ''
    if count_params == "W":
        stacked_bar_title = 'WEEKLY MESSAGES COUNT'
    elif count_params == "D":
        stacked_bar_title = 'DAILY MESSAGES COUNT'
    elif count_params == "M":
        stacked_bar_title = 'MONTHLY MESSAGES COUNT'
    elif count_params == "Y":
        stacked_bar_title = 'ANNUAL MESSAGES COUNT'

    DrawFigure().stacked_bar(periodically_dataframe,name_1,name_2,stacked_bar_title,'#00bcd4','#FFAA00')

if __name__ == '__main__':
    #Open file and cleaning data
    filename = 'sample_text.txt' #change into f
    msg_data = pd.read_csv(filename, sep="\t", header=None, names=['chat_time','name','message']).applymap(str)
    msg_data = DataClean().clean_dataframe(msg_data)

    #Create Folder images if not exist
    if not os.path.exists('images'):
        os.makedirs('images')

    #Get User Name
    list_name = msg_data.name.unique()
    name_1 = list_name[0]
    name_2 = list_name[1]

    count_question(msg_data,name_1,name_2)
    total_message(msg_data,name_1,name_2)
    most_used_words(msg_data)
    total_words(msg_data,name_1,name_2)

    count_params = "M" # W:  D: daily, Weekly, M: monthly, Y: yearly
    count_by_period(msg_data,count_params,name_1,name_2)