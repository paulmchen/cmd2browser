from flask import Flask
from flask import request
from collections import OrderedDict
import subprocess

app = Flask('flaskshell')
ip_whitelist = ['192.168.1.2', '192.168.1.3', '127.0.0.1']

error_404_msg = """<title>404 Not Found</title>
               <h1>Not Found</h1>
               <p>The requested URL was not found on the server.
               If you entered the URL manually please check your
               spelling and try again.</p>""", 404


def valid_ip():
    client = request.remote_addr
    if client in ip_whitelist:
        return True
    else:
        return False


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def exec_command(command):
    result_success = subprocess.check_output(
        [command], stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    rep = OrderedDict([("[0;32m", "<br/>"), ("[0;33m", "<br/>"), ("[0m", ""), ("\r\n", "<br/>"), ("\n", "<br/>")])
    return replace_all(result_success, rep)


# call command line ls command
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


# call command line docker command
@app.route('/docker_ps/')
def get_docker_ps():
    if valid_ip():
        command_success = "docker ps -a"
        try:
            result_success = exec_command(command_success)

        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to fetch command results."

        return '%s' % result_success
    else:
        return error_404_msg


if __name__ == '__main__':
    app.run()
