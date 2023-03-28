import socket

def request(url):

    # make sure the url start with a http request
    assert url.startwith('http://')
    url = url[len('http://')]

    # splitting the host and path form the url
    host, path = url.split('/', 1)
    path = '/' + path #adding the / back to the path

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP
    )
    s.connect((host, 80))

    s.send('GET {} HTTP/1.0\r\n'.format(path).encode('utf-8') + 
        'HOST {}\r\n\r\n'.format(host).encode('utf-8'))

    # Reading the response using makefile helper function which hides the loop for response reading, 
    # makefile returns a file like object containing every byte received from the server 
    response = s.makefile('r', encoding='utf-8', newline='\r\n')

    # splitting the response into pieces 
    statusline = response.readline()
    status, version, explanation = statusline(' ', 2)
    assert status == '200', '{}: {}'.format(status, explanation)

    # splitting the header line 
    headers = {}
    while True:
        line = response.readline()
        if line == '\r\n' : break
        header, value = line.split(':', 1)
        headers[header.lower()] = value.strip() #normalize header to lower case and strip leading and trailing while spaces

    # assuring some kind of header are no present
    assert 'transfer-encoding' not in headers
    assert 'content-encoding' not in headers

    # get the message body
    body = response.read()
    s.close()

    return headers, body