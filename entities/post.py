import uuid
from database import Database
import datetime

__author__ = 'neehad'

#create the post object
class Post(object):

    #this is the constructor
    def __init__(self, blog_id, title, content, author, date=datetime.datetime.utcnow(), id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = date
        self.id = uuid.uuid4().hex if id is None else id #if the id is None then do a new one else just id

    def save_to_mongo(self):
        Database.insert(collection='posts', #name of collection is posts and data is the json data
                        data=self.json())

   #define the json object
    def json(self):
        return {
            'id': self.id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id): #take in a post class with the id and look it up
        post_data = Database.find_one(collection='posts', query={'id': id}) #find the entry
        return cls(blog_id=post_data['blog_id'], #return the object
                   title=post_data['title'],
                   content=post_data['content'],
                   author=post_data['author'],
                   date=post_data['created_date'],
                   id=post_data['id'])

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
