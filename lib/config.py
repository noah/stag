# -*- coding: utf-8 -*-

import os
import shlex

BASE_PATH   = os.path.dirname(os.path.dirname(__file__))
OUTPUT_PATH = os.path.join(BASE_PATH, "_output")

config = {
    # how many posts to show in the index?
    "n_posts"       :   1,
    "site_title"    :   "openmind",
    "editor"        :   shlex.split("vim -O -c 'set ft=markdown' +/^$ '+normal j'"),
    "meta_date_fmt" :   "%Y-%m-%d %H:%M:%S",
    #
    "deploy_path"   :   "/srv/http/vhosts/blog.0x7be.org",
    #
    # you probably won't have to change anything below this line
    #
    "posts_path"    :   os.path.join(BASE_PATH, "_posts"),
    "template_path" :   os.path.join(BASE_PATH, "_templates"),
    "assets_path"   :   os.path.join(BASE_PATH, "_assets"),
    #
    "index_path"    :   os.path.join(OUTPUT_PATH, "index.html"),
    "archive_path"  :   os.path.join(OUTPUT_PATH, "archive.html"),
}
