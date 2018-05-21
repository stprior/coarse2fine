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
from path import path
import glob
import json
from tqdm import tqdm
from lib.dbengine import DBEngine
from lib.query import Query

parser = argparse.ArgumentParser(description='evaluate.py')
opts.translate_opts(parser)
opt = parser.parse_args()
torch.cuda.set_device(opt.gpu)
opt.anno = os.path.join(
    opt.data_path, 'annotated_ent/{}.jsonl'.format(opt.split))
opt.source_file = os.path.join(
    opt.data_path, 'data/{}.jsonl'.format(opt.split))
opt.db_file = os.path.join(opt.data_path, 'data/{}.db'.format(opt.split))
opt.pre_word_vecs = os.path.join(opt.data_path, 'embedding')


def main():
    dummy_parser = argparse.ArgumentParser(description='train.py')
    opts.model_opts(dummy_parser)
    opts.train_opts(dummy_parser)
    dummy_opt = dummy_parser.parse_known_args([])[0]

    js_list = table.IO.read_anno_json(opt.anno)

    for fn_model in glob.glob(opt.model_path):
        print(fn_model)
        print(opt.anno)
        opt.model = fn_model

        translator = table.Translator(opt, dummy_opt.__dict__)
        data = table.IO.TableDataset(js_list, translator.fields, None, False)
        test_data = table.IO.OrderedIterator(
            dataset=data, device=opt.gpu, batch_size=opt.batch_size, train=False, sort=True, sort_within_batch=False)

        # inference
        r_list = []
        for batch in test_data:
            r_list += translator.translate(batch)
        r_list.sort(key=lambda x: x.idx)
        assert len(r_list) == len(js_list), 'len(r_list) != len(js_list): {} != {}'.format(
            len(r_list), len(js_list))

        # output
        outfile = os.path.join(opt.data_path, opt.output)
        with codecs.open(outfile, 'w', encoding='utf-8') as f_out:
          for pred, gold in zip(r_list, js_list):
            sql_text = pred.predict(gold)
            f_out.write('{},{}\n'.format(''.join(gold['question']['words']),sql_text))
        print('Done - results written to {}'.format(outfile))


if __name__ == "__main__":
    main()
