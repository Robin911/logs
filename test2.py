import datetime, re

logline = '''123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET / HTTP/1.1" 200 8642 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'''
def extract(line):
    pattern = '''(?P<remote>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<aaaaaa>[^"]+)" "(?P<useragent>[^"]+)"'''
    regex = re.compile(pattern)
    matchar = regex.match(line)
    return matchar.groupdict()
def convert_time(timestr):
    return datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z')
def convert_request(request:str):
    return dict(zip(['method', 'url', 'protocol'], request.split()))
ops = {
    'datetime':convert_time,
    'status':int,
    'size':int,
    'request':convert_request
}
d = {}
for k, v in extract(logline).items():
    d[k] = ops.get(k, lambda x:x)(v)

for k, v in d.items():
    print(k, ':', v)