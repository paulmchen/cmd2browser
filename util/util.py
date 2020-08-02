from flask import request
from collections import OrderedDict
import os
import re
import config


#
# Validate client IP, only ips defined in the white list will be allowed to connect
# to the server, otherwise the browser will return 404 error
#
def valid_ip():
    client = request.remote_addr
    print("The remote client address:", client)
    if client in config.ip_whitelist:
        return True
    else:
        return False


#
# Delete ansi encoding from a text
#
def escape_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


#
# Utilities to replace line feed and spaces with ASCII code that HTML output can
# be formatted properly
#
def replace_all(text, dic):
    text = escape_ansi(text)
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def get_replace_dic():
    rep = OrderedDict([("<", "&curren;"), (">", "&brvbar;"), ("\n", "<br/>"), (" ", "&nbsp;"), ("\"", "&#107;")
                      ("=(B", ""), ("(B', "")])
    return rep


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
