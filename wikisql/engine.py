import opts
import argparse
import os
import torch
import table
import glob
import json
from annotate import annotate_example, load_tables

from spacy_annotate import add_pos_annotations

tables = {}
translator = {}
opt = {}

def init(data_path):
  global opt
  model_path = os.path.join(data_path,'pretrain.pt')
  parser = argparse.ArgumentParser(description='Exploration.ipynb')
  opts.translate_opts(parser)
  opt = parser.parse_args(
      ["-split","dev","-output","test.txt","-data_path",data_path,"-model_path",model_path])

  opt.anno = os.path.join(
      opt.data_path, 'annotated_ent/{}.jsonl'.format(opt.split))
  opt.source_file = os.path.join(
      opt.data_path, 'data/{}.jsonl'.format(opt.split))
  opt.db_file = os.path.join(opt.data_path, 'data/{}.db'.format(opt.split))
  table_file = os.path.join(opt.data_path, 'data/{}.tables.jsonl'.format(opt.split))
  opt.pre_word_vecs = os.path.join(opt.data_path, 'embedding')
  torch.cuda.set_device(opt.gpu)
  dummy_parser = argparse.ArgumentParser(description='train.py')
  opts.model_opts(dummy_parser)
  opts.train_opts(dummy_parser)
  dummy_opt = dummy_parser.parse_known_args([])[0]
  fn_model = glob.glob(opt.model_path)[0]
  opt.model=fn_model
  global tables, translator
  tables = load_tables(table_file)
  translator = table.Translator(opt, dummy_opt.__dict__)


def ask_question(table_id, question_text):
  question = {"phase": 1, 
              "table_id": table_id, 
              "question": question_text,
              "sql": {"sel": 1, "conds": [[1, 0, "Butler CC (KS)"]], "agg": 1}}
  table_instance = tables[table_id]
  annotated_question = annotate_example(question, table_instance)
  add_pos_annotations(annotated_question)

  js_list = [annotated_question]
  data = table.IO.TableDataset(js_list, translator.fields, None, False)
  test_data = table.IO.OrderedIterator(dataset=data,device=opt.gpu, batch_size=opt.batch_size, train=False, sort=True, sort_within_batch=False)
  batch=next(iter(test_data))
  result_list=translator.translate(batch)
  pred = result_list[0]
  

  return pred.predict(annotated_question)



