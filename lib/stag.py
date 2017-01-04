# -*- coding: utf-8 -*-

from os import path
from glob import glob
from shutil import copy2 as cp
from distutils.dir_util import copy_tree
from operator import attrgetter

from django.utils.feedgenerator import Atom1Feed

from lib.config import config, BASE_PATH, OUTPUT_PATH, TEMPLATE_PATH, STAG_PATH, N_POSTS
from lib.post import Post
from lib.utils import write_template, feedify, mkdir_p


class Stag(object):

    def init(self, argv):
        mkdir_p(path.join( BASE_PATH, "_output"))
        mkdir_p(path.join( BASE_PATH, "_posts"))
        mkdir_p(path.join( BASE_PATH, "_assets"))
        mkdir_p(path.join( BASE_PATH, "_templates"))
        cp(path.join(STAG_PATH, "_templates", "index.html"), TEMPLATE_PATH)
        cp(path.join(STAG_PATH, "_templates", "archive.html"), TEMPLATE_PATH)
        cp(path.join(STAG_PATH, "_templates", "base.html"), TEMPLATE_PATH)
        cp(path.join(STAG_PATH, "_templates", "post.html"), TEMPLATE_PATH)
        cp(path.join(STAG_PATH, "_templates", "post.skel"), TEMPLATE_PATH)
        cp(path.join(STAG_PATH, "stag.default.cfg"), path.join(BASE_PATH, "stag.cfg"))
        open(path.join(TEMPLATE_PATH, "ga.js"), 'w')

    def post(self, title, text=''):
        arg = ' '.join(title)
        try:
            with open(arg, 'r'):
                post = Post.from_file(arg)
        except Exception:
            try:
                post = Post.from_slugish(arg)
                assert post is not None
            except Exception:
                post = Post.from_title(arg, text)
        return post

    # list posts
    def ls(self, args):
        posts = self.posts()
        print("{} posts".format(len(posts)))
        for post in posts:
            print(post)

    # generate the site
    def gen(self, args):
        # TODO generalize
        posts = self.posts()
        with open(config["index_path"], mode="w") as index:
            print("Writing index <%s> (%s most recent posts) ..." % (index.name, N_POSTS))
            write_template(index, "index.html", recent_posts=posts[:N_POSTS])
        print("Writing posts ...")
        for post in posts:
            with open(post.output_path, mode="w") as op:
                write_template(op, "post.html", post=post)
        with open(config["archive_path"], mode="w") as archive:
            print("Writing archive <%s>" % archive.name)
            write_template(archive, "archive.html", posts=posts)
        print("Writing ATOM feed ...")
        feed = Atom1Feed(**config["feed"])
        [feed.add_item(**feedify(post).__dict__) for post in posts]
        with open(config["feed"]["feed_url"], mode="w") as f:
            f.write(feed.writeString("UTF-8"))
        print("Copying assets ...")
        copy_tree(config["assets_path"], OUTPUT_PATH)
        print("Generation done.")

    # list of Post objects
    def posts(self, sortby='created', reverse=True):
        s_posts = glob(path.join(config["posts_path"], "*.md"))
        return sorted([Post.from_file(path=p) for p in s_posts],
                      key=attrgetter(sortby), reverse=reverse)

    # deploy the site
    def deploy(self, args):
        print(config["deploy_path"])
        self.gen([])
        print("Deploying ...")
        copy_tree(OUTPUT_PATH, config["deploy_path"])
        print("Deployment done.")
