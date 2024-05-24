import urllib.request
import time
import urllib.parse
from bs4 import BeautifulSoup as Soup

# User input
username = 'Fill username'
password = 'Fill password'
init_url = 'https://gateway.iitk.ac.in:1003/fgtauth?65ca92cc56aa4562'

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]

exit_time = 10 # script exit time in secs

while True:
    try:
        test = opener.open(init_url)
        print("Connecting...")
        break
    except:
        print("Trying to connect to https://gateway.iitk.ac.in:1003")
        time.sleep(2)
        exit_time = exit_time - 2
        if exit_time < 0: exit(1)

html = test.read()
parsed = Soup(html, 'html.parser')

data = {"4Tredir": f"{init_url}", "username": username, "password": password}
form = parsed.findAll('form')[0]
magic = form.findAll('input')[1]['value']
data['magic'] = str(magic)

time.sleep(2)
login_data = urllib.parse.urlencode(data).encode('utf-8')
try:
    test = opener.open('https://gateway.iitk.ac.in:1003', login_data)
    print('Connection established')
except:
    print('Cannot connect now')

html = test.read()

parsed = Soup(html, 'html.parser')
script_tag = parsed.find('script', {'language': 'JavaScript'})
script_content = script_tag.string
key = script_content.split('?')[1][:-2]
url = 'https://gateway.iitk.ac.in:1003/keepalive?' + key
time.sleep(2400)

while True:
    try:
        opener.open(url)
        print('Authentication refreshed... ')
        time.sleep(2400)
    except:
        print('Cannot refresh the authentication ', url)
        time.sleep(10)
