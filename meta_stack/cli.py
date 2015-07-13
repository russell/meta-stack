# -*- coding: utf-8 -*-

import logging
from ConfigParser import SafeConfigParser

log = logging.getLogger(__file__)

SITE_OS_EXPORTS = {
    'uri': 'OS_AUTH_URL',
    'region': 'OS_REGION_NAME',
}

USER_OS_EXPORTS = {
    'username': 'OS_USERNAME',
    'password': 'OS_PASSWORD',
    'tenant': 'OS_TENANT_NAME',
}


class Variables():

    def __init__(self, site):
        parser = SafeConfigParser({'site_id': site})
        parser.read(["etc/base.cfg", "etc/sites/%s.cfg" % site])
        self.parser = parser

    def get_site_variables(self):
        variables = dict(self.parser.items('site'))
        del variables['site_id']
        return variables

    def get_user_variables(self, user):
        variables = dict(self.parser.items('user:%s' % user))
        return variables


def export_environment(args):
    parser = Variables(args.site)

    site = parser.get_site_variables()
    for var, val in site.items():
        if var in SITE_OS_EXPORTS:
            print 'export %s="%s"' % (SITE_OS_EXPORTS[var], val)

    user = parser.get_user_variables(args.user)
    for var, val in user.items():
        if var in USER_OS_EXPORTS:
            print 'export %s="%s"' % (USER_OS_EXPORTS[var], val)


def keystone_connection_2(local_ns):
    from keystoneclient.v2_0 import client
    return client.Client(username=local_ns['OS_USERNAME'],
                         password=local_ns['OS_PASSWORD'],
                         tenant_name=local_ns['OS_TENANT_NAME'],
                         auth_url=local_ns['OS_AUTH_URL'])


def keystone_connection_3(local_ns):
    from keystoneclient.v3 import client
    return client.Client(username=local_ns['OS_USERNAME'],
                         password=local_ns['OS_PASSWORD'],
                         tenant_name=local_ns['OS_TENANT_NAME'],
                         auth_url=local_ns['OS_AUTH_URL'])


def nova_connection(local_ns):
    from novaclient.v2 import client
    return client.Client(local_ns['OS_USERNAME'],
                         local_ns['OS_PASSWORD'],
                         tenant_name=local_ns['OS_TENANT_NAME'],
                         auth_url=local_ns['OS_AUTH_URL'],
                         service_type="compute")


def ipython_shell(args):
    from IPython import embed
    from IPython.config.loader import Config
    cfg = Config()
    cfg.PromptManager.in_template = '%s<\\#>: ' % args.site.strip().upper()

    parser = Variables(args.site)
    site = parser.get_site_variables()
    user = parser.get_user_variables(args.user)
    user_ns = {}
    for var, val in site.items():
        if var in SITE_OS_EXPORTS:
            user_ns[SITE_OS_EXPORTS[var]] = val

    for var, val in user.items():
        if var in USER_OS_EXPORTS:
            user_ns[USER_OS_EXPORTS[var]] = val

    user_ns['ks'] = keystone_connection(user_ns)
    user_ns['no'] = nova_connection(user_ns)

    embed(config=cfg,
          user_ns=user_ns,
          banner1='\nConnected to site %s\n' % args.site)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help="Increase verbosity (specify multiple times for more)")
    parser.add_argument(
        '-u', '--user', action='store', default='sanity',
        help="The user to print credentials for.")
    parser.add_argument(
        '-s', '--site', type=str,
        help='the site to access')

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid subcommands',
        help='additional help')

    ipython = subparsers.add_parser(
        'ipython', help='IPython shell into environment.')
    ipython.set_defaults(func=ipython_shell)

    export = subparsers.add_parser(
        'export', help='Export environment.')
    export.set_defaults(func=export_environment)

    args = parser.parse_args()

    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(name)s %(levelname)s %(message)s')
    args.func(args)
