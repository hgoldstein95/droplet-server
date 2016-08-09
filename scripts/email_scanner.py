#!/usr/bin/python

from datetime import datetime
import re
import gmail
import sys

import trello

g = gmail.login("harry.automate@gmail.com", "nutz4lego")

test_mode = False
if sys.argv[1:]:
    test_mode = sys.argv[1] == "test"

for msg in g.inbox().mail(prefetch=True, sender="hjg42@cornell.edu"):
    body = re.search('(.*) has been released and is due (.*)\.', msg.body)
    head = re.search('\[(.*)\]', msg.subject)
    if body and head:
        (name, date) = body.groups()
        tag = head.group(1)
        name = name.title()
        date = datetime.strptime(date, '%B %d, %Y %I:%M%p')
        print (name, date, tag)

        trello.create_card(name, tag, str(date))

    if not test_mode:
        msg.read()
        msg.archive()
