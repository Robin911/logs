import re
logline = '''123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET / HTTP/1.1" 200 8642 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'''

def extract(line):
    pattern = '''(?P<remote>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "([^"]+)" "(?P<useragent>[^"]+)"'''
    regex = re.compile(pattern)
    matchar = regex.match(line)
    return matchar.groupdict()

print(extract(logline))