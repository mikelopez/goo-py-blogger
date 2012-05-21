from gdata import service
import gdata
import atom

# old script from 2009 

class GoogleBlogger:
  """ a basic google API interface / blogger 
  Author: Marcos Lopez - dev@scidentify.info """

  blogger = ''
  user = ''
  password = ''
  next = 'https://next-url/'
  scope = 'http://www.blogger.com/feeds'
  source = 'app-source-name-1.0'
  service = 'blogger'
  server = 'www.blogger.com'
  account_type = 'GOOGLE'

  def __init__(self, username=None, password=None):
    """ login if passed username arg / password is optional"""
    if username:
      self.user = username
      if password:
        # use same pw or use arg password
        self.password = password
      self.BloggerLogin()

  def BloggerLogin(self):
    """ authenticate to blogger api """
    try:
      secure = False
      session = True
      self.blogger = service.GDataService(self.user, self.password)
      self.blogger.source = self.source
      self.blogger.service = self.service
      self.blogger.server = self.server
      self.blogger.account_type = self.account_type
      self.blogger.ProgrammaticLogin()
      return True
    except service.BadAuthentication:
      return False

  def BloggerGetBlogs(self):
    """ return list of blogs """
    query = service.Query()
    query.feed = '/feeds/default/blogs'
    feed = self.blogger.Get(query.ToUri())
    return feed

  def BloggerGetPosts(self, blogid):
    """ get blog posts for blogid """
    feed = self.blogger.GetFeed('/feeds/' + blogid + '/posts/default')

    return feed

  def BloggerPostBlog(self, blogid, title, content):
    """ post a blog as html content """
    entry = gdata.GDataEntry()
    entry.title = atom.Title('xhtml', title)
    entry.content = atom.Content(content_type='html', text=content)
    return self.blogger.Post(entry, '/feeds/%s/posts/default' % (blogid))




# main
if __name__ == '__main__':
  # init blogger class and login
  blog = googleBlogger()
  blog.BloggerLogin()
  blogs = []
  my_blogs = None

  # retrieve list of blogs
  my_blogs = blog.BloggerGetBlogs()
  for feed in my_blogs.entry:
    blogid = feed.GetSelfLink().href.split('/')[-1]
    blogs.append({
      'blogname':feed.title.text,
      'blogid':blogid,
    })


