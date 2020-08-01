import subprocess
import time
import tempfile
import util


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
        proc = subprocess.Popen(command, shell=True, stdout=fout)
        # wait for a few seconds
        time.sleep(exec_time_in_seconds)
        # stop the process
        proc.kill()
        fout.close()
        fin = open(temp_out_file_name, "rb")
        output = fin.read()
        fin.close()

        # remove the temp file
        util.delete_file(temp_out_file_name)
        return util.replace_all(output, util.get_replace_dic())
    except subprocess.SubprocessError:
        proc.kill()
        outs, errs = proc.communicate()
        return errs
