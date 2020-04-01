import urllib

def internet_on():
    try:
        urllib.urlopen('http://216.58.192.142', timeout=1)
        print('Conexión establecida')
        return True
    except urllib.URLError as err: 
        print('Conexión fallida')
        return False

print(internet_on)