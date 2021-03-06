import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

#@app.route('/')
#def index():
    # Articles are pages with a publication date
#    articles = (p for p in pages if 'published' in p.meta)
    # Show the 10 most recent articles, most recent first.
#    latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
#    return render_template('articles.html', articles=latest[:10])

@app.route('/category/<string:category>/')
def category(category):
    categories = [p for p in pages if category in p.meta.get('category', [])]
    return render_template('category.html', pages=categories, category=category)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=3000)
