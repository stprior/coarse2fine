from flask import Flask,request
import json
import table
import table.IO
import os
import codecs
import apprun

app = Flask(__name__)
(translator, opt) = apprun.initialise(app)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/questions/annotated", methods=['POST'])
def annotated_question():
    question_json = request.get_json()    
    js_list = [question_json]

    data = table.IO.TableDataset(js_list, translator.fields, None, False)
    test_data = table.IO.OrderedIterator(dataset=data,
        device=opt.gpu, batch_size=opt.batch_size, train=False, sort=True, sort_within_batch=False)

    # inference
    r_list = []
    for batch in test_data:
        r_list += translator.translate(batch)
    r_list.sort(key=lambda x: x.idx)
    assert len(r_list) == len(js_list), 'len(r_list) != len(js_list): {} != {}'.format(
        len(r_list), len(js_list))

    # output
    pred = r_list[0]
    sql_text = str.format("{}\n",pred.predict(question_json))
    return sql_text

@app.route("/questions", methods=['POST'])
def plain_question():
    question_json = request.get_json()    
    js_list = [question_json]

    data = table.IO.TableDataset(js_list, translator.fields, None, False)
    test_data = table.IO.OrderedIterator(dataset=data,
        device=opt.gpu, batch_size=opt.batch_size, train=False, sort=True, sort_within_batch=False)

    # inference
    r_list = []
    for batch in test_data:
        r_list += translator.translate(batch)
    r_list.sort(key=lambda x: x.idx)
    assert len(r_list) == len(js_list), 'len(r_list) != len(js_list): {} != {}'.format(
        len(r_list), len(js_list))

    # output
    pred = r_list[0]
    sql_text = str.format("{}\n",pred.predict(question_json))
    return sql_text

#want to show known tables
if __name__ == '__main__':
    app.run()