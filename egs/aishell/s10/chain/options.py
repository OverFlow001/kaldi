#!/usr/bin/env python3

# Copyright 2019 Mobvoi AI Lab, Beijing, China (author: Fangjun Kuang)
# Apache 2.0

import argparse
import os


def _set_training_args(parser):
    parser.add_argument('--train.cegs-dir',
                        dest='cegs_dir',
                        help='cegs dir containing comibined cegs.*.scp',
                        required=True,
                        type=str)

    parser.add_argument('--train.den-fst',
                        dest='den_fst_filename',
                        help='denominator fst filename',
                        required=True,
                        type=str)

    parser.add_argument('--train.egs-left-context',
                        dest='egs_left_context',
                        help='egs left context',
                        required=True,
                        type=int)

    parser.add_argument('--train.egs-right-context',
                        dest='egs_right_context',
                        help='egs right context',
                        required=True,
                        type=int)

    parser.add_argument('--train.num-epochs',
                        dest='num_epochs',
                        help='number of epochs to train',
                        required=True,
                        type=int)

    parser.add_argument('--train.lr',
                        dest='learning_rate',
                        help='learning rate',
                        required=True,
                        type=float)

    parser.add_argument('--train.l2-regularize',
                        dest='l2_regularize',
                        help='l2 regularize',
                        required=True,
                        type=float)


def _check_training_args(args):
    assert os.path.isdir(args.cegs_dir)

    assert os.path.isfile(args.den_fst_filename)

    assert args.egs_left_context > 0
    assert args.egs_right_context > 0

    assert args.num_epochs > 0
    assert args.learning_rate > 0
    assert args.l2_regularize > 0


def _check_args(args):

    _check_training_args(args)

    assert os.path.isfile(args.lda_mat_filename)

    # although -1 means to use CPU in `kaldi.SelectGpuDevice()`
    # we do NOT want to use CPU here so we require it to be >= 0
    assert args.device_id >= 0

    assert args.feat_dim > 0
    assert args.output_dim > 0
    assert args.hidden_dim > 0

    assert args.kernel_size_list is not None
    assert len(args.kernel_size_list) > 0

    assert args.dilation_list is not None
    assert len(args.dilation_list) > 0

    args.kernel_size_list = [int(k) for k in args.kernel_size_list.split(', ')]

    args.dilation_list = [int(k) for k in args.dilation_list.split(', ')]

    assert len(args.kernel_size_list) == len(args.dilation_list)


def get_args():
    parser = argparse.ArgumentParser(
        description='chain training in PyTorch with kaldi pybind')

    _set_training_args(parser)

    parser.add_argument('--dir',
                        help='dir to save results. The user has to '
                        'create it before calling this script.',
                        required=True,
                        type=str)

    parser.add_argument('--device-id',
                        dest='device_id',
                        help='GPU device id',
                        required=True,
                        type=int)

    parser.add_argument(
        '--lda-mat-filename',
        dest='lda_mat_filename',
        help='affine-transform-file in fixed-affine-layer of kaldi',
        required=True,
        type=str)

    parser.add_argument('--feat-dim',
                        dest='feat_dim',
                        help='nn input dimension',
                        required=True,
                        type=int)

    parser.add_argument('--output-dim',
                        dest='output_dim',
                        help='nn output dimension',
                        required=True,
                        type=int)

    parser.add_argument('--hidden-dim',
                        dest='hidden_dim',
                        help='nn hidden dimension',
                        required=True,
                        type=int)

    parser.add_argument('--kernel-size-list',
                        dest='kernel_size_list',
                        help='kernel size list',
                        required=True,
                        type=str)

    parser.add_argument('--dilation-list',
                        dest='dilation_list',
                        help='dilation list',
                        required=True,
                        type=str)

    args = parser.parse_args()

    _check_args(args)
    return args
