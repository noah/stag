+ stag

STAtic site Generator.

+ about stag

*stag* is a static site generator written in python3.  *stag* is good
for those late-night blogging sessions.  It won't fill you up and
finishes smooth, with a light *html5* palate and faint *markdown* notes.

Tired of solutions with soggy feature sets and bitter-tasting
documentation?  The only file you need to read to get going with stag is
`lib/config.py`

Stag is easy on your wallet, as any static site generator should be.
Stag is for people who like *markdown*, *pygments*, and the *django
standard library*.

So grab a six pack of `stag`.  Golden blogging quality since 2012.

+ dependencies

* `django-trunk` - 

    pip install git+http://github.com/django/django.git

* `markdown`

    pip install markdown

* `pygments`
    
    pip install pygments

* edit the `site.cfg` file

+ usage

*stag* is intended to be really simple to use:

    ⚡ ./stag
    Options:
    init - initialize a new site
    post <post title> - edit new or existing post
    deploy - deploy the site
    ls - list posts
    gen - generate the 'compiled' site

Also, *stag* is designed to be very simple -- it weighs in at a measly
~300 SLOC!

+ post metadata

&lt;rant&gt;

Somewhat incredibly, python does not support YAML natively.  This means
there are several bad and worse options to choose from for supporting
human-readable metadata; namely, JSON (native, but not as readable as
yaml), python dicts (too clunky), configparser (yuck), shlex (are you
fscking kidding me?)...

Faced with the aforementioned ugg, I considered using py-yaml ... this
would allow me to keep `stag` super flexible and de-coupled, with the
possibility of later adding something like reStructuredText, textile,
textify, yotextmomma, or whatever flavor-of-the-month markup language
comes next.

After learning that
[`python-markdown`][http://freewisdom.org/projects/python-markdown/Meta-Data]
has a very flexible markdown metadata extension (surprise, it looks just
like yaml!), which also includes pygments integration, I said fsck it,
and doubled-down on really learning markdown.  You should too!
