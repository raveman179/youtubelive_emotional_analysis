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
    # onemin_orien.append(dict(value['orientation'].value_counts()))
    onemin_orien.append((start/60,dict(value['orientation'].value_counts())))
    onemin_repre.append(dict(value['representative'].value_counts()))

# total_orien = pd.DataFrame(onemin_orien).fillna(0)
# total_orien = total_orien.loc[:, ['POSITIVE','NEUTRAL','NEGATIVE','mostly_POSITIVE', 'mostly_NEGATIVE']]

# total_repre = pd.DataFrame(onemin_repre).fillna(0)
# total_repre.drop('None', axis=1, inplace=True)
# total_repre = total_repre.loc[:, ['suki', 'yorokobi', 'takaburi','odoroki','ikari','haji','kowa','iya','aware','yasu', 'ikari']]

pprint(onemin_orien)

# total_orien.plot()
# plt.title('POSITIVE/NEGATIVE分類')
# plt.xlabel('再生時間')
# plt.ylabel('コメント個数')
# plt.savefig('orien.png')

# total_repre.plot()
# plt.title('感情別分類')
# plt.xlabel('再生時間')
# plt.ylabel('コメント個数')
# plt.savefig('reple.png')

'''
[(0.0, {'NEGATIVE': 1, 'POSITIVE': 1}),
 (1.0, {'NEGATIVE': 1, 'POSITIVE': 1}),
 (2.0, {'POSITIVE': 3}),
 (3.0, {'POSITIVE': 5}),
 (4.0, {'NEGATIVE': 4, 'NEUTRAL': 2, 'POSITIVE': 16}),
 (5.0, {'NEGATIVE': 2, 'NEUTRAL': 1, 'POSITIVE': 15}),
 (6.0, {'NEGATIVE': 1, 'POSITIVE': 9}),
 (7.0, {'NEGATIVE': 2, 'POSITIVE': 17}),
 (8.0, {'NEGATIVE': 5, 'NEUTRAL': 1, 'POSITIVE': 7}),
 (9.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 9}),
 (10.0, {'NEGATIVE': 2, 'NEUTRAL': 1, 'POSITIVE': 22}),
 (11.0, {'NEGATIVE': 3, 'NEUTRAL': 1, 'POSITIVE': 17}),
 (12.0, {'NEGATIVE': 3, 'NEUTRAL': 7, 'POSITIVE': 39}),
 (13.0, {'NEUTRAL': 25, 'POSITIVE': 76}),
 (14.0, {'NEGATIVE': 1, 'NEUTRAL': 29, 'POSITIVE': 66}),
 (15.0, {'NEGATIVE': 1, 'NEUTRAL': 25, 'POSITIVE': 51}),
 (16.0, {'NEGATIVE': 8, 'NEUTRAL': 6, 'POSITIVE': 166}),
 (17.0, {'NEGATIVE': 9, 'NEUTRAL': 4, 'POSITIVE': 60}),
 (18.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 34, 'mostly_POSITIVE': 2}),
 (19.0, {'NEGATIVE': 4, 'NEUTRAL': 1, 'POSITIVE': 36, 'mostly_POSITIVE': 2}),
 (20.0, {'NEGATIVE': 3, 'POSITIVE': 12, 'mostly_NEGATIVE': 1}),
 (21.0, {'NEGATIVE': 8, 'NEUTRAL': 3, 'POSITIVE': 44}),
 (22.0, {'NEGATIVE': 7, 'NEUTRAL': 3, 'POSITIVE': 61, 'mostly_NEGATIVE': 1}),
 (23.0, {'NEGATIVE': 1, 'NEUTRAL': 2, 'POSITIVE': 25}),
 (24.0, {'NEGATIVE': 3, 'NEUTRAL': 1, 'POSITIVE': 36}),
 (25.0,
  {'NEGATIVE': 7,
   'NEUTRAL': 3,
   'POSITIVE': 26,
   'mostly_NEGATIVE': 1,
   'mostly_POSITIVE': 1}),
 (26.0, {'NEUTRAL': 1, 'POSITIVE': 20}),
 (27.0, {'NEGATIVE': 6, 'POSITIVE': 9}),
 (28.0, {'NEGATIVE': 3, 'NEUTRAL': 2, 'POSITIVE': 25}),
 (29.0, {'POSITIVE': 22}),
 (30.0, {'NEGATIVE': 2, 'POSITIVE': 18}),
 (31.0, {'NEGATIVE': 10, 'NEUTRAL': 3, 'POSITIVE': 8, 'mostly_POSITIVE': 5}),
 (32.0, {'NEGATIVE': 2, 'NEUTRAL': 2, 'POSITIVE': 3}),
 (33.0,
  {'NEGATIVE': 2, 'POSITIVE': 6, 'mostly_NEGATIVE': 1, 'mostly_POSITIVE': 1}),
 (34.0, {'NEGATIVE': 2, 'POSITIVE': 49, 'mostly_POSITIVE': 1}),
 (35.0, {'NEGATIVE': 6, 'NEUTRAL': 1, 'POSITIVE': 22}),
 (36.0, {'NEGATIVE': 3, 'POSITIVE': 37}),
 (37.0, {'NEUTRAL': 1, 'POSITIVE': 18, 'mostly_POSITIVE': 1}),
 (38.0, {'NEGATIVE': 1, 'POSITIVE': 4}),
 (39.0, {'NEGATIVE': 1, 'POSITIVE': 10}),
 (40.0, {'NEGATIVE': 5, 'POSITIVE': 8}),
 (41.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 17}),
 (42.0,
  {'NEGATIVE': 3,
   'NEUTRAL': 2,
   'POSITIVE': 15,
   'mostly_NEGATIVE': 2,
   'mostly_POSITIVE': 2}),
 (43.0, {'NEGATIVE': 21, 'NEUTRAL': 4, 'POSITIVE': 28}),
 (44.0, {'NEGATIVE': 12, 'NEUTRAL': 1, 'POSITIVE': 12}),
 (45.0, {'NEGATIVE': 14, 'NEUTRAL': 3, 'POSITIVE': 49, 'mostly_NEGATIVE': 1}),
 (46.0, {'NEGATIVE': 4, 'NEUTRAL': 1, 'POSITIVE': 79}),
 (47.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 128}),
 (48.0, {'NEGATIVE': 2, 'POSITIVE': 39}),
 (49.0, {'NEGATIVE': 1, 'NEUTRAL': 4, 'POSITIVE': 11}),
 (50.0, {'NEGATIVE': 1, 'POSITIVE': 17}),
 (51.0, {'NEGATIVE': 1, 'POSITIVE': 7}),
 (52.0, {'NEUTRAL': 1, 'POSITIVE': 1}),
 (53.0, {'NEGATIVE': 6, 'POSITIVE': 3}),
 (54.0, {'NEGATIVE': 2, 'NEUTRAL': 1, 'POSITIVE': 1}),
 (55.0, {'NEGATIVE': 5, 'NEUTRAL': 3, 'POSITIVE': 5}),
 (56.0, {'NEGATIVE': 1, 'NEUTRAL': 2, 'POSITIVE': 6}),
 (57.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 8}),
 (58.0, {'NEGATIVE': 2, 'POSITIVE': 9}),
 (59.0, {'NEGATIVE': 3, 'POSITIVE': 98}),
 (60.0, {'NEGATIVE': 1, 'POSITIVE': 38}),
 (61.0, {'POSITIVE': 11}),
 (62.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 34}),
 (63.0, {'NEGATIVE': 2, 'NEUTRAL': 1, 'POSITIVE': 28}),
 (64.0, {'NEGATIVE': 4, 'NEUTRAL': 4, 'POSITIVE': 13}),
 (65.0, {'POSITIVE': 17}),
 (66.0, {'NEGATIVE': 1, 'POSITIVE': 9}),
 (67.0, {'NEGATIVE': 4, 'NEUTRAL': 2, 'POSITIVE': 9}),
 (68.0, {'NEGATIVE': 3, 'NEUTRAL': 3, 'POSITIVE': 19}),
 (69.0, {'NEGATIVE': 2, 'POSITIVE': 9}),
 (70.0, {'NEGATIVE': 1, 'NEUTRAL': 1, 'POSITIVE': 20}),
 (71.0, {'NEUTRAL': 2, 'POSITIVE': 23}),
 (72.0, {'NEUTRAL': 4, 'POSITIVE': 8}),
 (73.0, {'NEUTRAL': 2, 'POSITIVE': 5}),
 (74.0, {'POSITIVE': 5})]
'''