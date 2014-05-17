# -*- coding: utf-8 -*-

import os
import codecs

from nikola.plugin_categories import LateTask 
from nikola import utils

class RedirectDirectories(LateTask):
    """ Create redirect pages for directories """

    name = "redirect_directories"

    def gen_tasks(self):
        outputs = []
        flag = {}
        index_file = self.site.config.get('INDEX_FILE', 'index.html')

        yield self.group_task()

        for month in self.site.posts_per_month.keys():
            for lang in self.site.config['TRANSLATIONS']:
                outputs.append(self.site.path("archive", month, lang))
        for year in self.site.posts_per_year.keys():
            for lang in self.site.config['TRANSLATIONS']:
                outputs.append(self.site.path("archive", year, lang))

        for post in self.site.timeline:
            source = post.source_path
            key = os.path.dirname(source)
            if flag.get(key): continue
            flag[key] = True

            for lang in self.site.config["TRANSLATIONS"]:
                dir = os.path.dirname(post.destination_path(lang))
                if self.site.config.get('PRETTY_URLS'):
                    dir = os.path.dirname(dir)
                while dir:
                    output = os.path.join(dir, index_file)
                    outputs.append(output)
                    dir = os.path.dirname(dir)

        for output in list(set(outputs)):
            target = os.path.join(self.site.config['OUTPUT_FOLDER'], output) 
            if os.path.exists(target): continue
            yield {
                'basename': self.name,
                'name': target,
                'targets': [target+"~"],
                'actions': [(create_archive_redirect, (target, '..'))],
                'task_dep': ['render_site'],
            }


def create_archive_redirect(src, dst):
    if os.path.exists(src): return 
    utils.makedirs(os.path.dirname(src))
    with codecs.open(src, "wb+", "utf8") as fd:
        fd.write('<!DOCTYPE html><head><title>Redirecting...</title>'
                 '<meta http-equiv="refresh" content="0; '
                 'url={0}"></head>'.format(dst))
