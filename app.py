from flask import Flask
import subprocess
import util
import message


app = Flask('flaskshell')


# Example: call command line ls command
@app.route('/ls/')
def get_ls():
    if util.valid_ip():
        try:
            result_success = util.exec_command("ls -al")
        except subprocess.CalledProcessError as e:
            return message.error_500_msg
        return result_success
    else:
        return message.error_404_msg


# Example: call command line docker command
@app.route('/docker_ps/')
def get_docker_ps():
    if util.valid_ip():
        try:
            result_success = util.exec_command("docker ps -a")
        except subprocess.CalledProcessError as e:
            return message.error_500_msg
        return result_success
    else:
        return message.error_404_msg


# Example: call async command call e.g. top
@app.route('/top/')
def get_top():
    if util.valid_ip():
        try:
            result_success = util.exec_command_async("top", 1)
        except subprocess.CalledProcessError as e:
            return message.error_500_msg
        return result_success
    else:
        return message.error_404_msg


if __name__ == '__main__':
    app.run(host='0.0.0.0')
