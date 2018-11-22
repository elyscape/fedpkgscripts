#!/usr/bin/env python3

from __future__ import print_function

import argparse
import importlib

promote_update = importlib.import_module('promote-update')

def key_names_acme_first(update):
    title = update.title
    if title.startswith('python-acme'):
        return '\0' + title
    return title

def main():
    parser = argparse.ArgumentParser(description='Promote all eligible updates on Bodhi.')
    parser.add_argument('release', help='the release containing the updates')
    parser.add_argument('-s', '--status', default='stable', metavar='STATUS', choices=promote_update.STATUSES, help='the status to request (default: stable)')
    parser.add_argument('-o', '--oldstatus', default='testing', metavar='STATUS', choices=promote_update.STATUSES, help='the current status of the updates (default: testing)')
    parser.add_argument('-n', '--dry-run', action='store_true')

    args = parser.parse_args()

    promoter = promote_update.UpdatePromoter(args.dry_run)

    updates = promoter.get_updates(release=args.release, status=args.oldstatus)
    updates.sort(key=key_names_acme_first)

    promoter.promote_updates(updates, args.status)

if __name__ == '__main__':
    main()
