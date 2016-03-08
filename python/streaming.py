from json import loads, dumps
from sys import stdin, stdout


def Comptroller(func_list, name, start_urls, allowed_domains): 
    print dumps({'type':'spider_settings', 
                 'name':name, 
                 'start_urls':start_urls, 
                 'allowed_domains':allowed_domains})
    stdout.flush()
    func_dict = {func.func_name:func for func in func_list}
    
    while True:
        line = stdin.readline()
        dict = loads(line)
        if dict['callback']:
            returned = func_dict[dict['callback']](dict)
        else:
            returned = func_dict['parse'](dict)
        print dumps(returned)
        stdout.flush()
