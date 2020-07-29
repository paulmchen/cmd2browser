# cmd2browser
Execute system commands and display outputs to a browser

A python application that can be modified to execute system commands and then display the outputs to a Web browser.

## Install Prerequisites

Install Python (v2 or v3) and PIP:
1. Visit https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/ to learn how to instll Python
1. Visit https://www.shellhacks.com/python-install-pip-mac-ubuntu-centos/ to learn how to instqll PIP
1. Run the following command to install Python flask module:  

```shell
  pip install flask
```

## Install & Launch the App
Set up the code
1. Download the Python source file /cmd2browser/app.py and place it in a new folder
1. Launch the app
```shell
  python app.py
```

## Verify
1. Start a browser session and use the following URL to validate examples provided

```shell
  1. http://127.0.0.1:5000/ls/
  2. http://127.0.0.1:5000/docker_ps/
```

## Tips
- When you are connecting to the server from another client IP, you would need to add your client IP address to the white list in app.py. By default, the server will reject any non-local connections from any remote clients. Modify the following line by adding your client IP address to the white list of the server:
```shell
  ip_whitelist = ['192.168.1.2', '192.168.1.3', '127.0.0.1']
```
- To add a new command line call and then send its output to a web browser, you can create a new def function in app.py. For example, to call a system command "kubectl get pods", add the following 'def' to app.py:
```shell
  # Example: call 'kubectl get pods' command
  @app.route('/kc_pods/', methods=['GET'])
  def get_kc_pods():
    if valid_ip():
        try:
            result_success = exec_command("kubectl get pods")
        except subprocess.CalledProcessError as e:
            return "An error occurred while trying to fetch command results."
        return result_success
    else:
        return error_404_msg

```
Launch the following URL to verify your new command line execution from your favourite browser:
```shell
http://127.0.0.1:5000/kc_pods/
```