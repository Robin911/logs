logline = '''123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET / HTTP/1.1" 200 8642 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'''

lst = []
flag = False
for word in logline.split():
    if not flag and (word.startswith('[') or word.startswith('"')):
        if word.endswith('"') or word.endswith(']'):
            tmp = word[1:-1]
            flag = False
            lst.append(tmp)
        else:
            tmp = word[1:]
            flag = True
        continue
    if flag:
        if word.endswith(']') or word.endswith('"'):
            tmp += ' ' + word[:-1]
            lst.append(tmp)
            flag = False
            continue
        else:
            tmp += ' ' + word
            continue

    lst.append(word)

for i, key in enumerate(lst):
    print(i, key)