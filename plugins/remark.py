# -*- coding: utf-8 -*-

"""Implementation of generating slide based on remark."""

from __future__ import unicode_literals

import codecs
import os
import re

from nikola.plugin_categories import PageCompiler
from nikola.utils import makedirs, req_missing

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict  # NOQA

class CompileRemark(PageCompiler):
    """Generate slide."""

    name = "remark"
    demote_headers = True

    def __init__(self, *args, **kwargs):
        super(CompileRemark, self).__init__(*args, **kwargs)

    def compile_html(self, source, dest, is_two_file=True):
        makedirs(os.path.dirname(dest))
        with codecs.open(dest, "w+", "utf8") as out_file:
            with codecs.open(source, "r", "utf8") as in_file:
                data = in_file.read()
            if not is_two_file:
                data = re.split('(\n\n|\r\n\r\n)', data, maxsplit=1)[-1]
            out_file.write('<div id="source" style="display: none">' 
                            + data + '</div>')

    def create_post(self, path, onefile=False, is_page=False, **kw):
        metadata = OrderedDict()
        metadata.update(self.default_metadata)
        metadata.update(kw)
        makedirs(os.path.dirname(path))
        with codecs.open(path, "wb+", "utf8") as fd:
            if onefile:
                fd.write('<!-- \n')
                for k, v in metadata.items():
                    fd.write('.. {0}: {1}\n'.format(k, v))
                fd.write('-->\n\n')
            fd.write("\nWrite your {0} here.".format('page' if is_page else 'post'))
