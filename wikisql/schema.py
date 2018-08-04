import json
import graphene
import os
import codecs

js_list = []

class WikiSqlTable(graphene.ObjectType):
    id = graphene.ID()
    header = graphene.List(graphene.String)
    rows = graphene.List(graphene.List(graphene.String))

    def resolve_rows(self, info):
        return [['1','a','a'],['2','b','b']]

def parse_jsonl(json_table_desc):
    return WikiSqlTable(id = json_table_desc['id'],
        header = json_table_desc['header'],
        rows = json_table_desc['rows'])

class RootQuery(graphene.ObjectType):
    tables = graphene.List(WikiSqlTable, id=graphene.Argument(graphene.String))

    def resolve_tables(self, info, id=None):
        if id is None:
            tables = [parse_jsonl(jsonline) for jsonline in js_list[1:10]]
            return tables

        return [parse_jsonl(jsonline) for jsonline in js_list if jsonline.id == id]

def build_schema(data_path):
    global js_list
    table_path = os.path.join(data_path,'test.tables.jsonl')
    with codecs.open(table_path, "r", "utf-8") as corpus_file:
        js_list = [json.loads(line) for line in corpus_file]
    return RootQuery

