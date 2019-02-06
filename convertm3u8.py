import requests
import sys
import shutil
import os
import wget

url = sys.argv[1]
domain_name = url.split('/')[2]
contents = requests.get(url)
contents = contents.text
ts_filenames = []

for file in os.listdir("/home/ana/"):
    if file.endswith(".ts"):
        os.remove(file)

for i in contents.split("\n"):
    if ".ts" in i:
        ts_filenames.append(str(i).split('/')[-1])
        wget.download('http://' + domain_name + i)
    with open('merged.ts', 'wb') as merged:
        for ts_file in ts_filenames:
            with open(ts_file, 'rb') as mergefile:
                shutil.copyfileobj(mergefile, merged)

os.system("ffmpeg -i /home/ana/merged.ts -y -bsf:a aac_adtstoasc -c:v copy -c:a copy -movflags +faststart /home/ana/Downloads/send.mp4")
