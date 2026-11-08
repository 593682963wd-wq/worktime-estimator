import unittest,tempfile,json
from pathlib import Path
from core import run

class Tests(unittest.TestCase):
 def test_half(self):self.assertEqual(run(json.loads(Path('example.json').read_text()))['earned_estimate'],'25.00')
 def test_empty(self):
  with self.assertRaises(KeyError):run({})
 def test_invalid(self):
  p=json.loads(Path('example.json').read_text());p['workdays']=0
  with self.assertRaises(ValueError):run(p)
 def test_before(self):
  p=json.loads(Path('example.json').read_text());p['now']='2026-01-01T08:00:00';self.assertEqual(run(p)['progress'],0)

if __name__=="__main__":unittest.main()
