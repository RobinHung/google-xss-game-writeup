class MainPage(webapp.RequestHandler):

  def render_template(self, filename, context={}):
    path = os.path.join(os.path.dirname(__file__), filename)
    self.response.out.write(template.render(path, context))

  def get(self):
    # Disable the reflected XSS filter for demonstration purposes
    self.response.headers.add_header("X-XSS-Protection", "0")

    if not self.request.get('timer'):
      # Show main timer page
      self.render_template('index.html')
    else:
      # Show the results page
      timer= self.request.get('timer', 0)
      self.render_template('timer.html', { 'timer' : timer })

    return

application = webapp.WSGIApplication([ ('.*', MainPage), ], debug=False)
