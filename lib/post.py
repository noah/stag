# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
import codecs
from glob import glob
from datetime import datetime
from shutil import copy
from tempfile import NamedTemporaryFile
from subprocess import call

from django.template.defaultfilters import slugify
import markdown

from lib.config import config, OUTPUT_PATH
from lib.utils import post_path, hash, write_template, flatten_meta, meta_date


# This class uses the alternate constructor (aka factory) pattern
# See e.g.,
# http://jjinux.blogspot.com/2008/11/python-class-methods-make-good.html
#
# This is a good pattern because it allows one to enforce multiple,
# flexible constructors, without needing to branch on arguments.
#
# i.e., one does not need to write code like this
#   if kwargs['this']:      Post(some args)
#   elif kwargs['that']:    Post(some different args)
#
# @classmethod means one can call Post.whatever without having to
# initialize a post object first.

PATH_RE = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>.+).md")

class Post(object):


    def __init__(self):
        self.now        = datetime.now()
        self.created    = meta_date(self.now)

    # Create Post object from existing file
    @classmethod
    def from_file(klass, path):
        self        = klass()
        # compute some attributes from the filename
        self.path   = path
        try:
            with codecs.open(self.path, 'r', 'utf-8') as f:
                # run post file through the markdown parser
                mdown           = markdown.Markdown(extensions=["meta",
                    "codehilite(linenums=False)", "toc"])
                self.text       = f.read()
                self.html       = mdown.convert(self.text)
                self.wc         = len(self.html.split(None))
                meta            = flatten_meta(mdown.Meta)
                # s/self.meta.x/self.x/
                for k, v in meta.items(): self.__dict__[k] = v

                if(type(self.tags)) is str:
                    self.tags = [self.tags]

                # We now have the metadata from the post file, and some
                # computed values from the filename: validate.
                self.validate()

                self.permalink      = '-'.join([self.year, self.month, self.day, self.slug]) + ".html"
                self.output_path    = os.path.join(OUTPUT_PATH, self.permalink)
        except IOError:
            print("Invalid path: %s" % (self.path), file=sys.stderr)
            raise
        return self

    # Create Post object from a given title (computed slug).  Create
    # file from template if necessary.
    @classmethod
    def from_title(klass, title, text=''):
        self        = klass()
        self.title  = title
        self.text   = text
        self.slug   = slugify(self.title)
        self.path   = post_path(self.now, self.slug)
        post        = None
        try:
            with codecs.open(self.path, 'r', 'utf-8'): pass
            # post exists; edit it and return Post
            call(config["editor"] + [self.path])
            post = Post.from_file(self.path)
        except IOError:
            # post does not exist.  create named temporary file.  write
            # evaluated template to temporary file.  hash file. launch editor on
            # temporary file.  re-hash.  if hashes differ, temporary
            # file has changes so copy temporary file to self.path and
            # return Post else return None
            with NamedTemporaryFile(suffix=".md", mode="w+b") as tempfile:
                write_template(tempfile, 'post.skel', **self.__dict__)

                if len(text) < 1: # text not set in client
                    # editor path
                    before = hash(tempfile)
                    call(config["editor"] + [tempfile.name])
                    after = hash(tempfile)
                    if before != after:
                        copy(tempfile.name, self.path)
                        post = Post.from_file(self.path)
                    else:
                        print("No changes made.")
                else:
                    # client set text
                    copy(tempfile.name, self.path)
                    post = Post.from_file(self.path)
                    call(config["editor"] + [self.path])
        return post

    # Create Post object from slug(ish) argument.  Can be a globbing
    # pattern.
    @classmethod
    def from_slugish(klass, slugish):
        self = klass()
        for match in glob(os.path.join( config["posts_path"], slugish)):
            self.path = match
            try:
                # post exists; edit it and return Post
                with codecs.open(self.path, 'r', 'utf-8'): pass
                call(config["editor"] + [self.path])
                post = Post.from_file(self.path)
            except IOError:
                pass

    def __str__(self):
        return "%s (%s)" % (self.now, self.slug)

    def validate(self):
        m = PATH_RE.match(os.path.basename(self.path))

        if m is None:
            print("invalid slug:", self.path, file=sys.stderr)
            raise ValueError

        if None in m.group('year', 'month', 'day', 'slug'):
            print("verify that post file basename matches YYYY-MM-DD-slug.md",
                  self.path,
                  file=sys.stderr)
            raise ValueError

        self.year, self.month, self.day = m.group('year', 'month', 'day')
        # note: self.slug is set "blindly" in the for loop in from_file
        # or via slugify() in from_title

        if self.slug != m.group('slug'):
            print("verify that filename slug matches metadata slug",
                  self.path,
                  file=sys.stderr)
            raise ValueError

        parse_date = lambda d: datetime.strptime(d,
                                    config["meta_date_fmt"])#.strftime(config["meta_date_fmt"])

        self.created = parse_date(self.created)

        # not all posts are edited
        try:
            self.edited = parse_date(self.edited)
        except ValueError:
            self.edited = None
