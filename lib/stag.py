# -*- coding: utf-8 -*-

from glob import glob
from distutils.dir_util import copy_tree

from django.utils.feedgenerator import Atom1Feed

from lib.config import config, OUTPUT_PATH
from lib.post import Post
from lib.utils import write_template, feedify


class Stag(object):

    def post(self, argv):
        arg = ' '.join(argv)
        try:
            with open(arg, 'r'):
                post = Post.from_file(arg)
        except IOError:
            post = Post.from_title(arg)
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
            print("Writing index <%s> ..." % index.name)
            write_template(index, "index.html", recent_posts=posts[:config["n_posts"]])
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
        self.gen([])
        print("Deploying ...")
        copy_tree(OUTPUT_PATH, config["deploy_path"])
        print("Deployment done.")
