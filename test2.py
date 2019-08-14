logline = '''123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET / HTTP/1.1" 200 8642 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'''

lst = []
for word in logline.split():
    lst.append(word)


for i, key in enumerate(lst):
    print(i, key)