import socket
import sys
import ssl
import requests

def request(url):

    # make sure the url start with a http or https request
    # assert url.startswith('http://', 'https://')
    # url = url[len('http://'):]
    scheme, url = url.split('://', 1)
    assert scheme in ['http', 'https'], 'Unknown Schemc {}'.format(scheme)

    

    # splitting the host, path and port form the url
    host, path = url.split('/', 1)
    path = '/' + path #adding the / back to the path
    port = 80 if scheme=='http' else 443
    # if custom port are mentioned in the url, split it form the host name 
    if ':' in host:
        host, port = host.splist(':', 1)
        port = int(port)

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP
    )
    """
    Python ssl library implements all of these details for us, so making an encrypted connection is almost as easy as making a regular connection.
    When you wrap s, you pass a server_hostname argument, and it should match the argument you passed to s.connect. Note that I save the new socket back into the s variable. That’s because you don’t want to send over the original socket; it would be unencrypted and also confusing.
    """
    if scheme == 'https':
        ctx = ssl.create_default_context()
        s = ctx. wrap_socket(s, server_hostname=host)
    s.connect((host, port))

    # send request message to the server in proper http format.
    connectionType = 'close'
    uaHttpbin = requests.get('http://httpbin.org/user-agent') # make a request to httpbin to get the user agent
    userAgent = uaHttpbin.json()['user-agent'] # convert the response to json and extract the user-agent
    request = 'GET {} HTTP/1.0\r\n'.format(path) + 'Host {}\r\n'.format(host) + 'Connection {}\r\n'.format(connectionType) + 'User-Agent {}\r\n\r\n'.format(userAgent)
    s.send(request.encode('utf-8'))

    # Reading the response using makefile helper function which hides the loop for response reading, 
    # makefile returns a file like object containing every byte received from the server 
    response = s.makefile('r', encoding='utf-8', newline='\r\n')

    # splitting the response into pieces 
    statusline = response.readline()
    version, status, explanation = statusline.split(' ', 2)
    assert status == '200', '{}: {}'.format(status, explanation)

    # splitting the header line 
    headers = {}
    while True:
        line = response.readline()
        if line == '\r\n' : break
        header, value = line.split(':', 1)
        headers[header.lower()] = value.strip() #normalize header to lower case and strip leading and trailing while spaces

    # assuring some kind of header are no present
    """
    Go further: 
     The Content-Encoding header lets the server compress web pages before sending them. Large, text-heavy web pages compress well, and as a result the page loads faster. The browser needs to send an Accept-Encoding header in its request to list compression algorithms it supports. Transfer-Encoding is similar and also allows the data to be “chunked”, which many servers seem to use together with compression.
    """
    assert 'transfer-encoding' not in headers
    assert 'content-encoding' not in headers

    # get the message body
    body = response.read()
    s.close()

    return headers, body

# displaying the body of the html
def show(body):
    in_angle = False
    for c in body: 
        if c == '<':
            in_angle = True
        if c == '>': 
            in_angle = False
        elif not in_angle:
            print(c, end='')

# load a web page just by stringing together request and show:
def load(url):
    headers, body = request(url)
    show(body)

# load the browser from command line, reads the first argument from the command line as the url
if __name__ == "__main__":
    load(sys.argv[1])