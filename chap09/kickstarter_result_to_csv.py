# import した .json データを .csv データに変換
import glob
import json
import pandas as pd
import pandas.io.json

project_list = []

# result/ 以下の .json ファイルを抽出し、project_list に格納
for filename in glob.glob("result/*.json"):
    project = json.loads(open(filename).read())
    project_list.append(project)

# リストを DataFrame に変換
df = pandas.io.json.json_normalize(project_list)

# 時間を意味するカラムを抽出
datetime_columns = filter(lambda a:a[-3:] == "_at", df.columns)
# 選択したカラム中のデータを datetime に変換
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column], unit='s')
# DataFrame を csv に変換
csv_data = df.to_csv()

# 結果を書き込み
fp = open('kickstarter_result.csv', 'wb')
fp.write(csv_data)
fp.close()