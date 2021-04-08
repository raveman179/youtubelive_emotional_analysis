import pytchat
import time
# PytchatCoreオブジェクトの取得
livechat = pytchat.create(video_id = "zCK_490ryjg")# video_idはhttps://....watch?v=より後ろの
filepath = "./comment_zCK_490ryjg.txt"

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