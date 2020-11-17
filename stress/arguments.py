import argparse

cases_parser = argparse.ArgumentParser(add_help=False)
cases_parser.add_argument("--cases", required=True, action="store", dest="cases", default=[], nargs='+',
                          help="cases, default:None")

node1_ip_parser = argparse.ArgumentParser(add_help=False)
node1_ip_parser.add_argument("--node1_ip", action="store", dest="node1_ip", default=None,
                             help="node1 ip, default: None")

def parse_arg():
    """Init all the command line arguments."""
    parser = argparse.ArgumentParser(description='pztest')
    subparsers = parser.add_subparsers()

    sub_parser = subparsers.add_parser('ut', parents=[cases_parser], help='ut args.')
    sub_parser.set_defaults(action='ut')
    sub_parser.add_argument("--build_path", action="store", dest="build_path", default='/home/ut/',
                            help="Default is /home/ut/")

    args = parser.parse_args()

    return args