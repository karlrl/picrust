#!/usr/bin/env python
# File created on 15 Jan 2017
from __future__ import division

__author__ = "Gavin Douglas"
__copyright__ = "Copyright 2011-2017, The PICRUSt Project"
__credits__ = ["Gavin Douglas", "Morgan Langille"]
__license__ = "GPL"
__version__ = "1.1.3"
__maintainer__ = "Gavin Douglas"
__email__ = "gavinmdouglas@gmail.com"
__status__ = "Development"


from cogent.util.option_parsing import parse_command_line_parameters, make_option
from picrust.wrap_hsp import castor_hsp_wrapper
from picrust.util import make_output_dir_for_file

script_info = {}
script_info['brief_description'] = "Given a tree and a set of known " +\
                                   "character states will output " +\
                                   "predictions for unobserved character " +\
                                   "states. Note this does not require a " +\
                                   "separate ancestral state " +\
                                   "reconstruction step to be run."
script_info['script_description'] = "This script performs hidden state " +\
                                    "prediction on tips in the input tree " +\
                                    "with unknown trait values. Typically " +\
                                    "this script is used to predict the " +\
                                    "abundance of gene families present in " +\
                                    "each taxon, given a tree and a set of " +\
                                    "known trait values. This script " +\
                                    "outputs a table of trait predictions."

# Script usage examples from predict_traits.py
# script_info['script_usage'] = [\
# ("","Required options with NSTI:","%prog -a -i trait_table.tab -t reference_tree.newick -r asr_counts.tab -o predict_traits.tab"),\
# ("","Limit predictions to particular tips in OTU table:","%prog -a -i trait_table.tab -t reference_tree.newick -o predict_traits_limited.tab -l otu_table.tab"),
# ("","Reconstruct confidence","%prog -a -i trait_table.tab -t reference_tree.newick  -o predict_traits.tab")
# ]

HSP_METHODS = ['emp_prob', 'mk_model', 'mp', 'pic', 'sqp']

# Define command-line interface
script_info['output_description'] = "Output is a tab-delimited table of " +\
                                   "predicted character states"
script_info['required_options'] = [

  make_option('-i', '--observed_trait_table', type="existing_filepath",
              help='the input trait table describing directly observed ' +
                   'traits (e.g. sequenced genomes) in tab-delimited format'),

  make_option('-t', '--tree', type="existing_filepath",
              help='the full reference tree, in newick format')
]

script_info['optional_options'] = [

  make_option('-o', '--output_trait_table', type="new_filepath",
              default='predicted_traits.tsv',
              help='the output filepath for trait predictions ' +
                   '[default: %default]'),

  make_option('--ci_out', type="new_filepath",
              default='predicted_traits_ci.tsv',
              help='the output filepath for confidence intervals trait ' +
                   'predictions (if -c option set) [default: %default]'),

  make_option('-m', '--hsp_method', default='emp_prob', choices=HSP_METHODS,
              help='HSP method to use, options: ' +
                   ", ".join(HSP_METHODS) + '. "emp_prob": ' +
                   'predict discrete traits based on empirical state ' +
                   'probabilities across tips. "mk_model": predict ' +
                   'discrete traits based on fixed-rates continuous time ' +
                   'Markov model. "mp": predict discrete traits using max ' +
                   'parsimony. "pic": predict continuous trait with ' +
                   'phylogentic independent contrast. "sqp": ' +
                   'reconstruct continuous traits using squared-change ' +
                   'parsimony [default: %default]'),

  make_option('-n', '--calculate_NSTI', default=False,
              action="store_true",
              help='if specified, calculate NSTI and add to output file ' +
                   '[default: %default]'),

  make_option('-c', "--confidence", default=False, action="store_true",
              help='if specified, output 95% confidence intervals (only ' +
                   'possible for mk_model, emp_prob, and mp settings) ' +
                   '[default: %default]'),

  make_option('--check', default=False, action="store_true",
              help='if specified, check input trait table before hsp ' +
                   '[default: %default]'),

  make_option('--threads', default=1, type="int",
              help='Number of threads to use when running mk_model ' +
                   '[default: %default]'),

  make_option('--debug', default=False, action="store_true",
              help='Flag to specify run in debugging mode. ' +
                   '[default: %default]')
]

script_info['version'] = __version__


def main():

    option_parser, opts, args = parse_command_line_parameters(**script_info)

    hsp_table, ci_table = castor_hsp_wrapper(
                                        tree_path=opts.input_tree_fp,
                                        trait_table_path=opts.trait_table_path,
                                        hsp_method=opts.hsp_method,
                                        calc_nsti=opts.calculate_NSTI,
                                        calc_ci=opts.confidence,
                                        check_input=opts.check,
                                        threads=opts.threads,
                                        HALT_EXEC=opts.debug)

    # Output the table to file.
    make_output_dir_for_file(opts.output_trait_table)
    hsp_table.writeToFile(opts.output_trait_table, sep='\t')

    # Output the CI file as well if option set.
    if (opts.confidence):
        make_output_dir_for_file(opts.ci_out)
        ci_table.writeToFile(opts.ci_out, sep='\t')


if __name__ == "__main__":
    main()
