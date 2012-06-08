#
# ws30 -- the thirty minute web server
# author: Wilhelm Fitzpatrick (rafial@well.com)
# date: August 3rd, 2002
# version: 1.0
#
# Written after attending a Dave Thomas talk at PNSS and hearing about
# his "write a web server in Ruby in one hour" challenge.
#
# Actual time spent:
#  30 minutes reading socket man page
#  30 minutes coding to first page fetched
#   3 hours making it prettier & more pythonic
#
# updated for UW Internet Programming in Python, by Brian Dorsey
# updated by Jon Jacky: in defaults, replace '127.0.0.1' with ''
#  to allow connection from other hosts besides localhost
#

import os, socket, sys, datetime, bookdb

defaults = ['', 8080]  # '127.0.0.1' here limits connections to localhost
mime_types = {'.jpg' : 'image/jpg', 
             '.gif' : 'image/gif', 
             '.png' : 'image/png',
             '.html' : 'text/html', 
             '.pdf' : 'application/pdf'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""

DIRECTORY_LINE = '<a href="%s">%s</a><br>'

database = ['CherryPy Essentials: Rapid Python Web Application Development',
             'Python for Software Design: How to Think Like a Computer Scientist',
             'Foundations of Python Network Programming',
             'Python Cookbook, Second Edition',
             'The Pragmatic Programmer: From Journeyman to Master'
            ]


linklist = ["http://www.amazon.com/CherryPy-Essentials-Application-Development-applications/dp/1904811841/ref=sr_1_1?ie=UTF8&qid=1331064225&sr=8-1",
             "http://www.amazon.com/Python-Software-Design-Computer-Scientist/dp/0521725968/ref=sr_1_1?s=books&ie=UTF8&qid=1331064398&sr=1-1",
             "http://www.amazon.com/Foundations-Python-Network-Programming-comprehensive/dp/1430230037/ref=sr_1_1?s=books&ie=UTF8&qid=1331066930&sr=1-1",
             "http://www.amazon.com/Python-Cookbook-Alex-Martelli/dp/0596007973/ref=sr_1_2?s=books&ie=UTF8&qid=1331067146&sr=1-2",
             "http://www.amazon.com/Pragmatic-Programmer-Journeyman-Master/dp/020161622X/ref=sr_1_1?s=books&ie=UTF8&qid=1331067260&sr=1-1"
             ]


LISTLINE1 = '<p style="color:blue"><a href='


LISTLINE2 = '</a></p>'

BOOK_LISTING1 = """

<html>

<head>

    <title>Bookpage</title>

</head>

<body>

<h1>Book Listings:</h1>

"""

BOOK_LISTING2 = """

</body>

</html>

"""



def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(1)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method = None
    while True:
        line = stream.readline()
        print line
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
    return uri

def list_directory(uri):
    entries = os.listdir('.' + uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))

def get_file(path):
    f = open(path)
    try: 
        return f.read()
    finally: 
        f.close()

def get_page(bookdb):
    LISTLINES = []
    page = BOOK_LISTING1
    T = bookdb.titles()
    L = bookdb.links()
    i = 0
    while i < 5:
        entry = LISTLINE1 + L[i] + '>' + T[i] + LISTLINE2
        LISTLINES.append(entry)
        i = i + 1
    for k in range(len(LISTLINES)):
        page = page + LISTLINES[k]

    Page = page + BOOK_LISTING2
    return Page



def get_content(uri,bookdb):
    print 'fetching:', uri
    try:
        path = '.' + uri
        if(uri.endswith('/date.html')):
            return (200, '/date.html', datetime.datetime.now())
        if(uri.endswith('/books.html')):
            return (200, '/books.html', get_page(bookdb))
        if os.path.isfile(path):
            return (200, get_mime(uri), get_file(path))
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri))
            else:
                return (301, uri + '/')
        else: return (404, uri)
    except IOError, e:
        return (404, e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    B = bookdb.BookDB(database,linklist)
    args, nargs = sys.argv[1:], len(sys.argv)-1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host,port)
   
        
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            send_response(stream, get_content(get_request(stream),B))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

