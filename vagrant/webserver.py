from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

          if self.path.endswith("/restaurants"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h1>restaurants</h1>"
              output += "<h2><a href='/restaurants/new'>Make a new restaurant here</a></h2><br>"
              restaurants = session.query(Restaurant).all()
              for i in restaurants:
                output += i.name
                output += "<br>"
                output += "<a href ='/restaurants/%s/edit'>Edit </a> <br>" % i.id
                output += "<a href='/restaurants/%s/delete'>Delete</a><br>" %i.id
                output += "<br>"
              output += "</body></html>"
              self.wfile.write(output)
              #print output
              return

          if self.path.endswith("/restaurants/new"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h2>Make a new restaurant</h2>"
              output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name'><input type='submit' value='Create'> </form>"
              output += "</body></html>"
              self.wfile.write(output)
              #print output
              return

          if self.path.endswith("/edit"):
              restaurantID = self.path.split("/")[2]
              editRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
              if editRestaurant:
                  self.send_response(200)
                  self.send_header('Content-type', 'text/html')
                  self.end_headers()
                  output = "<html><body>"
                  output += "<h1>"
                  output += editRestaurant.name
                  output += "</h1>"
                  output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantID
                  output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % editRestaurant.name
                  output += "<input type = 'submit' value = 'Rename'>"
                  output += "</form>"
                  output += "</body></html>"

                  self.wfile.write(output)
              #print output
              return

          if self.path.endswith("/delete"):
              restaurantIDPath = self.path.split("/")[2]

              deleteRestaurant = session.query(Restaurant).filter_by(
                  id=restaurantIDPath).one()
              if deleteRestaurant:
                  self.send_response(200)
                  self.send_header('Content-type', 'text/html')
                  self.end_headers()
                  output = ""
                  output += "<html><body>"
                  output += "<h1>Are you sure you want to delete %s?" % deleteRestaurant.name
                  output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                  output += "<input type = 'submit' value = 'Delete'>"
                  output += "</form>"
                  output += "</body></html>"
                  self.wfile.write(output)

          if self.path.endswith("/hello"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h1>Hello!</h1>"
              output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
              output += "</body></html>"
              self.wfile.write(output)
              #print output
              return

          if self.path.endswith("/hola"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h1>&#161 Hola !</h1>"
              output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
              output += "</body></html>"
              self.wfile.write(output)
              #print output
              return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
          if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
              fields = cgi.parse_multipart(self.rfile, pdict)
              print fields
              messagecontent = fields.get('newRestaurantName')
              print messagecontent
              newRestaurant = Restaurant(name = messagecontent[0])
              print newRestaurant
              restaurantID = self.path.split("/")[2]
              print restaurantID
              editRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
              print editRestaurant
              if editRestaurant != []:
                editRestaurant.name = messagecontent[0]
                session.add(editRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
              

          if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
              fields = cgi.parse_multipart(self.rfile, pdict)
              restaurantID = self.path.split("/")[2]
              messagecontent = fields.get('newRestaurantName')
              newRestaurant = Restaurant(name = messagecontent[0])
              session.add(newRestaurant)
              session.commit()

              self.send_response(301)
              self.send_header('Content-type', 'text/html')
              self.send_header('Location', '/restaurants')
              self.end_headers()

          if self.path.endswith("/delete"):
              restaurantID = self.path.split("/")[2]
              deleteRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
              if deleteRestaurant:
                  session.delete(deleteRestaurant)
                  session.commit()
                  self.send_response(301)
                  self.send_header('Content-type', 'text/html')
                  self.send_header('Location', '/restaurants')
                  self.end_headers()
#            ctype, pdict = cgi.parse_header(
#               self.headers.getheader('content-type'))
#            if ctype == 'multipart/form-data':
#                fields = cgi.parse_multipart(self.rfile, pdict)
#                messagecontent = fields.get('message')
#            output = ""
#            output += "<html><body>"
#            output += " <h2> Okay, how about this: </h2>"
#            output += "<h1> %s </h1>" % messagecontent[0]
#            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
#            output += "</body></html>"
#            self.wfile.write(output)
#            #print output
        except Exception as e:
            print e


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()