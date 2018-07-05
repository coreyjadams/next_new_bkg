
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

# Enumerate the regions:
regions = [
    'ICS',
    'PEDESTAL',
    'SHIELDING_LEAD',
    'SHIELDING_STEEL',
    'SHIELDING_STRUCT',
    'VESSEL',
    'ANODE_QUARTZ',
    'DRIFT_TUBE',
    'HDPE_TUBE',
    'CARRIER_PLATE',
    'ENCLOSURE_BODY',
    'ENCLOSURE_WINDOW',
    'OPTICAL_PAD',
    'PMT_BASE',
    'PMT_BODY',
    'DB_PLUG',
    'DICE_BOARD',
    'EXTRA_VESSEL',
    'SUPPORT_PLATE',
]

# enumerate the isotopes:
isotopes = [
    'Bi-214',
    'Co-60',
    'K-40',
    'Tl-208',
]

event_count = {
    'Bi-214' : {
        'ICS' : 2E6,
        'PEDESTAL' : 2E8,
        'SHIELDING_LEAD' : 2E9,
        'SHIELDING_STEEL' : 2E7,
        'SHIELDING_STRUCT' : 2E10,
        'VESSEL' : 1E8,
        'ANODE_QUARTZ' : 5E5,
        'DRIFT_TUBE' : 1E7,
        'HDPE_TUBE' : 5E5,
        'CARRIER_PLATE' : 1E6,
        'ENCLOSURE_BODY' : 5E5,
        'ENCLOSURE_WINDOW' : 1E6,
        'OPTICAL_PAD' : 5E5,
        'PMT_BASE' : 5E6,
        'PMT_BODY' : 1E6,
        'DB_PLUG' : 2E7,
        'DICE_BOARD' : 1E6,
        'EXTRA_VESSEL' : 2E9,
        'SUPPORT_PLATE' : 1E6,
    },
    'Co-60' : {
        'ICS' : 1E7,
        'PEDESTAL' : 5E8,
        'SHIELDING_LEAD' : 5E8,
        'SHIELDING_STEEL' : 1E7,
        'SHIELDING_STRUCT' : 2E8,
        'VESSEL' : 1E9,
        'ANODE_QUARTZ' : 5E5,
        'DRIFT_TUBE' : 2E6,
        'HDPE_TUBE' : 5E5,
        'CARRIER_PLATE' : 2E6,
        'ENCLOSURE_BODY' : 5E5,
        'ENCLOSURE_WINDOW' : 1E6,
        'OPTICAL_PAD' : 5E5,
        'PMT_BASE' : 1E6,
        'PMT_BODY' : 2E7,
        'DB_PLUG' : 5E5,
        'DICE_BOARD' : 5E5,
        'EXTRA_VESSEL' : 2E7,
        'SUPPORT_PLATE' : 5E6,
    },
    'K-40' : {
        'ICS' :  1E7,
        'PEDESTAL' :  2E9,
        'SHIELDING_LEAD' :  5E8,
        'SHIELDING_STEEL' :  1E8,
        'SHIELDING_STRUCT' :  5E10,
        'VESSEL' :  1E9,
        'ANODE_QUARTZ' :  1E6,
        'DRIFT_TUBE' :  5E7,
        'HDPE_TUBE' :  2E7,
        'CARRIER_PLATE' :  5E6,
        'ENCLOSURE_BODY' :  1E6,
        'ENCLOSURE_WINDOW' :  5E6,
        'OPTICAL_PAD' :  2E6,
        'PMT_BASE' :  5E7,
        'PMT_BODY' :  5E7,
        'DB_PLUG' :  5E7,
        'DICE_BOARD' :  1E8,
        'EXTRA_VESSEL' :  1E10,
        'SUPPORT_PLATE' :  5E6,
    },
    'Tl-208' : {
        'ICS' : 5E5,
        'PEDESTAL' : 1E8,
        'SHIELDING_LEAD' : 2E8,
        'SHIELDING_STEEL' : 1E7,
        'SHIELDING_STRUCT' : 2E9,
        'VESSEL' : 2E7,
        'ANODE_QUARTZ' : 5E5,
        'DRIFT_TUBE' : 5E6,
        'HDPE_TUBE' : 5E5,
        'CARRIER_PLATE' : 5E5,
        'ENCLOSURE_BODY' : 5E5,
        'ENCLOSURE_WINDOW' : 5E5,
        'OPTICAL_PAD' : 5E5,
        'PMT_BASE' : 2E7,
        'PMT_BODY' : 1E6,
        'DB_PLUG' : 2E7,
        'DICE_BOARD' : 5E5,
        'EXTRA_VESSEL' : 1E9,
        'SUPPORT_PLATE' : 5E5,
    }
}

atomic_numbers = {
    'Co-60' : 27,
    'Bi-214': 83,
    'Tl-208': 81,
    'K-40'  : 19,
}

mass_numbers = {
    'Co-60' : 60,
    'Bi-214': 214,
    'Tl-208': 208,
    'K-40'  : 40,
}

# *** Bi-214 events ***
# region = ICS , nevents = 0.116E+07 -> generate 2E6
# region = PEDESTAL , nevents = 0.762E+08 -> generate 2E8
# region = SHIELDING_LEAD , nevents = 0.862E+09 -> generate 2E9
# region = SHIELDING_STEEL , nevents = 0.110E+08 -> generate 2E7
# region = SHIELDING_STRUCT , nevents = 0.108E+11 -> generate 2E10
# region = VESSEL , nevents = 0.574E+08 -> generate 1E8
# region = ANODE_QUARTZ , nevents = 0.767E+05 -> generate 5E5
# region = DRIFT_TUBE , nevents = 0.489E+07 -> generate 1E7. for 3e-2 efficiency (E>600 keV): 3.e5 events
# region = HDPE_TUBE , nevents = 0.180E+06 -> generate 5E5
# region = CARRIER_PLATE , nevents = 0.407E+06 -> generate 1E6
# region = ENCLOSURE_BODY , nevents = 0.931E+05 -> generate 5E5
# region = ENCLOSURE_WINDOW , nevents = 0.500E+06 -> generate 1E6
# region = OPTICAL_PAD , nevents = 0.892E+05 -> generate 5E5
# region = PMT_BASE , nevents = 0.312E+07 -> generate 5E6. for 1.6e-3 efficiency (E>600 keV): 8.e3 events
# region = PMT_BODY , nevents = 0.663E+06 -> generate 1E6
# region = DB_PLUG , nevents = 0.122E+08 -> generate 2E7
# region = DICE_BOARD , nevents = 0.349E+06 -> generate 1E6
# region = EXTRA_VESSEL , nevents = 0.130E+10 -> generate 2E9
# region = SUPPORT_PLATE , nevents = 0.574E+06 -> generate 1E6
# *** Co-60 events ***
# region = ICS , nevents = 0.398E+07 -> generate 1E7
# region = PEDESTAL , nevents = 0.158E+09 -> generate 5E8
# region = SHIELDING_LEAD , nevents = 0.197E+09 -> generate 5E8
# region = SHIELDING_STEEL , nevents = 0.658E+07 -> generate 1E7
# region = SHIELDING_STRUCT , nevents = 0.129E+09 -> generate 2E8
# region = VESSEL , nevents = 0.316E+09 -> generate 1E9. for 3.4e-4 efficiency (E>600 keV): 3.4e5 events
# region = ANODE_QUARTZ , nevents = 0.682E+04 -> generate 5E5
# region = DRIFT_TUBE , nevents = 0.131E+07 -> generate 2E6. for 5e-2 efficiency (E>600 keV): 1.e5 events
# region = HDPE_TUBE , nevents = 0.202E+06 -> generate 5E5
# region = CARRIER_PLATE , nevents = 0.139E+07 -> generate 2E6
# region = ENCLOSURE_BODY , nevents = 0.319E+06 -> generate 5E5
# region = ENCLOSURE_WINDOW , nevents = 0.560E+06 -> generate 1E6
# region = OPTICAL_PAD , nevents = 0.183E+05 -> generate 5E5
# region = PMT_BASE , nevents = 0.587E+06 -> generate 1E6
# region = PMT_BODY , nevents = 0.720E+07 -> generate 2E7
# region = DB_PLUG , nevents = 0.133E+06 -> generate 5E5
# region = DICE_BOARD , nevents = 0.377E+05 -> generate 5E5
# region = EXTRA_VESSEL , nevents = 0.111E+08 -> generate 2E7
# region = SUPPORT_PLATE , nevents = 0.196E+07 -> generate 5E6
# *** K-40 events ***
# region = ICS , nevents = 0.601E+07 -> generate 1E7
# region = PEDESTAL , nevents = 0.117E+10 -> generate 2E9
# region = SHIELDING_LEAD , nevents = 0.295E+09 -> generate 5E8
# region = SHIELDING_STEEL , nevents = 0.506E+08 -> generate 1E8
# region = SHIELDING_STRUCT , nevents = 0.380E+11 -> generate 5E10
# region = VESSEL , nevents = 0.338E+09 -> generate 1E9
# region = ANODE_QUARTZ , nevents = 0.410E+06 -> generate 1E6
# region = DRIFT_TUBE , nevents = 0.183E+08 -> generate 5E7. for 5e-3 efficiency (E>600 keV): 2.5e5 events
# region = HDPE_TUBE , nevents = 0.120E+08 -> generate 2E7
# region = CARRIER_PLATE , nevents = 0.210E+07 -> generate 5E6
# region = ENCLOSURE_BODY , nevents = 0.481E+06 -> generate 1E6
# region = ENCLOSURE_WINDOW , nevents = 0.189E+07 -> generate 5E6. for 8e-4 efficiency (E>600 keV): 4.e3 events
# region = OPTICAL_PAD , nevents = 0.701E+06 -> generate 2E6
# region = PMT_BASE , nevents = 0.221E+08 -> generate 5E7. for 1.8e-4 efficiency (E>600 keV): 9e3 events
# region = PMT_BODY , nevents = 0.229E+08 -> generate 5E7
# region = DB_PLUG , nevents = 0.149E+08 -> generate 5E7
# region = DICE_BOARD , nevents = 0.642E+08 -> generate 1E8. for 2e-3 efficiency (E>600 keV): 2e5 events
# region = EXTRA_VESSEL , nevents = 0.565E+10 -> generate 1E10
# region = SUPPORT_PLATE , nevents = 0.297E+07 -> generate 5E6
# *** Tl-208 events ***
# region = ICS , nevents = 0.143E+06 -> generate 5E5
# region = PEDESTAL , nevents = 0.559E+08 -> generate 1E8
# region = SHIELDING_LEAD , nevents = 0.832E+08 -> generate 2E8
# region = SHIELDING_STEEL , nevents = 0.335E+07 -> generate 1E7
# region = SHIELDING_STRUCT , nevents = 0.107E+10 -> generate 2E9
# region = VESSEL , nevents = 0.929E+07 -> generate 2E7
# region = ANODE_QUARTZ , nevents = 0.256E+06 -> generate 5E5
# region = DRIFT_TUBE , nevents = 0.185E+07 -> generate 5E6. for 4e-2 efficiency (E>600 keV): 2.e5 events
# region = HDPE_TUBE , nevents = 0.219E+05 -> generate 5E5
# region = CARRIER_PLATE , nevents = 0.499E+05 -> generate 5E5
# region = ENCLOSURE_BODY , nevents = 0.114E+05 -> generate 5E5
# region = ENCLOSURE_WINDOW , nevents = 0.249E+06 -> generate 5E5
# region = OPTICAL_PAD , nevents = 0.262E+05 -> generate 5E5
# region = PMT_BASE , nevents = 0.109E+08 -> generate 2E7. for 2.6e-3 efficiency (E>600 keV): 5.2e4 events
# region = PMT_BODY , nevents = 0.360E+06 -> generate 1E6
# region = DB_PLUG , nevents = 0.933E+07 -> generate 2E7
# region = DICE_BOARD , nevents = 0.617E+05 -> generate 5E5
# region = EXTRA_VESSEL , nevents = 0.582E+09 -> generate 1E9
# region = SUPPORT_PLATE , nevents = 0.702E+05 -> generate 5E5
# *** Xe-136 events ***
# region = ACTIVE , nevents = 0.749E+03 -> generate 5E5
