import sys, os
work_dir = os.path.join(os.getcwd().split('storage')[0], 'storage')
sys.path.append(work_dir)

from flask import Flask, render_template
from utils.util import get_localhost_ip
from libs.log_obj import LogObj


logger = LogObj().get_logger()
app = Flask(__name__)


@app.route('/')
def init():
    return render_template('main.html')

@app.route('/fs_mark')
def report():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(host=get_localhost_ip(), port=5000)