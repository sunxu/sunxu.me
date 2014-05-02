# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import codecs
import datetime
import os
import sys

from blinker import signal

from nikola.plugin_categories import Command
from nikola import utils

POSTLOGGER = utils.get_logger('new_post', utils.STDERR_HANDLER)
PAGELOGGER = utils.get_logger('new_page', utils.STDERR_HANDLER)
SLIDELOGGER = utils.get_logger('new_slide', utils.STDERR_HANDLER)
LOGGER = POSTLOGGER


def filter_post_pages(compiler, content_type, compilers, post_pages):
    """Given a compiler ("markdown", "rest"), and whether it's meant for
    a post or a page, and compilers, return the correct entry from
    post_pages."""

    # First throw away all the post_pages with the wrong is_post
    is_post = False if content_type == 'page' else True 
    filtered = [entry for entry in post_pages if entry[3] == is_post]

    # These are the extensions supported by the required format
    extensions = compilers[compiler]

    # Throw away the post_pages with the wrong extensions
    filtered = [entry for entry in filtered if any([ext in entry[0] for ext in
                                                    extensions])]

    if not filtered:
        raise Exception("Can't find a way, using your configuration, to create "
                        "a {0} in format {1}. You may want to tweak "
                        "COMPILERS or {2}S in conf.py".format(
                            content_type, compiler, content_type.upper()))
    return filtered[0]


def get_date(schedule=False, rule=None, last_date=None, force_today=False):
    """Returns a date stamp, given a recurrence rule.

    schedule - bool:
        whether to use the recurrence rule or not

    rule - str:
        an iCal RRULE string that specifies the rule for scheduling posts

    last_date - datetime:
        timestamp of the last post

    force_today - bool:
        tries to schedule a post to today, if possible, even if the scheduled
        time has already passed in the day.
    """

    date = now = datetime.datetime.now()
    if schedule:
        try:
            from dateutil import rrule
        except ImportError:
            LOGGER.error('To use the --schedule switch of new_post, '
                         'you have to install the "dateutil" package.')
            rrule = None
    if schedule and rrule and rule:
        if last_date and last_date.tzinfo:
            # strip tzinfo for comparisons
            last_date = last_date.replace(tzinfo=None)
        try:
            rule_ = rrule.rrulestr(rule, dtstart=last_date)
        except Exception:
            LOGGER.error('Unable to parse rule string, using current time.')
        else:
            # Try to post today, instead of tomorrow, if no other post today.
            if force_today:
                now = now.replace(hour=0, minute=0, second=0, microsecond=0)
            date = rule_.after(max(now, last_date or now), last_date is None)
    return date.strftime('%Y/%m/%d %H:%M:%S')


class CommandPost(Command):
    """Create a new post."""

    name = "post"
    doc_usage = "[options] [path]"
    doc_purpose = "create a new post or page or slide"
    cmd_options = [
        {
            'name': 'kind',
            'short': 'k',
            'long': 'kind',
            'type': str,
            'default': 'post',
            'help': 'Page type, one of post, page, slide.'
        },
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
        """Create a new post or page or slide."""
        global LOGGER
        compiler_names = [p.name for p in
                          self.site.plugin_manager.getPluginsOfCategory(
                              "PageCompiler")]

        if len(args) > 1:
            print(self.help())
            return False
        elif args:
            path = args[0]
        else:
            path = None

        content_type = options['kind']
        content_format = options['content_format']
        if ( content_type not in ['post', 'page', 'slide'] or
            content_format not in ['markdown', 'remark', 'html'] ):
            print(self.help())
            return False

        is_page = True if content_type == 'page' else False 
        is_post = not is_page

        title = options['title'] or None
        tags = options['tags']

        if content_type == 'page':
            LOGGER = PAGELOGGER
        elif content_type == 'post':
            LOGGER = POSTLOGGER
        else:
            LOGGER = SLIDELOGGER

        if content_format not in compiler_names:
            LOGGER.error("Unknown {0} format {1}".format(content_type, content_format))
            return

        compiler_plugin = self.site.plugin_manager.getPluginByName(
            content_format, "PageCompiler").plugin_object

        # Guess where we should put this
        entry = filter_post_pages(content_format, content_type,
                                  self.site.config['COMPILERS'],
                                  self.site.config['post_pages'])

        print("Creating New {0}".format(content_type.title()))
        print("-----------------\n")
        if title is None:
            print("Enter title: ", end='')
            # WHY, PYTHON3???? WHY?
            sys.stdout.flush()
            title = sys.stdin.readline()
        else:
            print("Title:", title)
        if isinstance(title, utils.bytes_str):
            title = title.decode(sys.stdin.encoding)
        title = title.strip()
        if not title:
            print("Empty tilte.")
            return False
        if not path:
            slug = utils.slugify(title)
        else:
            if isinstance(path, utils.bytes_str):
                path = path.decode(sys.stdin.encoding)
            slug = utils.slugify(os.path.splitext(os.path.basename(path))[0])

        # Calculate the date to use for the content
        schedule = self.site.config['SCHEDULE_ALL']
        rule = self.site.config['SCHEDULE_RULE']
        force_today = self.site.config['SCHEDULE_FORCE_TODAY']
        self.site.scan_posts()
        timeline = self.site.timeline
        last_date = None if not timeline else timeline[0].date
        date = get_date(schedule, rule, last_date, force_today)
        data = [title, slug, date, tags]
        prefix = '' if is_page else date[0:7]
        output_path = os.path.join(os.path.dirname(entry[0]), prefix)
        pattern = os.path.basename(entry[0])
        suffix = pattern[1:]
        if not path:
            txt_path = os.path.join(output_path, slug + suffix)
        else:
            txt_path = path

        if os.path.isfile(txt_path):
            LOGGER.error("The title already exists!")
            exit()

        d_name = os.path.dirname(txt_path)
        utils.makedirs(d_name)
        metadata = self.site.config['ADDITIONAL_METADATA']
        compiler_plugin.create_post(
            txt_path, onefile=True, title=title,
            slug=slug, date=date, tags=tags, is_page=is_page, **metadata)

        event = dict(path=txt_path)

        LOGGER.info("Your {0}'s text is at: {1}".format(content_type, txt_path))

        signal('new_' + content_type).send(self, **event)
