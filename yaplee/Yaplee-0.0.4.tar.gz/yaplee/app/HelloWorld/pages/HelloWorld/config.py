from yaplee.template import PageController as Controller

page = Controller(page_name='HelloWorld')

# Your page sections are here
SECTIONS = [
    page.Section(name='Main')
]

# Your page template are here
TEMPLATES = [
    page.Template(path='index.html', section='Main')
]

# Your page template static files are here
STATICS = [
    page.Static(path='style.css', section='Main')
]

# Your sections want to register are here
page.Register('Main', url='')