import sys, os
work_dir = os.path.join(os.getcwd().split('storage')[0], 'storage')
sys.path.append(work_dir)

from flask import Flask, render_template, request
from utils.util import get_localhost_ip, run_cmd, datetime_parser
from flask.json import jsonify
from libs.mysql_obj import MysqlObj
from monitor.collection import arguments
from settings.global_settings import MYSQL_USER, MYSQL_HOST, MYSQL_PASSWORD
import time
import json
from libs.log_obj import LogObj


logger = LogObj().get_logger()

args = arguments.parse_arg()
app = Flask(__name__)

mysql_obj = MysqlObj(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD)

db_name = 'vbos{name}'.format(name=args.node1_ip.replace('.', '_'))
create_db_cmd = 'create database if not exists {db}'.format(db=db_name)
mysql_obj.run_sql_cmd(create_db_cmd)

# global var define
table_name = None
hour24_time_list = []
w_iops_list = []
r_iops_list = []


@app.route('/')
def init():
    return render_template('main.html')


@app.route("/storage/info/performance", methods=["GET"])
def storage_performance(pvc_name):
    global table_name
    global hour24_time_list
    global w_iops_list
    global r_iops_list

    hour24_time_list = []
    w_iops_list = []
    r_iops_list = []

    collect_script = os.path.join(work_dir, "monitor/collection/collect.py")
    check_collect_cmd = "ps -ax |grep {script} |grep {pvc} |grep -v grep".format(script=collect_script, pvc=pvc_name)
    rtn_dict = run_cmd(check_collect_cmd)
    if rtn_dict['rc'] !=0 and rtn_dict['stdout'] == '':
        collect_cmd = "nohup python {script} volume --node1_ip {ip} --vset_ids {vset_ids} --pvc {pvc} > ./collection/log/collect_{pvc}.log 2>&1 &".format(script=collect_script, ip=args.node1_ip, vset_ids=" ".join([str(vset_id) for vset_id in args.vset_ids]), pvc=pvc_name)
        run_cmd(collect_cmd)

    sql_cmd1 = "select * from {db}.volumes".format(db=db_name)
    while True:
        try:
            mysql_obj.run_sql_cmd(sql_cmd1)
            rows = mysql_obj.fetchall
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))
            time.sleep(10)
            continue

        if len(rows) > 0:
            for row in rows:
                if row['pvc'] == pvc_name:
                    table_name = row['name']
                    break
            else:
                time.sleep(10)
                continue

            break
        else:
            continue

    sql_cmd = "select * from {db}.{table_name}".format(db=db_name, table_name=table_name)
    while True:
        try:
            mysql_obj.run_sql_cmd(sql_cmd)
            rows = mysql_obj.fetchall
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))
            time.sleep(5)
            continue

        try:
            if len(rows) > 0:
                for row in rows:
                    io_stat = json.loads(row['io_stat'])
                    w_iops_list.append(io_stat['w_iops'])
                    r_iops_list.append(io_stat['r_iops'])
                    hour24_time_list.append(row['c_time'])
                break
            else:
                time.sleep(5)
                continue
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))
            continue

    return render_template("volume_performance.html", pvc_name=pvc_name)


@app.route("/storage/info/performance/update", methods=["GET", "POST"])
def storage_performance_update():
    global table_name
    global hour24_time_list
    global w_iops_list
    global r_iops_list

    try:
        sql_cmd = "SELECT * FROM {db}.{table_name} ORDER BY c_time DESC LIMIT 1".format(db=db_name, table_name=table_name)
        mysql_obj.run_sql_cmd(sql_cmd)
        row = mysql_obj.fetchone
        io_stat = json.loads(row['io_stat'])
        c_time = row['c_time']
        time_diff = (c_time - hour24_time_list[-1]).seconds
        if time_diff > 0:
            hour24_time_list.append(c_time)
            w_iops_list.append(io_stat['w_iops'])
            r_iops_list.append(io_stat['r_iops'])

    except Exception as e:
        raise Exception('Exception occured, error is {err}!'.format(err=e))

    data = {}
    data['hour24_time_list'] = hour24_time_list
    data['w_iops_list'] = w_iops_list
    data['r_iops_list'] = r_iops_list

    

    return jsonify(data)


if __name__ == '__main__':
    app.run(host=get_localhost_ip(), port=5000)