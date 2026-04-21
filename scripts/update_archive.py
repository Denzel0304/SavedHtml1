import os
import json
import re
from datetime import datetime

data_dir = 'data'
output_file = 'list.json'
allowed_extensions = ('.html', '.htm')

archive_list = []

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

for filename in os.listdir(data_dir):
    if filename.lower().endswith(allowed_extensions):
        filepath = os.path.join(data_dir, filename)
        
        # 파일명 분석: [카테고리][태그] 제목_메모.html
        # 예: [경제][부동산,법률] 제목_메모.html
        category = "미분류"
        tags = []
        title = filename
        memo = ""
        
        # 정규식으로 대괄호 내용 추출
        brackets = re.findall(r'\[(.*?)\]', filename)
        if len(brackets) >= 1:
            category = brackets[0]
        if len(brackets) >= 2:
            tags = [t.strip() for t in brackets[1].split(',')]
            
        # 대괄호 제거 후 제목과 메모 분리
        pure_name = re.sub(r'\[.*?\]', '', filename).strip()
        if '_' in pure_name:
            parts = pure_name.split('_', 1)
            title = parts[0].strip()
            memo = parts[1].rsplit('.', 1)[0].strip()
        else:
            title = pure_name.rsplit('.', 1)[0].strip()

        file_stat = os.stat(filepath)
        archive_list.append({
            "title": title,
            "filename": filename,
            "category": category,
            "tags": tags,
            "memo": memo,
            "date": datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M')
        })

# 최신순 정렬
archive_list.sort(key=lambda x: x['date'], reverse=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(archive_list, f, ensure_ascii=False, indent=2)
