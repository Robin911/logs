import datetime, re
from queue import Queue
import threading
from pathlib import Path
regex = re.compile('''(?P<remote>[\d\.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<aaaaaa>[^"]+)" "(?P<useragent>[^"]+)"''')

def extract(line):
    matchar = regex.match(line)
    if matchar:
        return {k:ops.get(k, lambda x:x)(v) for k, v in matchar.groupdict().items()}
ops = {
    'datetime':lambda timestr:datetime.datetime.strptime(timestr, '%d/%b/%Y:%H:%M:%S %z'),
    'status':int,
    'size':int,
    'request':lambda request:dict(zip(['method', 'url', 'protocol'], request.split()))
}

def openfile(path:str):
    with open(path) as f:
        for line in f:
            fields = extract(line)
            if fields:
                yield fields
            else:
                continue # TODO 解析失败的日志抛弃
def load(*paths):
    for item in paths:
        p = Path(item)
        if not p.exists():
            continue
        if p.is_dir():
            for file in p.iterdir():
                if file.is_file():
                    yield from openfile(str(file))
        elif p.is_file():
            yield from openfile(str(p))

####################################################################################
def window(src:Queue, handler, width: int, interval: int):
    start = datetime.datetime.strptime('1970/01/01 01:01:01 +0800', '%Y/%m/%d %H:%M:%S %z')
    current = datetime.datetime.strptime('1970/01/01 01:01:02 +0800', '%Y/%m/%d %H:%M:%S %z')
    delta = datetime.timedelta(seconds=width - interval)
    buffer = []
    while True:
        data = src.get()
        if data:
            buffer.append(data)
            current = data['datetime']
        if (current - start).total_seconds() >= interval:
            ret = handler(buffer)
            print(ret)
            start = current
            buffer = [i for i in buffer if i['datetime'] > current - delta]

def donothing_handler(iterable:list):
    print(iterable)
    return iterable

def status_handler(iterable):
    status = {}
    for item in iterable:
        key = item['status']
        status[key] = status.get(key, 0) + 1
    total = len(iterable)
    return {k:status[k]/total for k, v in status.items()}
#################################################################################################
# 分发器
def dispatcher(src):
    # 分发器中记录handler， 同时保存各自的队列
    threads = []
    queues = []
    def reg(handler, width:int, interval:int):
        q = Queue()
        queues.append(q)
        h = threading.Thread(target=window, args=(q, handler, width, interval))
        threads.append(h)
    def run():
        for t in threads:
            t.start()
        for item in src:
            for q in queues:
                q.put(item)
    return reg, run

reg, run = dispatcher(load('test.log'))

# 注册 窗口
reg(status_handler, 7, 5)

# 启动
run()