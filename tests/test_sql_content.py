"""Execute authored expected SQL on the displayed fixtures. Never executes learner input."""
import collections
import json
from pathlib import Path
import sqlite3
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load_content():
    text = (ROOT / 'prototype/sql-foundations.js').read_text(encoding='utf-8')
    return json.loads(text.split('window.QA_SQL_QUESTIONS = ', 1)[1].rstrip().removesuffix(';'))

def execute(sql, rows):
    db = sqlite3.connect(':memory:')
    try:
        db.execute('CREATE TABLE products(name TEXT, price INTEGER, stock INTEGER)')
        db.executemany('INSERT INTO products VALUES (?,?,?)', rows)
        db.execute('PRAGMA query_only=ON')
        cursor = db.execute(sql)
        return [c[0] for c in cursor.description], cursor.fetchall()
    finally:
        db.close()

class ContentTests(unittest.TestCase):
    def test_schema_and_individual_feedback(self):
        questions = load_content()
        self.assertEqual(len(questions), 6)
        self.assertEqual(len({q['id'] for q in questions}), 6)
        for q in questions:
            with self.subTest(q=q['id']):
                self.assertEqual(q['version'], 2)
                self.assertEqual(len(set(q['choices'])), 3)
                self.assertEqual(len(q['why']), 3)
                self.assertEqual(sorted(q['displayOrder']), [0, 1, 2])
                self.assertIn(q['answer'], [0, 1, 2])
                self.assertTrue(all(len(s) > 25 for s in q['why']))
                self.assertEqual(len(q['steps']), 3)
                self.assertTrue(q['source'].startswith('https://www.sqlite.org/'))
        positions = [q['displayOrder'].index(q['answer']) for q in questions]
        self.assertEqual(set(positions), {0, 1, 2})

    def test_every_displayed_expected_result(self):
        for q in load_content():
            with self.subTest(q=q['id']):
                spec = q['verification']
                columns, rows = execute(spec['sql'], q['rows'])
                self.assertEqual(columns, spec['columns'])
                expected = [tuple(row) for row in spec['rows']]
                if 'ORDER BY' in spec['sql']:
                    self.assertEqual(rows, expected)
                else:
                    self.assertEqual(collections.Counter(rows), collections.Counter(expected))

    def test_and_boundary_matrix(self):
        sql = next(q['verification']['sql'] for q in load_content() if q['id'] == 'sql-and')
        for price in [2200, 2499, 2500, 2501]:
            for stock in [0, 1, 3]:
                with self.subTest(price=price, stock=stock):
                    _, rows = execute(sql, [('Тестовый товар', price, stock)])
                    self.assertEqual(bool(rows), price < 2500 and stock > 0)
        self.assertEqual(execute(sql, [('Товар', 2200, 0)])[1], [])

    def test_greater_excludes_equal(self):
        q = next(q for q in load_content() if q['id'] == 'sql-greater')
        for i, choice in enumerate(q['choices']):
            _, result = execute('SELECT price FROM products WHERE ' + choice,
                                [('A', 1999, 1), ('B', 2000, 1), ('C', 2001, 1)])
            self.assertEqual(result == [(2001,)], i == q['answer'])

    def test_and_is_not_a_column_separator(self):
        columns, _ = execute('SELECT name AND price FROM products;', [('A', 2200, 0)])
        self.assertEqual(len(columns), 1)
        self.assertEqual(len(execute('SELECT name,price FROM products;', [('A', 2200, 0)])[0]), 2)

    def test_boundary_equal_is_empty_not_exception(self):
        q = next(q for q in load_content() if q['id'] == 'sql-boundary')
        self.assertEqual(execute(q['verification']['sql'], q['rows'])[1], [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
