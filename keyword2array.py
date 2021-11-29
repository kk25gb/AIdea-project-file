# 問題: 鋅錳乃浦 和 鋅錳乃浦水懸劑 會被重複計算
import os
import numpy as np
import pandas as pd

keywordResult = np.zeros((560, 765)) # 540 articles 765 ketwords
df_all = pd.read_excel("C:\\Users\\User\\Desktop\\AIdea\\Stage_1\\Keywords\\Keywords\\02all.list.xlsx") # read keywords xlsx
df_all = df_all.fillna("nan") # delete "nan"
dirpath = "C:\\Users\\User\\Desktop\\AIdea\\Stage_1\\Train\\dataTrainComplete"
allFileList = os.listdir(dirpath)

# test
# test = f.read()
# print(df_all.iloc[0, :])
# print(test)
# print(test.find(df_all.iloc[2, 0]))
# print(test.count('鋅錳乃浦'))
# f = open("C:\\Users\\User\\Desktop\\AIdea\\Stage_1\\Train\\dataTrainComplete\\1.txt", "r", encoding="UTF-8")

# 計算次數
# cnt = 0
# for file in allFileList:
#     f = open("C:\\Users\\User\\Desktop\\AIdea\\Stage_1\\Train\\dataTrainComplete\\" + file, "r", encoding="UTF-8")
#     article = f.read()
#
#     for i in range(764):
#         keyword_cnt = 0
#         for j in range(7):
#             tmp = article.count(df_all.iloc[i, j])
#             if tmp == -1: tmp = 0
#             keyword_cnt = keyword_cnt + tmp
#         keywordResult[cnt, i] = keyword_cnt
#
#     cnt = cnt + 1
#
# print(keywordResult)

# binary 呈現
cnt = 0
articleIndex = [""] * 560
for file in allFileList:
    f = open("C:\\Users\\User\\Desktop\\AIdea\\Stage_1\\Train\\dataTrainComplete\\" + file, "r", encoding="UTF-8")
    article = f.read()
    articleIndex[cnt] = file

    for i in range(764):
        keyword_cnt = 0
        for j in range(7):
            tmp = article.count(df_all.iloc[i, j])
            if tmp == -1: tmp = 0
            keyword_cnt = keyword_cnt + tmp
            if keyword_cnt >= 1: keyword_cnt = 1
        keywordResult[cnt, i] = keyword_cnt

    cnt = cnt + 1

print(keywordResult)

score = np.zeros((560, 560))

for m in range(559):
    for n in range(559, m, -1):
        for w in range(764):
            if (keywordResult[m, w] == 1) & (keywordResult[n, w] == 1):
                score[m, n] = score[m, n] + 1

for q in range(559):
    for p in range(559):
        if score[q, p] >= 20:
            print(articleIndex[q], articleIndex[p])



# score = 0
# for x in range(764):
#     if (keywordResult[0, x] == 1) & (keywordResult[1, x] == 1):
#         score = score + 1
#
# print(score)

# y_true = keywordResult[0]
# y_pred = keywordResult[1]
# print(y_true)
# print(y_pred)
#
# print(jaccard_similarity_score(keyword_cnt[0], keyword_cnt[1]))
# index = file.replace(".txt", "")

