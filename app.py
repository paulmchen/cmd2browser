from flask import Flask
import subprocess
import time
import tempfile
import util
import message


app = Flask('flaskshell')


#
# Execute a command using shell=True mode.
# It is necessary to use the white list to control which clients can
# be allowed to access the server
#
def exec_command(command):
    result_success = subprocess.check_output(
        [command], stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    return util.replace_all(result_success, util.get_replace_dic())


#
# Execute an async command. The process is to be killed after
# the command is run in exec_time_in_seconds
#
def exec_command_async(command, exec_time_in_seconds):
    try:
        temp_out_file_name = tempfile.NamedTemporaryFile().name
        fout = open(temp_out_file_name, "w")
        proc = subprocess.Popen(command, stdout=fout)
        # wait for a few seconds
        time.sleep(exec_time_in_seconds)
        # stop the process
        proc.kill()
        fout.close()
        fin = open(temp_out_file_name, "r")
        output = fin.read()
        fin.close()

        # remove the temp file
        util.delete_file(temp_out_file_name)
        return util.replace_all(output, util.get_replace_dic())
    except subprocess.SubprocessError:
        proc.kill()
        outs, errs = proc.communicate()
        return errs


# Example: call command line ls command
@app.route('/ls/')
def get_ls():
    if util.valid_ip():
        try:
            result_success = exec_command("ls -al")
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
            result_success = exec_command("docker ps -a")
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
            result_success = exec_command_async("top", 2)
        except subprocess.CalledProcessError as e:
            return message.error_500_msg
        return result_success
    else:
        return message.error_404_msg


if __name__ == '__main__':
    app.run(host='0.0.0.0')
