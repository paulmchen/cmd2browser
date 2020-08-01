from flask import request
from collections import OrderedDict
import os
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
# A utilities to replace line feed and spaces with ASCII code that HTML output can
# be formatted properly
#
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def get_replace_dic():
    rep = OrderedDict([("[0;32m", "<br/>"), ("[0;33m", "<br/>"), ("[0m", "&nbsp;"), ("\r\n", "<br/>"),
                       ("<", "&curren;"), (">", "&brvbar;"), ("\n", "<br/>"), (" ", "&nbsp;"), ("\"", "&#107;")])
    return rep


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
