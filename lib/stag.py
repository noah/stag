# -*- coding: utf-8 -*-

from shutil import copy2 as cp
from os.path import join
from glob import glob
from distutils.dir_util import copy_tree

from django.utils.feedgenerator import Atom1Feed

from lib.config import config, BASE_PATH, OUTPUT_PATH, TEMPLATE_PATH, STAG_PATH, N_POSTS
from lib.post import Post
from lib.utils import write_template, feedify, mkdir_p


class Stag(object):

    def init(self, argv):
        mkdir_p(join( BASE_PATH, "_output"))
        mkdir_p(join( BASE_PATH, "_posts"))
        mkdir_p(join( BASE_PATH, "_assets"))
        mkdir_p(join( BASE_PATH, "_templates"))
        cp(join(STAG_PATH, "_templates", "index.html"), TEMPLATE_PATH)
        cp(join(STAG_PATH, "_templates", "archive.html"), TEMPLATE_PATH)
        cp(join(STAG_PATH, "_templates", "base.html"), TEMPLATE_PATH)
        cp(join(STAG_PATH, "_templates", "post.html"), TEMPLATE_PATH)
        cp(join(STAG_PATH, "_templates", "post.skel"), TEMPLATE_PATH)
        cp(join(STAG_PATH, "stag.default.cfg"), join(BASE_PATH, "stag.cfg"))
        open(join(TEMPLATE_PATH, "ga.js"), 'w')

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
        for post in self.posts():
            print(post)

    # generate the site
    def gen(self, args):
        # TODO generalize
        posts = self.posts()
        with open(config["index_path"], mode="w+b") as index:
            print("Writing index <%s> (%s most recent posts) ..." % (index.name, N_POSTS))
            write_template(index, "index.html", recent_posts=posts[:N_POSTS])
        print("Writing posts ...")
        for post in posts:
            with open(post.output_path, mode="w+b") as op:
                write_template(op, "post.html", post=post)
        with open(config["archive_path"], mode="w+b") as archive:
            print("Writing archive <%s>" % archive.name)
            write_template(archive, "archive.html", posts=posts)
        print("Writing ATOM feed ...")
        feed = Atom1Feed(**config["feed"])
        [feed.add_item(**feedify(post).__dict__) for post in posts]
        with open(config["feed"]["feed_url"], mode="w+b") as f:
            f.write(bytes(feed.writeString("UTF-8"), "utf-8"))
        print("Copying assets ...")
        copy_tree(config["assets_path"], OUTPUT_PATH)
        print("Generation done.")

    # reverse-chrono sorted list of Post objects
    def posts(self):
        s_posts = sorted(glob("%s/*.md" % config["posts_path"]), reverse=True)
        return [Post.from_file(path=p) for p in s_posts]

    # deploy the site
    def deploy(self, args):
        print(config["deploy_path"])
        self.gen([])
        print("Deploying ...")
        copy_tree(OUTPUT_PATH, config["deploy_path"])
        print("Deployment done.")
