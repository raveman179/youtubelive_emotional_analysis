from mlask import MLAsk
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import csv
from datetime import datetime, timedelta
import re

from pprint import pprint

pd.set_option('display.max_rows', None)
filepath = "/home/masaraveman/Documents/lang_learning/python/emotest/comment_zCK_490ryjg.txt"

with open(filepath, mode="r", encoding="UTF-8", errors="", newline="") as f:
    lst = csv.reader(f, delimiter=",")
    df = pd.DataFrame(lst, columns=['datetime', 'author_name', 'm1', 'm2', 'm3', 'm4'])
    

df["message"] = df["m1"]+df["m2"].fillna("")+df["m3"].fillna("")+df["m4"].fillna("")
df.drop(['m1', 'm2', 'm3', 'm4'], axis=1, inplace=True)

playtime = df["datetime"].values.tolist()
elapsed = []

for t in range(len(playtime)):
    dt1 = datetime.strptime(playtime[t], '%Y-%m-%d %H:%M:%S')
    dt2 = datetime.strptime(playtime[0], '%Y-%m-%d %H:%M:%S')
    td = dt2 - dt1
    elapsed.append(abs(td.total_seconds()))

elap = pd.Series(elapsed, name="elapsedtime")
message = df["message"]

# 接頭辞　:_kizunaai
# haroha,haroro,harooo,harobikuri 連結でハロー絵文字
custom_emoji = {'Hai':{'orientation': 'NEUTRAL', 'representative':'None'},\
                'Doumo':{'orientation': 'NEUTRAL', 'representative':'None'},\
               'Yabami':{'orientation': 'POSITIVE', 'representative':'takaburi'},\
               'Wakkyu':{'orientation': 'NEGATIVE', 'representative':'ikari'},\
               'Pyokopyoko':{'orientation': 'POSITIVE', 'representative':'yorokobi'},\
               'Aikawa':{'orientation': 'POSITIVE', 'representative':'suki'},\
               'Penlight1':{'orientation': 'NEUTRAL', 'representative':'None'},\
               'Aikawa':{'orientation': 'POSITIVE', 'representative':'suki'},\
               'Doya':{'orientation': 'POSITIVE', 'representative':'takaburi'},\
               'Pan':{'orientation': 'NEUTRAL', 'representative':'None'},\
               'Hawawa':{'orientation': 'NEGATIVE', 'representative':'haji'},\
               'Life':{'orientation': 'NEUTRAL', 'representative':'None'},\
               'Wow2':{'orientation': 'POSITIVE', 'representative':'yorokobi'},\
               'Haa':{'orientation': 'NEGATIVE', 'representative':'ikari'},\
               'Eee':{'orientation': 'POSITIVE', 'representative':'odoroki'},\
               'Kusa':{'orientation': 'POSITIVE', 'representative':'suki'},\
               'Hikuwa':{'orientation': 'NEGATIVE', 'representative':'iya'},\
               'Nyan':{'orientation': 'POSITIVE', 'representative':'yorokobi'},\
               'Tensai':{'orientation': 'POSITIVE', 'representative':'takaburi'},\
               'Install':{'orientation': 'NEUTRAL', 'representative':'None'},\
               'Gogogo':{'orientation': 'POSITIVE', 'representative':'None'},\
               'Kawaii':{'orientation': 'POSITIVE', 'representative':'suki'},\
               'Haroha':{'orientation': 'POSITIVE', 'representative':'None'},\
               'Haroro':{'orientation': 'POSITIVE', 'representative':'None'},\
               'Haroo':{'orientation': 'POSITIVE', 'representative':'None'},\
               'Harobikuri':{'orientation': 'POSITIVE', 'representative':'None'}}
           
emotion = MLAsk()
emo = lambda m: emotion.analyze(m)

def try_emotion_perse(m):
    e = emo(m)
    if ':_kizunaai' in e['text']: #　カスタム絵文字
        category = re.findall(r':_kizunaai(.*?):', e['text'])
        orien, repre = custom_emoji[category[0]]['orientation'], custom_emoji[category[0]]['representative']

    else:                           
        try:
            orien = e['orientation']
        except KeyError:
            return None, None
        ekey = list(e['emotion'].keys())
        repre = ekey[0]

    return orien, repre

ori_list = []
repre_list = []
for index, row in df['message'].iteritems():
    ori, rep = try_emotion_perse(row)
    ori_list.append(ori)
    repre_list.append(rep)

orien = pd.Series(ori_list, name='orientation')
repre = pd.Series(repre_list, name='representative')
df_message = pd.concat([elap, message, orien, repre], axis=1)

onemin_orien = []
onemin_repre = []
for t in range(0, int(df_message.iat[-1,0]), 60): # 0秒からelapstime最終行の値まで60秒刻み
    start = t
    end = t + 60
    value = df_message.query('{} < elapsedtime < {}'.format(start, end))
    onemin_orien.append(dict(value['orientation'].value_counts()))
    onemin_repre.append(dict(value['representative'].value_counts()))

total_orien = pd.DataFrame(onemin_orien).fillna(0)
total_repre = pd.DataFrame(onemin_repre).fillna(0)
total_repre.drop('None', axis=1, inplace=True)
# total_orien.plot()
# plt.title('positive/negative分類')
# plt.xlabel('再生時間')
# plt.ylabel('コメント個数')
# plt.show()
# plt.savefig('orien.png')

total_repre.plot()
# plt.xlabel('再生時間')
# plt.ylabel('コメント個数')
# plt.savefig('reple.png')
plt.legend()