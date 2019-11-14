# -*- coding: utf-8 -*-

import requests
import argparse

def parse_args():
    description = """
A test case to insert rules in bulk. 
The values of policy_type range from 1 to 18, which means:
    1  => trojan rule
    2  => attack rule
    3  => malware rule
    4  => abnormal rule
    5  => keyword rule
    6  => encryption rule
    7  => compress rule
    8  => picture rule
    9  => ip audit rule
    10 => domain audit rule
    11 => url audit rule
    12 => account audit rule
    13 => net log rule
    14 => app behavior rule
    15 => web filter rule
    16 => dns filter rule
    17 => ip whitelist rule
    18 => block rule
Note that you need put the rule file(.xlsx or .xls) in "media/" of the Detect Center Project.
For example, for "media/batch_insert/keyword/keyword_rule.xlsx", the relative_path
is "batch_insert/keyword/keyword_rule.xlsx".
"""
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--type', required=True, type=int, choices=range(1, 19), help='the policy type')
    parser.add_argument('-p', '--path', required=True, help='the relative path of the rule file(.xlsx or .xls)')
    return parser.parse_args()


def send_request(policy_type, relative_path):
    data = {
        'policy_type': policy_type,
        'file_path': relative_path,
        'device_id_list': '#'
    }
    r = requests.post('http://192.168.120.234:8089/rule/batch_insert', data=data)
    print r.status_code
    print r.text.encode('utf-8')


if __name__ == '__main__':
    args = parse_args()
    send_request(args.type, args.path)
