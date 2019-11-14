# from celery import Celery
from pathlib import Path
import os


# app = Celery('cc', backend="redis://localhost:6379/0")



from celery import Celery
app = Celery('tasks', broker='redis://localhost:6379/0')
@app.task
def add(x, y):
    return x + y

base_dir = Path(__file__).parent

script = (base_dir / 'run_cmd.py').resolve()


import subprocess
import signal

@app.task
def run(cmd):
    p = None
    def sighandle(signum, frame):
        print(f'sig {signum} received from task...')
        if p:
            print(p.pid)
            # p.terminate()
            print(signum)
            os.killpg(p.pid, signum)
            # os.system(f'kill -{signum} {p.pid}')
            print('after kill')
        # p.send_signal(signum)
    signal.signal(signal.SIGTERM, sighandle)
    p = subprocess.Popen(f'python {script} {cmd}', shell=True, encoding='utf-8', 
    # stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
    start_new_session=True)
    # # for line in p.stdout:
    # #     print(line)
    p.wait()
    return p.returncode
