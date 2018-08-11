import unittest
import engine

class TestEngine(unittest.TestCase):
  def test_question(self):
    engine.init('/home/stevop/repos/coarse2fine/data_model/wikisql')
    sql = engine.ask_question('1-10015132-11', 'How many years did Brad play for Toronto')
    self.assertEqual('SELECT  col4 FROM table WHERE col5 = Brad', sql)


if __name__ == '__main__':
    unittest.main()