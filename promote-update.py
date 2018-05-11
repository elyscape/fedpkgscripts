#!/usr/bin/env python

from __future__ import print_function

import argparse

from bodhi.client.bindings import BodhiClient

STATUSES = ['testing', 'batched', 'stable', 'obsolete', 'unpush', 'revoke']

class UpdatePromoter(object):
    def __init__(self, dry_run=False):
        self._client = BodhiClient()
        self._client.init_username()
        self._dry_run = dry_run
        self._log_prefix = ''
        if dry_run:
            self._log_prefix = 'dry run: '

    def promote_update(self, update, status='stable'):
        print('{}{} - requesting {}'.format(self._log_prefix, update.title, status))
        request_params = {
                'update': update.title,
                'request': status,
            }
        if not self._dry_run:
            self._client.request(**request_params)

    def promote_updates(self, updates, status='stable'):
        for update in updates:
            if status in ['stable', 'batched'] and not update.meets_testing_requirements:
                print('{}skipping {} - not eligible for {}'.format(self._log_prefix, update.title, status))
                continue
            self.promote_update(update, status)

    def get_updates(self, release, package=None, status='testing'):
        query_params = {
                'mine': True,
                'releases': release,
                'rows_per_page': 100,
                'status': status,
            }
        if package:
            query_params['packages'] = package
        return self._client.query(**query_params).updates

def main():
    parser = argparse.ArgumentParser(description='Promote an update on Bodhi.')
    parser.add_argument('package', help='the package to promote')
    parser.add_argument('release', help='the release containing the update')
    parser.add_argument('-s', '--status', default='stable', metavar='STATUS', choices=STATUSES, help='the status to request (default: stable)')
    parser.add_argument('-o', '--oldstatus', default='testing', metavar='STATUS', choices=STATUSES, help='the current status of the update (default: testing)')
    parser.add_argument('-n', '--dry-run', action='store_true')

    args = parser.parse_args()

    promoter = UpdatePromoter(args.dry_run)

    updates = promoter.get_updates(package=args.package, release=args.release, status=args.oldstatus)

    promoter.promote_updates(updates, args.status)

if __name__ == '__main__':
    main()
