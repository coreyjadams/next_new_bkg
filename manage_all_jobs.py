import os, sys
import subprocess
import time
import sqlite3

from configuration import regions, isotopes, event_count, atomic_numbers, mass_numbers

from database import DatasetReader, ProjectReader
from config import ProjectConfig

from utils import ProjectHandler

# This script checks the production of each set of files.  If it is finished,
# It calculates the passing rate of events and stores other useful information

# If it is not finished, it submits the jobs.

# function to initialize the database file if not present:
def connect():
    return sqlite3.connect('next_new_bkg.db')

def init_db():
    conn = connect()
    c = conn.cursor()

    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS next_new_bkg_summary(
            id INTEGER AUTO_INCREMENT,
            dataset TEXT,
            element TEXT,
            region TEXT,
            n_simulated INTEGER,
            n_passed INTEGER,
            n_jobs INTEGER,
            PRIMARY KEY(id)
        )
    '''
    c.execute(create_table_sql)


def get_njobs(isotope, region):
    # First, find out the number of events needed:
    n_events_total = int(event_count[isotope][region])

    #Less than 5e6 events we run in just one job:
    if n_events_total <= 5E6:
        return 1, n_events_total

    # Otherwise, assume about 5 million events per job (plus 1 job to deal with rounding):
    n_jobs = int(n_events_total / 5E6)

    # If the number of jobs is too high (>5000) we increase the events per job:
    if n_jobs > 5000:
        n_jobs = 5000

    #Calculate the number of events per job:

    events_per_job = int(n_events_total / n_jobs )

    return n_jobs, events_per_job


def main():

    # if action not in ['--submit', '--status', '--check']:
    #     raise Exception("action not supported.")


    pr = ProjectReader()
    dr = DatasetReader()

    # Get the list of datasets that are in the production database:
    datasets = pr.list_datasets()

    datasets = [ ds for tupl in datasets for ds in tupl]

    for isotope in isotopes:
        element = isotope.split('-')[0]
        for region in regions:
            yml_name = '{element}/{region}/nexus_{element}_{region}.yml'.format(element=element, region=region)

            # Read in the yml file:
            pc = ProjectConfig(yml_name)
            stage = pc.stage(element)

            print stage.output_dataset()

            # First, check if this project is in the database:
            if stage.output_dataset() in datasets:
                # Check the output of this dataset.

                # From the yml, get the number off jobs and the events per job:
                total_events_submitted = stage.total_output_events()
                total_events_produced  = dr.sum(
                    dataset=stage.output_dataset(),
                    target='nevents',
                    type=0)
                n_jobs = stage.n_jobs()

                # From the database figure out how many jobs succeeded,
                # and how many events were produced:
                n_jobs_succeeded = dr.get_n_successful_jobs(stage.output_dataset())

                print "For dataset {}, {} of {} jobs completed".format(
                    stage.output_dataset(),
                    n_jobs_succeeded, n_jobs)
                print "  {} of {} events passed the selection".format(
                    total_events_produced,
                    total_events_submitted)

                # If the number of jobs completed equals the number of jobs submitted,
                # it's done.

                if n_jobs_succeeded == n_jobs:
                    insertion_sql = '''
                        INSERT INTO next_new_bkg_summary(dataset, element, region, n_simulated, n_passed, n_jobs)
                        VALUES (?, ?, ?, ?, ?, ?)
                    '''
                    curr = connect().cursor()
                    tupl = (stage.output_dataset(), element, region, int(total_events_submitted), int(total_events_produced), int(n_jobs))
                    curr.execute(insertion_sql, tupl)

                elif n_jobs_succeeded == 0:
                    print "Completely resubmitting {}".format(stage.output_dataset())
                    # clean and resubmit
                    ph = ProjectHandler(yml_name, action='clean', stage=element)
                    ph.act()
                    ph = ProjectHandler(yml_name, action='submit', stage=element)
                else:
                    # Doing makeup jobs, just report it:
                    print "Requires makeup jobs"
            else:
                # Need to submit it for the first time.
                ph = ProjectHandler(yml_name, action='submit', stage=element)
                ph.act()
                print "Nothing submitted."
            # Find out how many


            # command = ['production.py', '-y', yml_name, '--stage', element, action]

            # proc = subprocess.Popen(command,
            #                         stdout = subprocess.PIPE,
            #                         stderr = subprocess.PIPE,
            #                         env = dict(os.environ))
            # retval=proc.poll()
            # # the loop executes to wait till the command finish running
            # stdout=''
            # stderr=''
            # while retval is None:
            #     time.sleep(1.0)
            #     # while waiting, fetch stdout (including STDERR) to avoid crogging the pipe
            #     for line in iter(proc.stdout.readline, b''):
            #         stdout += line
            #     for line in iter(proc.stderr.readline, b''):
            #         stderr += line
            #     # update the return value
            #     retval = proc.poll()

            # return_code = proc.returncode

            # if return_code != 0:
            #     raise Exception("Failed")

            # else:
            #     print stdout


if __name__ == '__main__':
    # Delete the database, if it exist:
    try:
        os.path.remove('next_new_bkg.db')
    except:
        pass
    connect()
    init_db()
    main()
