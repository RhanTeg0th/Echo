import os, socket, sys, bookdb


defaults = ['',2600]





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

INDEX = """

<html>

<head>

    <title>Index Page</title>

    <script type="text/javascript">

     function redirect()
     
      {
        location.replace("http://localhost:2600/books.html");
      }	
    </script>

    

<head>

<body>

<button onclick="redirect()">Click here to goto the book database listings</button>


</body>

</html>

"""

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


B = bookdb.BookDB(database,linklist)


def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
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

def get_content(uri):
    print 'fetching:', uri
    try:
                
        if uri.endswith('books.html'):
            return (200, get_mime(uri), get_page(B))
        
        if(uri.endswith('/')):
            return (200, 'text/html', INDEX)
            
        else: return (404, uri)              
            
    
    except IOError, e:
        return (404, e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):
    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host,port)
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            send_response(stream, get_content(get_request(stream)) )
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()
