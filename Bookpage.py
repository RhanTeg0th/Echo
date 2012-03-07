import sys
import socket
import bookdb

# let's pretend we're getting this information from a database somewhere


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



host = 'localhost'
port =2600
size = 1024


if len(sys.argv) > 1:
    port = int(sys.argv[1])




BOOK_LISTING1 = """

HTTP/1.0 200 Okay
Server: BookDB
Content-type: text/html


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


if __name__ == '__main__':

     B = bookdb.BookDB(database,linklist)
     bookpage = get_page(B)    
    
     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)     
     s.bind((host,port))

    

     print 'Server starting on port', port


     s.listen(1)

     while True:
          client,address = s.accept()
          client.recv(size)
          client.send(bookpage)                  
          s.close()
           



















