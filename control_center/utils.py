import subprocess

def get_wifi():
    subprocess_result = subprocess.Popen('iwgetid',shell=True,stdout=subprocess.PIPE)
    subprocess_output = subprocess_result.communicate()[0],subprocess_result.returncode
    return subprocess_output[0].decode('utf-8')