import pytchat
import time
# PytchatCoreオブジェクトの取得
video_id = "I1wqOXlXHp8"
'''
"zCK_490ryjg"　キズナアイから大事なお知らせがあります
"9u_I1k65MYE"　【空気読み。】読めるんです！ほんとです！ぺこ！【ホロライブ/兎田ぺこら】
"I1wqOXlXHp8"　公園の地下に巨大神殿があるらしいので行ってみた【にじさんじ/月ノ美兎】
'''
livechat = pytchat.create(video_id)# video_idはhttps://....watch?v=より後ろの
filepath = "./comment_{}.txt".format(video_id)

with open(filepath, mode='a') as f:
    while livechat.is_alive():
        # チャットデータの取得
        chatdata = livechat.get()
        for c in chatdata.items:
            f.write(f"{c.datetime},{c.author.name},{c.message}\n")
            '''
            JSON文字列で取得:
            # print(c.json())
            '''
        time.sleep(5)