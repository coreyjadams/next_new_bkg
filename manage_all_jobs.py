import os, sys
import subprocess
import time

from configuration import regions, isotopes, event_count, atomic_numbers, mass_numbers

def main(action):

    if action not in ['--submit', '--status', '--check']:
        raise Exception("action not supported.")

    for isotope in isotopes:
        element = isotope.split('-')[0]
        for region in regions:
            yml_name = '{element}/{region}/nexus_{element}_{region}.yml'.format(element=element, region=region)
            print yml_name

            command = ['production.py', '-y', yml_name, '--stage', element, action]

            proc = subprocess.Popen(command,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE,
                                    env = dict(os.environ))
            retval=proc.poll()
            # the loop executes to wait till the command finish running
            stdout=''
            stderr=''
            while retval is None:
                time.sleep(1.0)
                # while waiting, fetch stdout (including STDERR) to avoid crogging the pipe
                for line in iter(proc.stdout.readline, b''):
                    stdout += line
                for line in iter(proc.stderr.readline, b''):
                    stderr += line
                # update the return value
                retval = proc.poll()




if __name__ == '__main__':

    action = sys.argv[-1]
    main(action)
