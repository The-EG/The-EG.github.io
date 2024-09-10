from . import rst_html5
from . import directives

def register():
    rst_html5.register()
    directives.register()

