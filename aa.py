import datetime, re
logline = '''123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET / HTTP/1.1" 200 8642 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'''
regex = re.compile('''(?P<remote>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<aaaaaa>[^"]+)" "(?P<useragent>[^"]+)"''')
ops = {
    'datetime':lambda timestr:datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z'),
    'status':int,
    'size':int,
    'request':lambda request:dict(zip(['method', 'url', 'protocol'], request.split()))
}
def extract(line):
    matchar = regex.match(line)
    return {k:ops.get(k, lambda x:x)(v) for k, v in matchar.groupdict().items()}
for k, v in extract(logline).items():
    print(k, ':', v)