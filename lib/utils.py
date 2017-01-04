# -*- coding: utf-8 -*-

import os
import errno
import hashlib
from datetime import datetime

from lib.config import config

from django.template import Context, Template
from django.conf import settings
from django import setup

settings.configure(
    TEMPLATES = [{
        'BACKEND'   : 'django.template.backends.django.DjangoTemplates',
        'DIRS'      : [
            config["template_path"],
        ],
    }])
setup()

def post_path(t, s):
    return '.'.join([os.path.join(config["posts_path"],
                        '-'.join([datetime.strftime(t, "%Y-%m-%d"), s])), 'md'])

def meta_date(t):
    return datetime.strftime(t, config["meta_date_fmt"])


def hash(fh):
    fh.seek(0) # be kind: rewind.
    return hashlib.md5(fh.read()).hexdigest()


def get_template(name):
    return open(os.path.join(config['template_path'], name), 'r').read()


def eval_template(name, **kwargs):
    c = Context(kwargs)
    c.update({'config' : config}) # make config available in templates
    return Template(get_template(name)).render(c)


def write_template(fh, template, **data):
    fh.write(eval_template(template, **data).encode('utf-8'))
    fh.flush()

def flatten_meta(m):
    # Markdown.Meta is a dict of lists.  This is not desirable for
    # key-value pairs with 1-element values.  So, flatten it unless
    # there are multiple values.
    for k, v in m.items():
        if len(m[k]) == 1:
            m[k] = v[0]
    return m


def feedify(post):
    # munge feed object into something django can work with
    post.description    = ''.join([post.html[:250], "..."])
    post.link           = '/'.join([config["site_url"], post.permalink])
    post.author_name    = config["feed"]["author_name"]
    post.author_email   = config["feed"]["author_email"]
    post.pubdate        = post.created
    if post.edited is not None:
        post.pubdate = post.edited

    return post

# http://stackoverflow.com/a/600612/67416
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
