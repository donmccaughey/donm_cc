from datetime import datetime
from flask import Flask, render_template
from news import Cache, Items, URL
from pathlib import Path
from urllib.parse import urlsplit

app = Flask(__name__)
app.config.from_prefixed_env()

news_path = Path(app.config['NEWS_PATH'])
cache = Cache(news_path)


@app.route('/')
def home():
    items = Items.from_json(cache.get() or Items().to_json())
    return render_template('home.html', items=items, now=datetime.now())


@app.template_filter()
def format_date_time(value: datetime) -> str:
    return value.strftime('%Y-%m-%d %H:%M:%S')


@app.template_filter()
def domain(value: URL) -> str:
    parts = urlsplit(value.url)
    hostname_parts = parts.hostname.split('.')
    if len(hostname_parts) > 2 and 'www' == hostname_parts[0]:
        del hostname_parts[0]
    return '.'.join(hostname_parts)