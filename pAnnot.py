#!/usr/bin/python3
import argparse
import subprocess
import os
import sys

def main(args):
    # print(args)
    if args['step'] == 'download':
        cmd = ['python', os.path.join('scripts', 'download.py')]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("stdout:", result.stdout)
        if result.stderr:
            print("stderr:", result.stderr)

    elif args['step'] == 'build':
        if args['term'] is not None and len(args['term']) == 2:
            db_name = args['project_name'] if args['project_name'] else '_'.join(args['term'])
            cmd = ['python', os.path.join('scripts', 'build.py'), db_name] + args['term']
            result = subprocess.run(cmd, capture_output=True, text=True)
            print("stdout:", result.stdout)
            if result.stderr:
                print("stderr:", result.stderr)
        else:
            print("pAnnot is stopped: the argument of -t should be defined when -s build is used.")
            sys.exit(1)

    elif args['step'] == 'parse':
        if args['reference'] is not None:
            cmd = ['python', os.path.join('scripts', 'parse.py'), args['reference']]
            result = subprocess.run(cmd, capture_output=True, text=True)
            print("stdout:", result.stdout)
            if result.stderr:
                print("stderr:", result.stderr)
        else:
            print("pAnnot is stopped: the argument of -r should be defined when -s parse is used.")
            sys.exit(1)
    else:
        print("pAnnot is stopped: the argument of -s should be download, build or parse.")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="pAnnot: Term-based Parsing of genome annotations.")
    parser.add_argument('-s', '--step', required = True, action ='store',
        help ='Steps for parsing annotations. They are download, build, or parse.')
    parser.add_argument('-t', '--term', action = 'store', nargs = 2,
        help = 'Terms used for retrieving annotation data when \"-s build\" is used.')
    parser.add_argument('-p', '--project_name', action = 'store', 
        help = 'Assign a name the local database. In default, that is the term.')
    parser.add_argument('-r', '--reference', action = 'store',
        help = 'reference term for paring annotation data when \"-s parse\" is used')
    args = vars(parser.parse_args())

    # 
    main(args)