# -*- coding: utf-8 -*-

import os
import shlex

# YOU REALLY SHOULD CHANGE SITE_* !

SITE_TITLE              = "openmind"
SITE_TAGLINE            = "What was I thinking?"
SITE_URL                = "https://blog.tilton.co"
SITE_AUTHOR             = "Noah K. Tilton"
SITE_EMAIL              = "noah@tilton.co"
SITE_DEPLOY_PATH        = "/srv/http/vhosts/blog.tilton.co"
SITE_GOOGLE_ANALYTICS   = """
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-37603035-1']);
    _gaq.push(['_setDomainName', 'tilton.co']);
    _gaq.push(['_trackPageview']);
    (function() {
     var ga = document.createElement('script'); ga.type =
     'text/javascript'; ga.async = true;
     ga.src = ('https:' == document.location.protocol ?
       'https://ssl' : 'http://www') +
     '.google-analytics.com/ga.js';
     var s =
     document.getElementsByTagName('script')[0];
     s.parentNode.insertBefore(ga, s);
     })();
"""

# IT PROBABLY WON'T BE NECESSARY TO CHANGE THE FOLLOWING

BASE_PATH   = os.path.dirname(os.path.dirname(__file__))
OUTPUT_PATH = os.path.join(BASE_PATH, "_output")

config = {
    # how many posts to show on the index page?
    "n_posts"       :   1,
    "site_tagline"  :   SITE_TAGLINE,
    "site_title"    :   SITE_TITLE,
    "site_url"      :   SITE_URL,
    "editor"        :   shlex.split("vim -O -c 'set ft=markdown' +/^$ '+normal j'"),
    "meta_date_fmt" :   "%Y-%m-%d %H:%M:%S",
    #
    "deploy_path"   :   SITE_DEPLOY_PATH,
    "ga"            :   SITE_GOOGLE_ANALYTICS,
    #
    "posts_path"    :   os.path.join(BASE_PATH, "_posts"),
    "template_path" :   os.path.join(BASE_PATH, "_templates"),
    "assets_path"   :   os.path.join(BASE_PATH, "_assets"),
    #
    "index_path"    :   os.path.join(OUTPUT_PATH, "index.html"),
    "archive_path"  :   os.path.join(OUTPUT_PATH, "archive.html"),
    #
    "feed"          : {
        # SITE_ -> django.utils.feedgenerator.SyndicationFeed mappings
        "title"         :   SITE_TITLE,
        "link"          :   SITE_URL,
        "description"   :   SITE_TAGLINE,
        "author_name"   :   SITE_AUTHOR,
        "author_email"  :   SITE_EMAIL,
        "feed_url"      :   os.path.join(OUTPUT_PATH, SITE_TITLE + ".atom"),
        "language"      : "en",
    },
}
