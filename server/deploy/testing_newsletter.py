# coding=utf-8
from __future__ import absolute_import

import multiprocessing

bind = "127.0.0.1:5003"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "deploy/newsletter.access.log"
errorlog = "deploy/newsletter.error.log"
pidfile = "deploy/newsletter.pid"
raw_env = "SUP_EXT_NEWSLETTER_CONFIG_NAME=testing"