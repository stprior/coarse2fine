from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import os
import records
# import ujson as json
import json
from stanza.nlp.corenlp import CoreNLPClient
from tqdm import tqdm
import copy
from lib.common import count_lines, detokenize
from lib.query import Query


client = None


def annotate(sentence, lower=True, include_pos=False):
    global client
    if client is None:
        annotators = 'ssplit,tokenize'
        if include_pos: annotators = annotators + ',pos'
        client = CoreNLPClient(default_annotators=annotators.split(','))
    words, gloss, after, pos = [], [], [], []
    for s in client.annotate(sentence):
        for t in s:
            words.append(t.word)
            gloss.append(t.originalText)
            after.append(t.after)
            if include_pos: pos.append(t.pos)
    if lower:
        words = [w.lower() for w in words]
    if include_pos: return {        
        'words': words,
        'after': after,
        'ent': pos,
        'gloss': gloss,        
    }
    return {        
        'words': words,
        'after': after,
        'gloss': gloss,        
    }


def annotate_example(example, table):
    ann = {
        'table_id': example['table_id'],
        'question': annotate(example['question'], include_pos=True),
        'table': {
            'header': [annotate(h) for h in table['header']],
        }
    }
    ann['query'] = sql = copy.deepcopy(example['sql'])
    for c in ann['query']['conds']:
        c[-1] = annotate(str(c[-1]))

    q1 = 'SYMSELECT SYMAGG {} SYMCOL {}'.format(
        Query.agg_ops[sql['agg']], table['header'][sql['sel']])
    q2 = ['SYMCOL {} SYMOP {} SYMCOND {}'.format(
        table['header'][col], Query.cond_ops[op], detokenize(cond)) for col, op, cond in sql['conds']]
    if q2:
        q2 = 'SYMWHERE ' + ' SYMAND '.join(q2) + ' SYMEND'
    else:
        q2 = 'SYMEND'
    inp = 'SYMSYMS {syms} SYMAGGOPS {aggops} SYMCONDOPS {condops} SYMTABLE {table} SYMQUESTION {question} SYMEND'.format(
        syms=' '.join(['SYM' + s for s in Query.syms]),
        table=' '.join(['SYMCOL ' + s for s in table['header']]),
        question=example['question'],
        aggops=' '.join([s for s in Query.agg_ops]),
        condops=' '.join([s for s in Query.cond_ops]),
    )
    ann['seq_input'] = annotate(inp)
    out = '{q1} {q2}'.format(q1=q1, q2=q2) if q2 else q1
    ann['seq_output'] = annotate(out)
    ann['where_output'] = annotate(q2)
    assert 'symend' in ann['seq_output']['words']
    assert 'symend' in ann['where_output']['words']
    return ann


def is_valid_example(e):
    if not all([h['words'] for h in e['table']['header']]):
        return False
    headers = [detokenize(h).lower() for h in e['table']['header']]
    if len(headers) != len(set(headers)):
        return False
    input_vocab = set(e['seq_input']['words'])
    for w in e['seq_output']['words']:
        if w not in input_vocab:
            print('query word "{}" is not in input vocabulary.\n{}'.format(
                w, e['seq_input']['words']))
            return False
    input_vocab = set(e['question']['words'])
    for col, op, cond in e['query']['conds']:
        for w in cond['words']:
            if w not in input_vocab:
                print('cond word "{}" is not in input vocabulary.\n{}'.format(
                    w, e['question']['words']))
                return False
    return True


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--din', default='/home/stevop/repos/coarse2fine/data_model/wikisql/data', help='data directory')
    parser.add_argument(
        '--dout', default='/home/stevop/repos/coarse2fine/data_model/wikisql/annotated_ent', help='output directory')
    args = parser.parse_args()

    if not os.path.isdir(args.dout):
        os.makedirs(args.dout)

    for split in ['pred']:
        fsplit = os.path.join(args.din, split) + '.jsonl'
        ftable = os.path.join(args.din, split) + '.tables.jsonl'
        fout = os.path.join(args.dout, split) + '.jsonl'

        print('annotating {}'.format(fsplit))
        with open(fsplit) as fs, open(ftable) as ft, open(fout, 'wt') as fo:
            print('loading tables')
            tables = {}
            for line in tqdm(ft, total=count_lines(ftable)):
                d = json.loads(line)
                tables[d['id']] = d
            print('loading examples')
            n_written = 0
            for line in tqdm(fs, total=count_lines(fsplit)):
                d = json.loads(line)
                try:
                    a = annotate_example(d, tables[d['table_id']])
                except IndexError:
                    print("Table {} not found".format(d['table_id']))
                    raise
                if not is_valid_example(a):
                    raise Exception(str(a))

                gold = Query.from_tokenized_dict(a['query'])
                reconstruct = Query.from_sequence(
                    a['seq_output'], a['table'], lowercase=True)
                if gold.lower() != reconstruct.lower():
                    raise Exception(
                        'Expected:\n{}\nGot:\n{}'.format(gold, reconstruct))
                a['id'] = '{}-{}'.format(split, n_written)
                fo.write(json.dumps(a) + '\n')
                n_written += 1
            print('wrote {} examples'.format(n_written))
