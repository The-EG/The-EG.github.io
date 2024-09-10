AUTHOR = 'Taylor Talkington'
SITENAME = 'Musings of an Evil Genius'
SITEURL = ""

PATH = "."
ARTICLE_PATHS = ['posts']
STATIC_PATHS = ['assets']

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'English'

DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['egblog']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'theme'
