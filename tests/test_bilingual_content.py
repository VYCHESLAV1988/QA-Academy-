"""Contract checks for authored bilingual material, not external fact verification."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(file,symbol):
    return json.loads((ROOT/'prototype'/file).read_text(encoding='utf-8').split('window.'+symbol+' = ',1)[1].strip().removesuffix(';'))
Q=load('sql-foundations.js','QA_SQL_QUESTIONS')
I=load('interview-language.js','QA_INTERVIEW')
N=load('tutor-feedback.js','QA_TUTOR_NOTES')

class BilingualContentTests(unittest.TestCase):
    def test_all_six_have_translations_and_models(self):
        self.assertEqual(set(I),{q['id'] for q in Q})
        for q in Q:
            with self.subTest(id=q['id']):
                i=I[q['id']]
                self.assertEqual(len(i['choices']),len(q['choices']))
                self.assertEqual(len(i['checkpointChoices']),len(N[q['id']]['checkpoint']['choices']))
                for field in ('question','translation','context','answer','answerRu','checkpoint'):
                    self.assertTrue(i[field].strip())
                self.assertGreater(len(i['answer'].split()),20)
                self.assertEqual(len(i['terms']),4)
    def test_and_answer_preserves_stock_condition(self):
        a=I['sql-and']
        self.assertIn('out of stock',a['choices'][1])
        self.assertIn('both conditions',a['answer'])
        self.assertIn('3',a['checkpoint'])
    def test_checkpoint_select_matches_real_task(self):
        self.assertIn('SELECT price FROM products',I['sql-select']['checkpoint'])
        self.assertEqual(N['sql-select']['checkpoint']['sql'],'SELECT price FROM products;')
    def test_no_developer_footer_in_html(self):
        html=(ROOT/'prototype/lesson.html').read_text(encoding='utf-8').lower()
        for phrase in ('проверяемый прототип','не готовая платформа','нет выдуманной статистики','не официальный экзамен','версия интерфейса'):
            self.assertNotIn(phrase,html)
        self.assertNotIn('<footer',html)
    def test_all_local_assets_exist(self):
        import re
        html=(ROOT/'prototype/lesson.html').read_text()
        refs=re.findall(r'(?:src|href)="([^"#]+\.(?:js|css))"',html)
        self.assertEqual(len(refs),5)
        for ref in refs:self.assertTrue((ROOT/'prototype'/ref).is_file(),ref)

if __name__=='__main__':unittest.main()
