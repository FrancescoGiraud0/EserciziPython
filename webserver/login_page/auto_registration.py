import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

URL = "http://127.0.0.1:5000/register"
IP  = "127.0.0.1"
method = 'POST'
username = 'luigi'
passw = '0000'

s.connect((IP, 5000))

request_type = f'{method} {URL} HTTP/1.0'
body_entity = f'username={username}&password={passw}'
headers = f'Content-Type: application/x-www-form-urlencoded\nContent-Length: {len(body_entity)}'

request = f'{request_type}\n{headers}\n\n{body_entity}'

print(f'REQUEST:\n{request}\n'+ '-'*10)

s.sendall(request.encode())

http_response = []
data = 'None'

while data != '':
    data = s.recv(4096).decode()
    print(f'{data}')
    http_response.append(data)

html_doc = http_response[-2]
tag_pos = html_doc.find('<html>')
html_doc = html_doc[tag_pos:]

out_file = open('register.html', 'w')
out_file.write(html_doc)
out_file.close()

s.close()
