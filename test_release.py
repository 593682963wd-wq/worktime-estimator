"""作者：Wangyuan；日期：2026-11-08。职责：通过合成输入复验已确认缺陷。"""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
class ReleaseTests(unittest.TestCase):
 def test_decimal_json_precision(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.json';p.write_text('{"monthly_salary":2.00500000000000001,"workdays":1,"work_hours":1,"start":"2026-01-01T00:00:00","now":"2026-01-01T01:00:00"}')
   r=subprocess.run([sys.executable,'-B','cli.py',str(p)],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['daily_estimate'],'2.01')
 def test_invalid_decimal_cli(self) -> None:
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.json';p.write_text('{"monthly_salary":"bad","workdays":1,"work_hours":1}')
   r=subprocess.run([sys.executable,'-B','cli.py',str(p)],capture_output=True,text=True)
   self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
