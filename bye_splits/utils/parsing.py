# coding: utf-8

_all_ = [ ]

import os
import sys
parent_dir = os.path.abspath(__file__ + 3 * '/..')
sys.path.insert(0, parent_dir)

def add_parameters(parser):
    parser.add_argument('--sel', default='all', type=str,
                        help='Selection used to select cluster under study.')
    parser.add_argument('--reg', choices=('Si', 'ECAL', 'HCAL', 'All', 'MaxShower', 'ExcludeMaxShower'),
                        default='Si', type=str,
                        help='Z region in the detector for the trigger cell geometry.')
    seed_help = ( 'Size of the window used for seeding in the phi ' +
                  'direction. The size in R/z is always 1/. A larger size' +
                  'captures more information but consumes more ' +
                  'firmware resources.' )
    parser.add_argument('--seed_window', help=seed_help, default=1, type=int)
    parser.add_argument('--smooth_kernel',
                        choices=('default', 'flat_top'),
                        default='default', type=str,
                        help='Type of smoothing kernel being applied.')
    parser.add_argument('--cluster_algo',
                        choices=('max_energy', 'min_distance'),
                        default='min_distance', type=str,
                        help='Clustering algorithm applied.')
    parser.add_argument('--user', type=str, help='LXPlus username.')
    parser.add_argument('--cluster_studies', type=bool, help='boolean, whether or not to read and write files for the cluster size studies steps.', default=False)