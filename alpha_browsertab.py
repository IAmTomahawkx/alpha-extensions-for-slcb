class BrowserTab:
  def __init__(self, icon_string, tab_title, url):
    self.icon = icon_string
    self.title = tab_title
    self.url = url
  def register(self): pass
  def unload(self): pass