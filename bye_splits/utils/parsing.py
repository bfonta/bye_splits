# coding: utf-8

_all_ = [ ]

import os
import sys
parent_dir = os.path.abspath(__file__ + 3 * '/..')
sys.path.insert(0, parent_dir)

def add_parameters(parser):
    parser.add_argument('-m', '--ipar', help='iterative algorithm tunable parameter',
                        default=0.5, type=float)
    parser.add_argument('-s', '--sel', default='splits_only', type=str,
                        help='Selection used to select cluster under study.')
    parser.add_argument('--reg', choices=('Si', 'ECAL', 'MaxShower'),
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