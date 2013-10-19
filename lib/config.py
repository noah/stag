# -*- coding: utf-8 -*-

from os import getcwd
from os.path import join
from os.path import dirname
import shlex

# IT PROBABLY WON'T BE NECESSARY TO CHANGE THE FOLLOWING

STAG_PATH       = dirname(dirname(__file__))
BASE_PATH       = getcwd()
OUTPUT_PATH     = join(BASE_PATH, "_output")
TEMPLATE_PATH   = join(BASE_PATH, "_templates")

import configparser
userconfig  = configparser.RawConfigParser()
result      = userconfig.read(join(BASE_PATH, "stag.cfg"))

DEPLOY_PATH = TAGLINE = TITLE = URL = AUTHOR = EMAIL = DISQUS_SHORTNAME = ''
N_POSTS = 1

if result == []:
    print("Please configure stag.cfg")
else:
    TAGLINE             = userconfig["stag"]["tagline"]
    TITLE               = userconfig["stag"]["title"]
    URL                 = userconfig["stag"]["url"]
    AUTHOR              = userconfig["stag"]["author"]
    EMAIL               = userconfig["stag"]["email"]
    DEPLOY_PATH         = join( BASE_PATH, userconfig["stag"]["deploy_path"] )
    DISQUS_SHORTNAME    = userconfig["stag"]["disqus_shortname"]
    N_POSTS             = int( userconfig["stag"]["n_posts"] )


try:
    GOOGLE_ANALYTICS = open(join(TEMPLATE_PATH, "ga.js"), 'r').read()
except:
    GOOGLE_ANALYTICS = ''

config = {
    "site_tagline"  :   TAGLINE,
    "site_title"    :   TITLE,
    "site_url"      :   URL,
    "editor"        :   shlex.split("vim -O -c 'set ft=markdown' +/^$ '+normal j'"),
    "meta_date_fmt" :   "%Y-%m-%d %H:%M:%S",
    #
    "deploy_path"   :   DEPLOY_PATH,
    "ga"            :   GOOGLE_ANALYTICS,
    #
    "posts_path"    :   join(BASE_PATH, "_posts"),
    "template_path" :   TEMPLATE_PATH,
    "assets_path"   :   join(BASE_PATH, "_assets"),
    #
    "index_path"    :   join(OUTPUT_PATH, "index.html"),
    "archive_path"  :   join(OUTPUT_PATH, "archive.html"),
    "disqus_shortname" : DISQUS_SHORTNAME,
    #
    "feed"          : {
        # -> django.utils.feedgenerator.SyndicationFeed mappings
        "title"         :   TITLE,
        "link"          :   URL,
        "description"   :   TAGLINE,
        "author_name"   :   AUTHOR,
        "author_email"  :   EMAIL,
        "feed_url"      :   join(OUTPUT_PATH, TITLE + ".atom"),
        "language"      : "en",
    },
}
