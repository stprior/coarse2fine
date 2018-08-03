from __future__ import division
from builtins import bytes
import os
import argparse
import math
import codecs
import torch

import table
import table.IO
import opts
from itertools import takewhile, count
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
from path import Path
import glob
import json
from tqdm import tqdm
from lib.dbengine import DBEngine
from lib.query import Query

parser = argparse.ArgumentParser(description='evaluate.py')
opts.translate_opts(parser)
opt = parser.parse_args(['-data_path','/home/stevop/repos/coarse2fine/data_model/wikisql','-model_path','/home/stevop/repos/coarse2fine/data_model/wikisql/pretrain.pt'])
torch.cuda.set_device(opt.gpu)
opt.anno = os.path.join(
    opt.data_path, 'annotated_ent/{}.jsonl'.format(opt.split))
opt.source_file = os.path.join(
    opt.data_path, 'data/{}.jsonl'.format(opt.split))
opt.db_file = os.path.join(opt.data_path, 'data/{}.db'.format(opt.split))
opt.pre_word_vecs = os.path.join(opt.data_path, 'embedding')

def initialise(app):
    dummy_parser = argparse.ArgumentParser(description='train.py')
    opts.model_opts(dummy_parser)
    opts.train_opts(dummy_parser)
    dummy_opt = dummy_parser.parse_known_args([])[0]


    for fn_model in glob.glob(opt.model_path):
        print(fn_model)
        print(opt.anno)
        opt.model = fn_model

        translator = table.Translator(opt, dummy_opt.__dict__)
        return (translator, opt)
