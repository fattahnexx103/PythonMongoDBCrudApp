import uuid
import datetime
from database import Database
from entities.post import Post

__author__ = 'neehad'


class Blog(object):
    #the __init__ is like the constructor and we set all the varaibles
    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id #we encode the id and make it random if it is null else we go with normal id

    #this makes a new post
    def new_post(self):
        #prompts user for name and other info related to make a post
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        date = input("Enter post date, or leave blank for today (in format DDMMYYYY): ")
        if date == "": #if user leaves date blank, system uses system date by default
            date = datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, "%d%m%Y") #this trims the system date
        #we make a new post object with the info
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date)
        post.save_to_mongo() #we save it to the database

    #retrieve the post from database
    def get_posts(self):
        return Post.from_blog(self.id)

    #we save the post object in the database in the collection of blogs and as json data
    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    #we make json data using the variables
    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'id': self.id
        }
    #getting post using id
    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'id': id}) #use the database methods to find it and return a blog object and set the data
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   id=blog_data['id'])
