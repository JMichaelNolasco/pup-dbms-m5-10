import json
import os
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
import webapp2
import json



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
    year= ndb.StringProperty()
    created_by = ndb.KeyProperty(repeated=True)
    created_by_email = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section= ndb.StringProperty()
    author= ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    email= ndb.StringProperty()
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    phone_number= ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    





class LoginPage(webapp2.RequestHandler):
    def get(self):
             
        loggedin_user = users.get_current_user()
        if loggedin_user:
            user_key = ndb.Key('User', loggedin_user.user_id())
            user=user_key.get()
            if user:
                thesis=Thesis()
                user_key=thesis.created_by         
                self.redirect('/home')
            else:
                self.redirect('/register')               
        else:
              template = JINJA_ENVIRONMENT.get_template('login.html')
     
              login=users.create_login_url(self.request.uri)
              template_values = {
                'login' :login,      
              }
              self.response.write(template.render(template_values))


      


class RegisterPage(webapp2.RequestHandler):
    def get(self):
               
        loggedin_user = users.get_current_user()
        if loggedin_user:
            user_key = ndb.Key('User', loggedin_user.user_id())
            user=user_key.get()
            if user:
                thesis=Thesis()
                user_key=thesis.created_by
                self.redirect('/home')
            else:
                template = JINJA_ENVIRONMENT.get_template('register.html')
                user_email=users.get_current_user().email() 
                template_values = {
                    'user_email': user_email          
                }
                self.response.write(template.render(template_values))
        else:
            self.redirect('/login')           
            
    def post(self):
        loggedin_user=users.get_current_user()
        user = User(id=loggedin_user.user_id(),email=loggedin_user.email(),
                    first_name=self.request.get('first_name'),
                    last_name=self.request.get('last_name'),
                    phone_number=self.request.get('phone_number'))
        user.put()
        self.redirect('/')



class ThesisHandler(webapp2.RequestHandler):
    def get(self):
    
        # user = users.get_current_user()
        # if user:   
        #     url = users.create_logout_url('/login')         
        #     template = JINJA_ENVIRONMENT.get_template('home.html')
        #     url_linktext = 'Logout' + ' ' + users.get_current_user().email()  
        # else:
        #     url =  users.create_login_url('/home')
        #     url_linktext =  'Login'         
        # template_values = {
        #     'user': user,
        #     'url': url,
        #     'url_linktext': url_linktext
        # }
        loggedin_user = users.get_current_user()
        if loggedin_user:
            user_key = ndb.Key('User', loggedin_user.user_id())
            user=user_key.get()
            if user:
                template = JINJA_ENVIRONMENT.get_template('home.html')
                url = users.create_logout_url('/login') 
                url_linktext = 'Logout' + ' ' + users.get_current_user().email()
                template_values = {
                   'url': url,
                   'url_linktext': url_linktext
                }
                self.response.write(template.render(template_values))  
            else:
                self.redirect('/register')
        else:
            self.redirect('/login')  
     
        

    def post(self):
        thesis =Thesis()
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.put()
        self.redirect('/')



class ThesisAPI(webapp2.RequestHandler):
    
    def get(self):
        CpE_Thesis= Thesis.query().order(-Thesis.date).fetch()

        thesis_list=[]
        for thesis in CpE_Thesis:
            thesis_list.append ({
                'id': thesis.key.id(),  
                'year' : thesis.year,
                'title': thesis.title,
                'author': thesis.author,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
              
            })
        response = {
            'result' :'OK' ,
            'data' : thesis_list          
        }
      
        self.response.headers['Content-type'] = 'app/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()
        
        
      
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.author=users.get_current_user().nickname()
        thesis.section = self.request.get('section')
        thesis.put()


        response = {
            'result': 'OK',
            'data':{
                             
                'year' : thesis.year,
                'title': thesis.title,
                'author':thesis.author,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section

            }
        }
        self.response.out.write(json.dumps(response))

class UsersAPI(webapp2.RequestHandler):
    
    def get(self):
        Users= User.query().order(-Thesis.date).fetch()

        users_list=[]
        for user in Users:
            users_list.append ({
                # 'user_id': user.key.id(),  
                # 'email': user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'phone_number': user.phone_number
                
              
            })
        response = {
            'result' :'OK' ,
            'data' : users_list          
        }
      
        self.response.headers['Content-type'] = 'app/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        loggedin_user=users.get_current_user()
        user = User()
        user.first_name=self.request.get('first_name')
        user.last_name=self.request.get('last_name')
        user.phone_number=self.request.get('phone_number')
                  
        user.put()


        response = {
            'result': 'OK',
            'data':{
                             
                # 'user_id': user.id,  
                # 'email': user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'phone_number': user.phone_number

            }
        }
        self.response.out.write(json.dumps(response))


class ThesisDelete(webapp2.RequestHandler):
   
       
    def get(self,id):
       
        
        thesis_key = Thesis.get_by_id(int(id))
        thesis_key.key.delete()
        
        self.redirect('/')
        
       
class ThesisEdit(webapp2.RequestHandler):
    def get(self,id):
        template = JINJA_ENVIRONMENT.get_template('t.html')
        self.response.write(template.render())
        
        CpE_Thesis = Thesis.query().order(-Thesis.date).fetch()
        thesis_id = int(id)

        response = {
            'CpE_Thesis': CpE_Thesis,
            'id':thesis_id
        }

        self.response.write(template.render(response))

 
      

    def post(self,id):
        thesis_id = int(id)    
        thesis = Thesis.get_by_id(thesis_id)
        # thesis.created_by = users.get_current_user().user_id()
       
        thesis.year = self.request.get('year')
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.put()
        self.redirect('/home')

app = webapp2.WSGIApplication([

    ('/api/thesis', ThesisAPI),
    ('/api/user', UsersAPI),
    ('/thesis/delete/(\d+)', ThesisDelete),
    ('/login', LoginPage),
    ('/thesis/edit/(\d+)',ThesisEdit),
    ('/home', ThesisHandler),
    ('/', ThesisHandler),
    ('/register',RegisterPage)
    
    
], debug=True)


