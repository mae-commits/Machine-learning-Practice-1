import requests
import json
import os
import time
from fake_useragent import UserAgent

os.makedirs('result', exist_ok=True)

search_term = ""
sort_key = "newest"
category_list = [16, 331, 332, 333, 334, 335, 336, 337, 52, 362, 338, 51, 339, 340, 341, 342] # technology category
base_query = "https://www.kickstarter.com/projects/search.json?term={term}&category_id={category_id}&page={page_id}&sort={sort}"

# テクノロジーカテゴリのカテゴリIDで検索をかける
for category_id in category_list:
    project_count = 0
    # page_id 1~200 で検索
    for page_id in range(1, 201):
        # query を投げてjson形式でレスポンスを受け取る
        try:
            query = base_query.format(term=search_term, category_id=category_id, page_id=page_id, sort=sort_key)
            print(query)
            headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
            r = requests.get(query, headers=headers)
            print(r.status_code)
            response_json=r.json()
            print(response_json) 
        except:
            break
        
        if len(response_json["projects"]) == 0:
            break
        
        project_count += len(response_json["projects"])
        total_hits = response_json["total_hits"]
        
        print(category_id, "progress", project_count, "/", total_hits, round(float(project_count)/total_hits * 100, 2), "%")
        
        for project in response_json["projects"]:
            filepath = "result/{}.json".format(project["id"])
            fp = open(filepath, "w")
            fp.write(json.dumps(project, sort_keys=True, indent=2))
            fp.close()
            
        time.sleep(1)