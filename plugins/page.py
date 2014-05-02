# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from nikola.plugin_categories import Command


class CommandPage(Command):
    """Create a new page."""

    name = "page"
    doc_usage = "[options] [path]"
    doc_purpose = "create a new page in the site"
    cmd_options = [
        {
            'name': 'title',
            'short': 't',
            'long': 'title',
            'type': str,
            'default': '',
            'help': 'Title for the post.'
        },
        {
            'name': 'tags',
            'long': 'tags',
            'type': str,
            'default': '',
            'help': 'Comma-separated tags for the post.'
        },
        {
            'name': 'content_format',
            'short': 'f',
            'long': 'format',
            'type': str,
            'default': 'markdown',
            'help': 'Markup format for the post, one of markdown, remark, html,',
        },

    ]

    def _execute(self, options, args):
        """Create a new page."""
        options['kind'] = 'page'
        p = self.site.plugin_manager.getPluginByName('post', 'Command').plugin_object
        return p.execute(options, args)
