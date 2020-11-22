import argparse


ip_parser = argparse.ArgumentParser(add_help=False)
ip_parser.add_argument("--ip", action="store", dest="ip", default=None,
                             help="ip, default: None")


def ssh_auth_parser():
    """
    ssh connect keys
    :return:
    """
    ssh_auth_parser = argparse.ArgumentParser(add_help=False)
    ssh_auth_group = ssh_auth_parser.add_argument_group('SSH auth info args')
    ssh_auth_group.add_argument("--username", action="store", dest="username", default="root", help="default:root")
    ssh_auth_group.add_argument("--password", action="store", dest="password", default="password",
                                help="default:password")
    ssh_auth_group.add_argument("--key_file", action="store", dest="key_file", default=None, help="pem key file path")

    return ssh_auth_parser


def parse_arg():
    """Init all the command line arguments."""
    parser = argparse.ArgumentParser(description='volume')
    subparsers = parser.add_subparsers()

    sub_parser = subparsers.add_parser('volume',
                                       parents=[ip_parser, ssh_auth_parser()],
                                       help='volume args.')
    sub_parser.set_defaults(action='volume')

    args = parser.parse_args()

    return args