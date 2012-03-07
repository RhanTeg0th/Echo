"""
From Brian Dorsey's Internet Programming in Python, Winter 2011

Modified by Anton Feichtmeir, Winter 2012
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



class BookDB():

    def __init__(self, DB,hyperlinks):
        self.DB = database
        self.hyperlinks = linklist

    def titles(self):
        return self.DB

    def links(self):
        return self.hyperlinks        
        
    def title_info(self, id):
        return database[id]

    def get_title(self,id):
        T = self.titles()
        i = int(id)-1
        return T[i]
    
    def get_link(self,id):
        L = self.links()
        i = int(id)-1
        return L[i]





        


