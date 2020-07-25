from flask import Flask
from flask import request
from collections import OrderedDict
import subprocess

app = Flask('flaskshell')
# add your client IPs to the list to enable your client to get command execution
# outputs from your browser
ip_whitelist = ['192.168.1.2', '192.168.1.3', '127.0.0.1']

error_404_msg = """<title>404 Not Found</title>
               <h1>Not Found</h1>
               <p>The requested URL was not found on the server.
               If you entered the URL manually please check your
               spelling and try again.</p>""", 404


#
# Validate client IP, only ips defined in the white list will be allowed to connect
# to the server, otherwise the browser will return 404 error
#
def valid_ip():
    client = request.remote_addr
    print("The remote client address:", client)
    if client in ip_whitelist:
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


#
# Execute a command using shell=True mode.
# It is necessary to use the white list to control which clients can
# be allowed to access the server
#
def exec_command(command):
    result_success = subprocess.check_output(
        [command], stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    rep = OrderedDict([("[0;32m", "<br/>"), ("[0;33m", "<br/>"), ("[0m", "&nbsp;"), ("\r\n", "<br/>"),
                       ("\n", "<br/>"), (" ", "&nbsp;")])
    return replace_all(result_success, rep)


# Example: call command line ls command
@app.route('/ls/')
def get_ls():
    if valid_ip():
        command_success = "ls -al"
        try:
            result_success = exec_command(command_success)

        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to fetch command results."

        return '%s' % result_success
    else:
        return error_404_msg


# Example: call command line docker command
@app.route('/docker_ps/')
def get_docker_ps():
    if valid_ip():
        command_success = "docker images"
        try:
            result_success = exec_command(command_success)

        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to fetch command results."

        return '%s' % result_success
    else:
        return error_404_msg


if __name__ == '__main__':
    app.run()
