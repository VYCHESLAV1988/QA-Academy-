"""Real browser checks; inline mode explicitly excludes persistence tests."""
import functools
import http.server
import os
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
INLINE = os.getenv('QA_INLINE_HTML') == '1'

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

class LessonBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'prototype')))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)
        cls.pw = sync_playwright().start()
        cls.addClassCleanup(cls.pw.stop)
        opts = dict(headless=True)
        if os.getenv('QA_CHROMIUM_PATH'):
            opts['executable_path'] = os.environ['QA_CHROMIUM_PATH']
        cls.browser = cls.pw.chromium.launch(**opts)
        cls.addClassCleanup(cls.browser.close)
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/lesson.html'

    def setUp(self):
        self.context = self.browser.new_context(viewport=dict(width=1440, height=1000))
        self.addCleanup(self.context.close)
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda err: self.errors.append(str(err)))
        if INLINE:
            html = (ROOT/'prototype/lesson.html').read_text(encoding='utf-8')
            html = html.replace('<link rel="stylesheet" href="lesson.css">', '<style>'+(ROOT/'prototype/lesson.css').read_text(encoding='utf-8')+'</style>')
            for asset in ('sql-foundations.js','tutor-feedback.js','interview-language.js','lesson.js'):
                html = html.replace(f'<script src="{asset}"></script>', '<script>'+(ROOT/'prototype'/asset).read_text(encoding='utf-8')+'</script>')
            self.page.set_content(html, wait_until='load')
        else:
            self.page.goto(self.url, wait_until='networkidle')
        self.page.set_default_timeout(3000)

    def tearDown(self):
        self.assertEqual(self.errors, [])

    def show(self, index):
        self.page.evaluate('(index) => {state.queue=questions.map(q=>q.id);state.index=index;route("practice");}', index)

    def answer(self, value):
        self.page.locator(f'#answers input[value="{value}"]').check()
        self.page.get_by_role('button', name='Проверить ответ', exact=True).click()

    def attempts(self):
        return self.page.evaluate('state.attempts')

    def test_initial_and_version(self):
        self.assertEqual(self.page.locator('html').get_attribute('data-ui-version'),'4')
        self.assertFalse(self.page.locator('#load-error').is_visible())
        self.assertEqual(self.page.locator('#intro-table tbody tr').count(),4)
        self.assertEqual(self.attempts(),[])

    def test_empty_submission_not_graded(self):
        self.show(0)
        self.page.locator('#check').click()
        self.assertTrue(self.page.locator('#answer-error').is_visible())
        self.assertEqual(self.attempts(),[])

    def test_all_18_options_have_authored_feedback_and_honest_score(self):
        for index, correct in enumerate([1,1,1,1,2,1]):
            for chosen in range(3):
                with self.subTest(question=index, chosen=chosen):
                    self.show(index)
                    self.answer(chosen)
                    feedback=self.page.locator('#feedback').inner_text()
                    self.assertIn('Правильный ответ простыми словами',feedback)
                    self.assertIn(f'За выбор ответа: {5 if chosen==correct else 0} / 5',feedback)
                    self.assertIn('Главное, что стоит запомнить',feedback)
                    self.assertIn('Sample answer',feedback)
                    self.assertTrue(self.page.locator('#interview-answer .english').is_visible())
                    self.assertNotRegex(feedback.lower(),r'\b(ложь|ложно|истина|тупой|очевидно)\b')
                    self.assertEqual(self.page.locator('#answers .correct').count(),1)
                    if chosen!=correct:
                        self.assertIn('Что нужно исправить',feedback)

    def test_and_explains_price_and_stock_without_boolean_jargon(self):
        self.show(3); self.answer(0)
        text=self.page.locator('#feedback').inner_text()
        for phrase in ['В выбранном варианте правильно указано сравнение цены','товар закончился','хотя бы одна единица','Нет, этот товар не попадёт']:
            self.assertIn(phrase,text)
        self.assertEqual(self.page.locator('#feedback h2').inner_text(),'Разбор твоего ответа')

    def test_duplicate_submit_not_saved(self):
        self.show(0); self.answer(1)
        self.page.locator('#answer-form').evaluate("f=>f.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}))")
        self.assertEqual(len(self.attempts()),1)

    def test_hints_are_assisted(self):
        self.show(0); self.page.locator('#hint').click(); self.answer(1)
        self.assertTrue(self.attempts()[0]['assisted'])
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#first-count').inner_text(),'0 / 6')

    def test_reinforcement_has_no_effect_on_score_or_history(self):
        self.show(3); self.answer(0)
        before=self.attempts()
        self.page.get_by_role('button',name='Проверить закрепление',exact=True).click()
        self.assertIn('Выбери вариант',self.page.locator('#reinforcement-result').inner_text())
        self.page.locator('#reinforcement input[value="0"]').check()
        self.page.get_by_role('button',name='Проверить закрепление',exact=True).click()
        self.assertIn('Разберём этот пример',self.page.locator('#reinforcement-result').inner_text())
        self.page.locator('#reinforcement input[value="1"]').check()
        self.page.get_by_role('button',name='Проверить ещё раз',exact=True).click()
        self.assertIn('Верно.',self.page.locator('#reinforcement-result').inner_text())
        self.assertEqual(self.attempts(),before)

    def test_all_six_reinforcements(self):
        for index, value in enumerate([0,1,0,1,2,0]):
            self.show(index); self.answer(1 if index!=4 else 2)
            self.page.locator(f'#reinforcement input[value="{value}"]').check()
            self.page.get_by_role('button',name='Проверить закрепление',exact=True).click()
            self.assertTrue(self.page.locator('#reinforcement-result').inner_text().startswith('Верно.'))
        self.assertEqual(len(self.attempts()),6)

    def test_review_only_wrong(self):
        self.show(0); self.answer(0)
        self.page.locator('#next').click(); self.answer(1)
        self.page.locator('[data-view="results"]').click()
        self.page.locator('#review').click()
        self.assertEqual(self.page.locator('#position').inner_text(),'Задание 1 из 1')
        self.assertEqual(self.page.evaluate('current().id'),'sql-select')

    def test_complete_lesson(self):
        self.page.locator('#start').click()
        for answer in [1,1,1,1,2,1]:
            self.answer(answer); self.page.locator('#next').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(),'6 / 6')
        self.assertEqual(self.page.locator('#first-count').inner_text(),'6 / 6')

    def test_mobile_all_questions_and_feedback(self):
        for width in (390,320,768):
            self.page.set_viewport_size(dict(width=width,height=844))
            for index in range(6):
                self.show(index); self.answer(0)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,index))

    def test_keyboard(self):
        self.show(0)
        self.page.locator('#answers input[value="1"]').focus(); self.page.keyboard.press('Space')
        self.page.locator('#check').focus(); self.page.keyboard.press('Enter')
        self.assertIn('5 / 5',self.page.locator('#feedback .points').inner_text())

    def test_back_to_explanation(self):
        self.show(3); self.answer(0); self.page.locator('#back-explanation').click()
        self.assertTrue(self.page.locator('#learn').is_visible())

    def test_reset_confirmed(self):
        self.show(0); self.answer(1); self.page.locator('[data-view="results"]').click()
        self.page.get_by_text('Управление прогрессом',exact=True).click()
        self.page.once('dialog',lambda d:d.dismiss()); self.page.locator('#reset').click()
        self.assertEqual(len(self.attempts()),1)
        self.page.once('dialog',lambda d:d.accept()); self.page.locator('#reset').click()
        self.assertEqual(self.attempts(),[])

    @unittest.skipIf(INLINE,'Inline mode cannot establish persistence on a real browser origin')
    def test_reload_persistence(self):
        self.show(3); self.answer(0); saved=self.attempts(); self.page.reload()
        self.assertEqual(self.attempts(),saved)
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(),'1 / 6')

    @unittest.skipIf(INLINE,'Inline mode cannot establish persistence on a real browser origin')
    def test_existing_v2_history_preserved(self):
        saved=dict(version=1,attempts=[dict(id='sql-and',selected=0,assisted=False,contentVersion=2,at='2026-10-15T00:00:00Z')],queue=['sql-and'],index=0,theme='light')
        self.page.evaluate('(s)=>localStorage.setItem("qa-academy-lesson-v1",JSON.stringify(s))',saved)
        self.page.reload(); self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(),'1 / 6')
        self.assertEqual(self.attempts(),saved['attempts'])
        self.assertFalse(self.page.locator('#content-notice').is_visible())

    @unittest.skipIf(INLINE,'Inline mode cannot establish persistence on a real browser origin')
    def test_theme_persistence(self):
        self.page.locator('#theme').click(); self.page.reload()
        self.assertEqual(self.page.locator('body.theme-dark').count(),1)

    @unittest.skipIf(INLINE,'Inline mode cannot establish persistence on a real browser origin')
    def test_corrupted_storage(self):
        self.page.evaluate('localStorage.setItem("qa-academy-lesson-v1","{broken")')
        self.page.reload(); self.show(0); self.answer(1)
        self.assertEqual(len(self.attempts()),1)

    def test_disabled_storage_warning(self):
        if not INLINE:
            self.page.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('Blocked','SecurityError')}")
            self.page.reload()
        self.show(0); self.answer(1)
        self.assertTrue(self.page.locator('#storage-warning').is_visible())


    def test_bilingual_prompt_and_model_after_submit(self):
        self.show(3)
        self.assertIn('result set',self.page.locator('#question-title').inner_text())
        self.assertTrue(self.page.locator('#question-translation').is_visible())
        self.assertEqual(self.page.locator('#interview-answer').count(),0)
        self.answer(0)
        self.assertIn('both conditions',self.page.locator('#interview-answer .english').inner_text())
        self.assertIn('товар отсутствует',self.page.locator('#interview-answer .translation').inner_text())

    def test_translation_toggle_keeps_answer_and_no_extra_attempt(self):
        self.show(3)
        self.page.locator('#answers input[value="0"]').check()
        self.page.locator('#translations').uncheck()
        self.assertFalse(self.page.locator('#question-translation').is_visible())
        self.assertTrue(self.page.locator('#answers input[value="0"]').is_checked())
        self.page.locator('#check').click()
        self.assertEqual(len(self.attempts()),1)
        self.assertFalse(self.attempts()[0]['translationShown'])
        self.page.locator('#translations').check()
        self.assertTrue(self.page.locator('#interview-answer .translation').is_visible())
        self.assertEqual(len(self.attempts()),1)
        self.assertTrue(self.page.locator('#check').is_disabled())

    def test_no_technical_footer(self):
        self.assertEqual(self.page.locator('footer').count(),0)
        for view in ('learn','practice','results'):
            self.page.locator(f'[data-view="{view}"]').click()
            self.assertNotRegex(self.page.locator('body').inner_text().lower(),r'проверяемый прототип|не готовая платформа|выдуманной статистики|официальный экзамен')

    @unittest.skipIf(INLINE, 'Needs a real origin to verify saved language preference')
    def test_translation_preference_persists(self):
        self.show(1)
        self.page.locator('#translations').uncheck()
        self.page.reload()
        self.assertFalse(self.page.locator('#translations').is_checked())
        self.assertFalse(self.page.locator('#question-translation').is_visible())

if __name__=="__main__":unittest.main(verbosity=2)
