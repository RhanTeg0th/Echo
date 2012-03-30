import os, socket, sys, cgi, bookdb, Login , urllib , urlparse

import cgitb
cgitb.enable(display=0, logdir="/tmp")


defaults = ['localhost',2600]

size = 1024


U = "WebBookDBadmin"

P = "r1ng0st4rr"


PATH = 'http://localhost:2600/'




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
                

<head>

<body>

<h1>Bookdb admin login: </h1>



<form action="/tmp" method="get">

Username: <input type="text" name="user" /> </br> 

Password: <input type="text" name="pswd" />

<input type="submit" value="Submit"/>



</form>





</body>

</html>

"""


REINDEX = """

<html>

<head>

    <title>Index Page</title>

    <script type="text/javascript">

     function loginerror()
    
      {
         alert("Login info incorrect! Please resubmit.");
      }
      
    </script>

 
<head>

<body onload="loginerror()">

<h1>Bookdb admin login: </h1>

<form action="/tmp" method="get">

Username: <input type="text" name="user" /> </br> 

Password: <input type="text" name="pswd" />

    

<input type="submit" value="Submit" />



</form>




</body>

</html>

"""



REDIRECT = """

<html>

<head>

    <title>Index Page</title>
    
    <script type="text/javascript">

     function redirect()
     
      {
        location.replace("http://localhost:2600/");
      }	
    </script>

    
</head>

<body onload="redirect()">
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
    s.listen(3)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')
  
   

def get_bookpage(bookdb):
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

def get_mime(url):
         return mime_types.get(os.path.splitext(url)[1], 'text/plain')


def get_content(stream):

    loggedin = False

    Indxstr = ''
    loginstr = 'user=WebBookDBadmin&pswd=r1ng0st4rr HTTP/1.1'
    bookstr = '/books.html'
    

    line = stream.readline().strip()    
    url = urlparse.urlparse(line)
    
    print url
    
    print "fetching", url.query       
              
    try:

                   
        if(url.query==Indxstr):
            
            
             return (200, 'text/html', INDEX)        

        if(url.query!=Indxstr):
            

            if(url.query==loginstr):
                    
                    loggedin = True                
                   
                    return (200, get_mime('/books.html'),get_bookpage(B))
                

            if(url.query!=loginstr):
                

                   return (200,'text/html', REINDEX)
            

                   

        if(url.query==bookstr and loggedin==False):


               return (200,'text/html', REDIRECT)
            

        
                               
        
        else:

              return (404, url)              
            
    
    except IOError, e:
        return (404, e)



def send_response(content):
    stream.write(response[content[0]] % content[1:])
    

if __name__ == '__main__':

    
    L = Login.Login()
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host,port)
    print 'starting %s on %s...' % (host, port)
    
    try:
        while True:
            stream = listen (server)
            send_response(get_content(stream))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()
