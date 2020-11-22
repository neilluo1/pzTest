import sys, os

work_dir = os.path.join(os.getcwd().split('pzcore')[0], 'pzcore')
sys.path.append(work_dir)

from monitor.collection.volume import CollectVolumeData
from monitor.collection import arguments
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 1048576))

args = arguments.parse_arg()

if args.action == 'volume':
    collect_volume_data_obj = CollectVolumeData(args.ip, args.username, args.password)
    collect_volume_data_obj.create_volume_table()
    collect_volume_data_obj.insert_volume_data()
