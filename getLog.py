import requests
from hashlib import md5
import io
import argparse

###########################
#Read in Arguments & set default parameters
###########################
parser = argparse.ArgumentParser(description='Get the log file')
parser.add_argument("--pw",help="--pw=myPassword")

parser.add_argument("--opFile",default='eeg.csv',help="--opFile='path_to_file'")

args = parser.parse_args()

r = requests.get('http://192.168.1.254/index.cgi?active_page=9144')
login = args.pw

# if 'Prasads' in r.text():
    # print "found"
# else:
    # print "not found"
#print(r.text)
# buf = io.StringIO(r.text)
buf = r.text.split("\n")

for line in buf:
    a = line.find('password_')
    if a >=0:
        password_id,junk = line[a:a+25].split("'",1)
        print(password_id)
        break

for line in buf:
    a = line.find('"auth_key" value="')
    if a >=0:
        junk,auth_key,junk2 = line[a+15:].split('"',2)
        print("9 char auth_key = ",auth_key)
        break


for line in buf:
    a = line.find('"post_token" value=')
    if a >=0:
        junk,post_token,junk2 = line[a+15:].split('"',2)
        print("64 char post_token = ",post_token)
        break


for line in buf:
    a = line.find('"request_id" value=')
    if a >=0:
        junk,request_id,junk2 = line[a+15:].split('"',2)
        #print (line)
        #print(junk, " ", request_id, " ", junk2)
        print("10 char request_id = ",request_id)
        break


print ("session_id = ", r.cookies['rg_cookie_session_id'])

# hash = hashlib.md5()
# hash.update(('%s%s' % (login, password_id)).encode('utf-8'))
# pw_hash = hash.hexdigest()
pw_hash = md5((login + auth_key).encode('utf-8')).hexdigest()
print ("salted md5 hash = ", pw_hash)


#payload = {'request_id': request_id, 'active_page': '9148', 'mimic_button_field':'submit_button_login_submit%3A+..','post_token': post_token, 'password_' + password_id:'', 'md5_pass': pw_hash, 'auth_key': auth_key }

payload = 'request_id='+request_id+'&active_page=9144&active_page_str=bt_login&mimic_button_field=submit_button_login_submit%3A+..&button_value=&post_token='+post_token+'&password_'+password_id+'=&md5_pass='+pw_hash+'&auth_key='+auth_key

print (payload)

my_headers = {'Content-Type':'application/x-www-form-urlencoded','Cache-Control':'max-age=0','Referer':'http://192.168.1.254/index.cgi?active_page=9121','Connection':'keep-alive','DNT':'1'}

r1=requests.post('http://192.168.1.254/index.cgi', data=payload, headers=my_headers, cookies=r.cookies,allow_redirects=True)
print(r1)
print(r1.request.body)
print(r1.request.headers)

with open('result1.html','w', encoding="utf-8") as f:
    f.write(r1.text)
