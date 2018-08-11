import json
import graphene
import os
import codecs
import engine

js_list = []
js_lookup = {}


class WikiSqlTable(graphene.ObjectType):
    id = graphene.ID()
    tablename = graphene.String()
    header = graphene.List(graphene.String)
    rows = graphene.List(graphene.List(graphene.String))

    def resolve_rows(self, info):
        return [['1','a','a'],['2','b','b']]

def make_wikisqltable(json_table_desc):
    return WikiSqlTable(id = json_table_desc['id'],
        tablename = json_table_desc.get('page_title', ''),
        header = json_table_desc['header'],
        rows = json_table_desc['rows'])

class RootQuery(graphene.ObjectType):
    tables = graphene.List(WikiSqlTable, id=graphene.Argument(graphene.String))

    def resolve_tables(self, info, id=None):
        if id is None:
            tables = [make_wikisqltable(jsonline) for jsonline in js_list[1:50]]
            return tables
        jsonline = js_lookup[id]
        return [make_wikisqltable(jsonline)]

class AskQuestion(graphene.Mutation):
    class Arguments:
        table_id = graphene.ID()
        question_text = graphene.String()
    sql = graphene.String()

    def mutate(self, info, table_id, question_text):
        sql = engine.ask_question(table_id,question_text)
        return AskQuestion(sql=sql)

class RootMutations(graphene.ObjectType):
    ask_question = graphene.Field(AskQuestion)


def save_table(json_line):
    jsl = json.loads(json_line)
    js_lookup[jsl['id']] = jsl
    return jsl
    
def build_schema(data_path):
    global js_list
    table_path = os.path.join(data_path,'test.tables.jsonl')
    with codecs.open(table_path, "r", "utf-8") as corpus_file:
        js_list = [json.loads(line) for line in corpus_file]
    return (RootQuery, RootMutations)

