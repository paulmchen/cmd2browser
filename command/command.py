import subprocess
import time
import tempfile
import util
import message


#
# Execute a command using shell=True mode.
# It is necessary to use the white list to control which clients can
# be allowed to access the server
#
def run(command):
    if util.valid_ip():
        result_success = subprocess.check_output(
            [command], stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        return util.replace_all(result_success, util.get_replace_dic())
    else:
        return message.error_404_msg


#
# Execute an async command. The process is to be killed after
# the command is run in exec_time_in_seconds
#
def run_async(command, exec_time_in_seconds):
    if util.valid_ip():
        try:
            temp_out_file_name = tempfile.NamedTemporaryFile().name
            with open(temp_out_file_name, "w") as fout:
                proc = subprocess.Popen(command, shell=True, stdout=fout)
                # wait for a few seconds
                time.sleep(exec_time_in_seconds)
                # stop the process
                proc.kill()

            # read contents of the file
            with open(temp_out_file_name, "rb") as fin:
                output = fin.read()

            # remove the temp file
            util.delete_file(temp_out_file_name)
            return util.replace_all(output, util.get_replace_dic())
        except subprocess.SubprocessError:
            proc.kill()
            outs, errs = proc.communicate()
            return errs
    else:
        return message.error_404_msg
