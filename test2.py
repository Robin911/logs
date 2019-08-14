logline = '''123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET / HTTP/1.1" 200 8642 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'''

import datetime

def convert_time(timestr):
    return datetime.datetime.strftime(timestr, '%d/%b/%Y:%H:%M:%S %z')

fields = []
flag = False
for word in logline.split():
    if not flag and (word.startswith('[') or word.startswith('"')):
        if word.endswith('"') or word.endswith(']'):
            tmp = word[1:-1]
            flag = False
            fields.append(tmp)
        else:
            tmp = word[1:]
            flag = True
        continue
    if flag:
        if word.endswith(']') or word.endswith('"'):
            tmp += ' ' + word[:-1]
            fields.append(tmp)
            flag = False
            continue
        else:
            tmp += ' ' + word
            continue
    fields.append(word)

names = ['remote', '', '', 'datetime', 'request', 'status', 'size', 'useragent', '']
ops = [None, None, None, convert_time, None, int, int, None, None]

d = {}
for i, field in enumerate(fields):
    key = names[i]
    d[key] = field

for k, v in d.items():
    print(k,':', v)