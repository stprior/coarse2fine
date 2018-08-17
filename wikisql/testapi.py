import unittest
from schema import build_schema
import graphene
import engine

#end to end test
class TestApi(unittest.TestCase):
    def setUp(self):
        (rootQueryClass,mutationsClass) = build_schema('/home/stevop/repos/coarse2fine/data_model/wikisql/data')
        self.schema = graphene.Schema(query=rootQueryClass, mutation=mutationsClass)
        engine.init('/home/stevop/repos/coarse2fine/data_model/wikisql')

    def test_mutant(self):
        result = self.schema.execute("""
        mutation m {
            askQuestion(tableId:"1-10015132-11", questionText: "How many years did Brad play for Toronto") 
            { sql }
        }""")
        print(result.data['askQuestion']['sql'])
        self.assertEqual('SELECT  col4 FROM table WHERE col5 = Brad', result.data['askQuestion']['sql'])

    def test_query(self):
        result = self.schema.execute("""{tables(id:"1-10638523-1"){id, tablename, header, rows }}""")
        #print(result.data['askQuestion']['sql'])
        self.assertEqual('SELECT  col4 FROM table WHERE col5 = Brad', result.data['askQuestion']['sql'])

if __name__ == '__main__':
    unittest.main()
