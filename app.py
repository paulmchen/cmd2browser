#
# Execute system commands and display outputs to a browser
#
from flask import Flask
import subprocess

import command
import message

app = Flask('flaskshell')


# Example: call ls command
@app.route('/ls/')
def get_ls():
    try:
        return command.run("ls -al")
    except subprocess.CalledProcessError as e:
        return message.error_500_msg


# Example: call docker command
@app.route('/docker_ps/')
def get_docker_ps():
    try:
        return command.run("docker ps -a")
    except subprocess.CalledProcessError as e:
        return message.error_500_msg


# Example: call netstat command
@app.route('/netstat/')
def get_netstat():
    try:
        return command.run("netstat -tnlv")
    except subprocess.CalledProcessError as e:
        return message.error_500_msg


# Example: call async command top
@app.route('/top/')
def get_top():
    try:
        return command.run_async("top", 1)
    except subprocess.CalledProcessError as e:
        return message.error_500_msg


if __name__ == '__main__':
    app.run(host='0.0.0.0')
