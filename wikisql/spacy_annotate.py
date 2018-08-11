import spacy
import codecs
import json
from spacy.tokens import Doc
nlp = spacy.load('en_core_web_lg')

def add_pos_annotations(annotated_question):
  w_list = annotated_question['question']['gloss']
  ws_list = [it.isspace() for it in annotated_question['question']['after']]
  doc = Doc(nlp.vocab, words=w_list, spaces=ws_list)
  for name, proc in nlp.pipeline:
      doc = proc(doc)
  annotated_question['question']['ent'] = [tk.tag_ for tk in doc]
  assert(len(annotated_question['question']['ent']) == len(annotated_question['question']['words']))
  return 
