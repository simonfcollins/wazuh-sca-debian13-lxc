#!/usr/bin/python3

import argparse
import re
import sys

parser = argparse.ArgumentParser(
    prog='cis-step-id',
    description='''
                Increments the IDs of rules within Wazuh CIS rulesets by a specified offset.
                Useful when creating custom CIS rulesets from an existing ruleset where both are 
                used as policies by Wazuh. When importing policies, Wazuh will skip a policy upon
                encountering a duplicate rule within the policy. This tool remedies that issue by
                creating a copy of the source CIS ruleset with rule IDs incremented by a specified 
                offset.
                '''
)

parser.add_argument(
    '-s', '--source',
    required=True,
    help='Source file'
)

parser.add_argument(
    '-i', '--offset',
    required=True,
    type=int,
    help='Integer offset to add to each ID'
)

parser.add_argument(
    '-o', '--dest',
    required=True,
    help='Destination file'
)

args = parser.parse_args()

try:
    with open(args.source, 'r') as file:
        contents = file.read()

    updated = re.sub(
        r'(^  - id: )(\d+)',
        lambda m: m.group(1) + str(int(m.group(2)) + args.offset),
        contents,
        flags=re.M
    )

    with open(args.dest, 'w') as file:
        file.write(updated)

except FileNotFoundError:
    print(f"Error: Source file '{args.source}' not found.", file=sys.stderr)
    sys.exit(1)

except PermissionError:
    print("Error: Permission denied accessing a file.", file=sys.stderr)
    sys.exit(1)

except OSError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
