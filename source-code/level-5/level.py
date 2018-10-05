class MainPage(webapp.RequestHandler):
  def render_template(self, filename, context={}):
    path = os.path.join(os.path.dirname(__file__), filename)
    self.response.out.write(template.render(path, context))

  def get(self):
    # Disable the reflected XSS filter for demonstration purposes
    self.response.headers.add_header("X-XSS-Protection", "0")

    # Route the request to the appropriate template
    if "signup" in self.request.path:
      self.render_template('signup.html',
        {'next': self.request.get('next')})
    elif "confirm" in self.request.path:
      self.render_template('confirm.html',
        {'next': self.request.get('next', 'welcome')})
    else:
      self.render_template('welcome.html', {})

    return

application = webapp.WSGIApplication([ ('.*', MainPage), ], debug=False)
