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
def fs_mark_reports():
    report_path = os.path.join(work_dir, 'report/templates/')
    reports = []
    for template in os.listdir(report_path):
        if 'fs_mark-report' in template and os.path.isfile(os.path.join(report_path, template)):
            reports.append(template)

    return render_template('fs_mark.html', reports=reports)

@app.route('/fs_mark/<report_html>')
def fs_mark_report(report_html):
    return render_template(os.path.join(report_html))

if __name__ == '__main__':
    app.run(host=get_localhost_ip(), port=5000)