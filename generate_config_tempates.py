import os, sys

from configuration import regions, isotopes, event_count, atomic_numbers, mass_numbers

class cd:
    """Context manager for changing the current working directory

    Taken from: https://stackoverflow.com/questions/431684/how-do-i-cd-in-python/13197763#13197763
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


# For each sample that needs to be generated, we need to know the following info:
# - number of events
# - region
# - isotope
#   - atomic number
#   - mass number

# Additionally, the start id varies between sample.  We reserve 10^7 eventid spots
# For each isotope/region combination.  For samples that get broken up,
# we have to adjust this accordingly inside of the script.


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
    # Take the config templates and generate source/region specific templates:

    # This also generates yml files for each job.

    # Open up the templates, and loop through the isotopes


    init_template = None
    with open('init_template.txt','r') as _in:
        init_template = _in.read()

    if init_template is None:
        raise Exception("Could not read the init template")


    config_template = None
    with open('config_template.txt','r') as _in:
        config_template = _in.read()

    if config_template is None:
        raise Exception("Could not read the init template")

    nexus_yml_template = None
    with open('nexus_yml_template.txt','r') as _in:
        nexus_yml_template = _in.read()

    if nexus_yml_template is None:
        raise Exception("Could not read the init template")

    config_name = 'nexus_{element}_{region}_template_config.mac'
    init_name   = 'nexus_{element}_{region}_template_init.mac'
    yml_name    = 'nexus_{element}_{region}.yml'
    start_id = 0
    for isotope in isotopes:
        element = isotope.split('-')[0]
        # Make a directory for the element, if it doesn't exist:
        if not os.path.isdir(element):
            os.mkdir(element)
        with cd(element):
            for region in regions:
                if not os.path.isdir(region):
                    os.mkdir(region)
                with cd(region):
                    # Write out a template config and init file:
                    this_config_name = config_name.format(element=element, region=region)
                    this_init_name   = init_name.format(element=element, region=region)
                    n_jobs, events_per_job = get_njobs(isotope, region)
                    with open(this_config_name, 'w') as _config:
                        _config.write(
                            config_template.format(
                                element       = element,
                                atomic_number = atomic_numbers[isotope],
                                mass_number   = mass_numbers[isotope],
                                region        = region,
                                random_seed   = "{random_seed}",
                                file_index    = "{file_index}",
                                start_id      = start_id,
                                nevents       = events_per_job,
                            )
                        )
                    with open(this_init_name, 'w') as _init:
                        _init.write(
                            init_template.format(
                                element    = element,
                                region     = region,
                                file_index = "{file_index}",
                            )
                        )

                        if element == "Bi":
                            _init.write('\n/nexus/RegisterDelayedMacro Bi214.mac\n')


                    extra = ""
                    if element == "Bi":
                        extra='''extra_scripts:
                - /n/holylfs02/LABS/guenette_lab/users/cadams/next/nexus/Bi214.mac'''
                    with open(yml_name.format(element=element, region=region), 'w') as _yml:
                        _yml.write(
                            nexus_yml_template.format(
                                element        = element,
                                region         = region,
                                config_name    = this_config_name,
                                init_name      = this_init_name,
                                extra          = extra,
                                n_jobs         = n_jobs,
                                events_per_job = 5000000,
                            )
                        )


                start_id += 10000000


if __name__ == '__main__':
    main()