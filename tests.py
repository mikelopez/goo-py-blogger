import unittest
import sys
import logging
"""
Marcos Lopez - dev@scidentify.info 
this test does not go through posting to your blog. 
"""

class TestBlogger(unittest.TestCase):

  blogger = None
  username = ""
  password = ""

  def test_basic(self):
    """ test basic init of this class """
    sys.path.append('.')
    log = logging.getLogger("TestBlogger.test_basic")

    from googleBlogger import *
    self.blogger = GoogleBlogger()
    self.assertTrue(self.blogger)
    self.blogger.user = self.username
    self.blogger.password = self.password

    self.assertEquals(getattr(self.blogger, 'scope'), 'http://www.blogger.com/feeds')
    self.assertEquals(getattr(self.blogger, 'service'), 'blogger')

    login_result = self.blogger.BloggerLogin()

    if not login_result:
      raise AssertionError("Login returned false, check authentication")

    log.info('Getting blogs')
    b = self.blogger.BloggerGetBlogs()

    if len(b.entry) < 1:
      log.info('Less than 1 blog returned. Might be new account')
    else:
      log.info('Blogs found')
      blogs = []
      for feed in b.entry:
        log.info('-- Blog: %s' % feed.title.text)
        blogid = feed.GetSelfLink().href.split('/')[-1]
        blogs.append({
          'blogname': feed.title.text, 'blogid': blogid,
        })


if __name__ == '__main__':
  logging.basicConfig(stream=sys.stdout)
  logging.getLogger("TestBlogger.test_basic").setLevel(logging.INFO)

  unittest.main()
