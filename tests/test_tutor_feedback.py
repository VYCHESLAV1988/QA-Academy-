"""Content and executable SQL checks; no learner code is executed."""
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(name, symbol):
    text=(ROOT/'prototype'/name).read_text(encoding='utf-8')
    return json.loads(text.split('window.'+symbol+' = ',1)[1].strip().removesuffix(';'))
Q=load('sql-foundations.js','QA_SQL_QUESTIONS')
NOTES=load('tutor-feedback.js','QA_TUTOR_NOTES')
def execute(rows,sql):
    conn=sqlite3.connect(':memory:')
    try:
        conn.execute('CREATE TABLE products(name TEXT,price INTEGER,stock INTEGER)')
        conn.executemany('INSERT INTO products VALUES(?,?,?)',rows)
        cursor=conn.execute(sql)
        return [d[0] for d in cursor.description],[list(r) for r in cursor.fetchall()]
    finally:
        conn.close()
class TutorFeedbackTests(unittest.TestCase):
    def test_question_source_unchanged(self):
        data=(ROOT/'prototype/sql-foundations.js').read_bytes()
        sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        self.assertEqual(sha,'ad835dcce6d755a1f2a67e5709920f2bd618d870')
    def test_all_options_have_coherent_feedback(self):
        self.assertEqual(set(NOTES),{q['id'] for q in Q})
        for q in Q:
            note=NOTES[q['id']]
            with self.subTest(id=q['id']):
                self.assertEqual(len(note['observations']),len(q['choices']))
                self.assertEqual(len(note['corrections']),len(q['choices']))
                self.assertIsNone(note['corrections'][q['answer']])
                self.assertGreater(len(note['model']),100)
                for i in range(3):
                    if i!=q['answer']:self.assertTrue(note['corrections'][i])
    def test_no_boolean_jargon_in_authored_feedback(self):
        self.assertNotRegex(json.dumps(NOTES,ensure_ascii=False).lower(),r'\b(ложь|ложно|истина|тупой|очевидно)\b')
    def test_six_primary_sql_results(self):
        for q in Q:
            with self.subTest(id=q['id']):
                columns,rows=execute(q['rows'],q['verification']['sql'])
                self.assertEqual(columns,q['verification']['columns'])
                self.assertEqual(rows,q['verification']['rows'])
    def test_six_reinforcement_sql_results(self):
        for key,note in NOTES.items():
            task=note['checkpoint']
            with self.subTest(id=key):
                self.assertEqual(execute(task['rows'],task['sql'])[1],task['expected'])
                self.assertTrue(0<=task['answer']<len(task['choices']))
    def test_and_boundaries(self):
        for price in (2200,2499,2500,2501):
            for stock in (0,1,3):
                with self.subTest(price=price,stock=stock):
                    rows=execute([['Phone',price,stock]],'SELECT name FROM products WHERE price < 2500 AND stock > 0')[1]
                    self.assertEqual(bool(rows),price<2500 and stock>0)
if __name__=='__main__':unittest.main(verbosity=2)
