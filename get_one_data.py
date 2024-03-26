from elasticsearch import Elasticsearch
import csv
# from dotenv import load_dotenv
import os

# load_dotenv()
username = os.environ['ELASTIC_USERNAME']
password = os.environ['ELASTIC_PASSWORD']
index = os.environ['ELASTIC_INDEX']
host = os.environ['ELASTIC_HOST']

# Kết nối tới Elasticsearch với thông tin tài khoản
es = Elasticsearch([{'host': host, 'port': 9200}], http_auth=(username, password))

query = {
    "query": {
        "match": {
            "city": "Tỉnh Đồng Nai"
        }
    }

}

res = es.search(index=index, body=query, size=1)
hit = res['hits']['hits'][0]


# Lưu dòng dữ liệu vào file CSV
csv_file = "data/output.csv"
csv_columns = ['area','bathroom','bedroom','city','createDate','direction'
'district','postId', 'postType', 'price', 'street', 'ward']

try:
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:  # Mở ở chế độ thêm (append mode)
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        if csvfile.tell() == 0:  # Kiểm tra nếu tệp CSV trống
            writer.writeheader()
        row = {col: hit['_source'].get(col, 'null') for col in csv_columns}
        writer.writerow(row)
        print("Dữ liệu đã được thêm vào file output.csv")
except IOError:
    print("Lỗi khi mở hoặc ghi vào file CSV")