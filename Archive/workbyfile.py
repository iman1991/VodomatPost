import json
import time

def write_on_file(information):
    date_time=dict(datetime = time.time())
    f=open('archive.txt','a')
    date=information
    date_time.update(date)
    solution=json.dumps(date)
    f.write(solution+'\n')
    f.close()

def read():
    print('Читаем из файла')
    f = open('archive.txt', 'r')
    a=f.read()
    f.close()
    a="["+a+"]"
    d = json.loads(a)
    return d