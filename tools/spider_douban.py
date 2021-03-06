# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import os
import sys
import urllib2
import re
import json
import urllib

PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
try:
    import keepcd
    print('Start keepcd version: %s' % keepcd.__version__)
except ImportError:
    import site
    site.addsitedir(ROOTDIR)
    site.addsitedir(ROOTDIR+"/keepcd")
    print('Development of keepcd: ' + ROOTDIR)

from tornado.options import options
from dojang.util import parse_config_file




def run_command(name):
    
    from dojang.util import parse_config_file, import_object
    from easycrawl.models import CrawlSite
    from easycrawl.helper import create_crawl_class, update_crawl_status
    from easycrawl.database import crawldb
    # from keepcd.admin.easycrawl.douban.app import worker
    

    site = CrawlSite.query.filter_by(name=name).first()
    worker_name = "easycrawl.%s.app.worker" % name
    print worker_name
    worker = import_object(worker_name)
    clz = create_crawl_class('douban_movie')
    url = 'http://movie.douban.com'
    update_crawl_status(clz, crawldb, url, 0)

    worker.run(callback=None)
    worker.run(callback=None)
    worker.finished()
    


if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf8') 
    parser = argparse.ArgumentParser(
        prog='keep cd',
        description='keep',
    )
    parser.add_argument('command', nargs="*")
    args = parser.parse_args()
    parse_config_file(ROOTDIR+"/settings.py")
    run_command('douban')



