import json
import csv
import random
from urllib.request import urlopen
from sklearn import model_selection, ensemble, metrics
from sklearn.utils import shuffle
from tqdm import trange
from time import gmtime, strftime

# 讀入向量化訓練資料
url = 'https://raw.githubusercontent.com/kk25gb/AIdea-project-file/main/stage1/vectorize_data.json'
response = urlopen(url)
data = json.loads(response.read())
known_assay_labels = list(data.keys())

# 讀入 truth label
url = 'https://raw.githubusercontent.com/kk25gb/AIdea-project-file/main/stage1/TrainLabel.csv'
response = urlopen(url)
lines = [l.decode('utf-8') for l in response.readlines()]
true_labels = list(csv.reader(lines))
del true_labels[0]

# 讀入 stage2 預測資料
with open("../stage2/vectorize_data.json") as f:
	test_data = json.load(f)
print("test data length:",len(test_data))

# 生成 false label
input_keys = list(data.keys())
false_labels = []
while len(false_labels) < len(true_labels):
	temp = [random.choice(input_keys), random.choice(input_keys)]
	if temp[0] == temp[1]:
		continue
	if temp not in true_labels:
		false_labels.append(temp)


# 產生所需資料格式
def data_generator(input, Label=0):
	return [[data[row[0]] + data[row[1]], Label] for row in input]

# 產生標籤為True的向量資料對
true_list = data_generator(true_labels,1)
# print(true_list[0])
# 產生標籤為False的向量資料對
false_list = data_generator(false_labels,0)

# 混合 Ture / False 標籤的資料
train_list = true_list + false_list

X = [row[0] for row in train_list]
Y = [row[1] for row in train_list]

# 從 train_list 中分出 validation data
train_X, valid_X, train_y, valid_y = model_selection.train_test_split(X, Y, random_state=777, test_size = 0.3)
# print(valid_X[0])
# 訓練 random forest 模型
forest = ensemble.RandomForestClassifier(n_estimators = 3000, criterion='entropy')
forest_fit = forest.fit(train_X, train_y)


# 預測 validation set
valid_y_predicted = forest.predict(valid_X)

accuracy = metrics.accuracy_score(valid_y, valid_y_predicted)
print(accuracy)

# 預測 stage2 test data

# 處理 stage2 預測資料格式
# print(test_list[0])
results={}
test_keys = list(test_data.keys())

for label1 , assay_1 in test_data.items():
	temp_list=[]
	data_to_predict = [assay_1+assay_2 for assay_2 in list(test_data.values()) if assay_1 != assay_2]
	# print(len(test_data))
	# break
	valid_y_predicted = forest.predict(data_to_predict)
	for i in range(len(valid_y_predicted)):
		if valid_y_predicted[i]==1:
			temp_list.append(test_keys[i])
	results[label1]=temp_list

# print(results[list(test_data.keys())[0]])

# with open('./predict_results.json', 'w', encoding='utf8') as f:
#     json.dump(results, f, ensure_ascii=False)

table = [['Test','Reference']]

for key, value in results.items():
	# for num in results[value]:
	if len(value)>0:
		for item in value:
			table.append([key, item])


with open('../output/output_'+str(strftime("%Y-%m-%d %H-%M-%S", gmtime()))+'.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	# 寫入二維表格
	writer.writerows(table)