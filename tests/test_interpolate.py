from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest
import pybacktrack
from pybacktrack.util.call_system_command import call_system_command
import py


def test_interpolate_file(tmpdir):
    """Test pybacktrack.read_interpolate_function and pybacktrack.interpolate_file functions."""
    
    # Test data directory is in 'data' sub-directory of directory containing this test module.
    test_data_dir = py.path.local(__file__).dirpath('data')
    
    # Original input/output age-to-depth test data.
    curve_filename = test_data_dir.join('ODP-114-699_age-depth-model.txt')
    input_filename = test_data_dir.join('ODP-114-699_strat_boundaries.txt')
    output_base_filename = 'ODP-114-699_strat_boundaries_age_depth.txt'
    output_filename = test_data_dir.join(output_base_filename)
    
    # We'll be writing to temporary directory (provided by pytest 'tmpdir' fixture).
    test_output_filename = tmpdir.join(output_base_filename)
    
    #
    # These function calls are the equivalent of:
    #
    #     python -m pybacktrack.util.interpolate
    #         -cx 1 -cy 0
    #         -r
    #         -c tests/data/ODP-114-699_age-depth-model.txt
    #         tests/data/ODP-114-699_strat_boundaries.txt
    #         tests/data/ODP-114-699_strat_boundaries_age_depth.txt
    #
    
    curve_function, _, _ = pybacktrack.read_interpolate_function(
        str(curve_filename),
        x_column_index=1,
        y_column_index=0)
    
    # Convert x values in 1-column input file to x and y values in 2-column output file.
    pybacktrack.interpolate_file(
        curve_function,
        str(input_filename),
        str(test_output_filename),
        input_x_column_index=0,
        reverse_output_columns=True)
    
    # Compare original output file and temporary output file just written.
    assert test_output_filename.read() == output_filename.read()


def test_interpolate_script(tmpdir):
    """Test the built-in interpolate script."""
    
    # Test data directory is in 'data' sub-directory of directory containing this test module.
    test_data_dir = py.path.local(__file__).dirpath('data')
    
    # Original input/output age-to-depth test data.
    curve_filename = test_data_dir.join('ODP-114-699_age-depth-model.txt')
    input_filename = test_data_dir.join('ODP-114-699_strat_boundaries.txt')
    output_base_filename = 'ODP-114-699_strat_boundaries_age_depth.txt'
    output_filename = test_data_dir.join(output_base_filename)
    
    # We'll be writing to temporary directory (provided by pytest 'tmpdir' fixture).
    test_output_filename = tmpdir.join(output_base_filename)
    
    # The command-line strings to execute:
    #
    #     python -m pybacktrack.util.interpolate
    #         -cx 1 -cy 0
    #         -r
    #         -c tests/data/ODP-114-699_age-depth-model.txt
    #         tests/data/ODP-114-699_strat_boundaries.txt
    #         tests/data/ODP-114-699_strat_boundaries_age_depth.txt
    #
    interpolate_script_command_line = ['python', '-m', 'pybacktrack.util.interpolate',
                                       '-cx', '1', '-cy', '0',
                                       '-r',
                                       '-c', str(curve_filename),
                                       str(input_filename),
                                       str(test_output_filename)]
    
    # Call the system command.
    call_system_command(interpolate_script_command_line)
    
    # Compare original output file and temporary output file just written.
    assert test_output_filename.read() == output_filename.read()
