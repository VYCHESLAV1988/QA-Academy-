"""UI regression. INLINE is a documented DOM-only fallback, not a persistence test."""
import functools
import http.server
import os
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
INLINE = os.environ.get('QA_INLINE_HTML') == '1'
KEY = 'qa-academy-lesson-v1'

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

class LessonBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'prototype')))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/lesson.html'
        cls.pw = sync_playwright().start()
        options = dict(headless=True)
        if os.environ.get('QA_CHROMIUM_PATH'):
            options['executable_path'] = os.environ['QA_CHROMIUM_PATH']
        cls.browser = cls.pw.chromium.launch(**options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context = self.browser.new_context(viewport=dict(width=1440, height=1000))
        self.page = self.context.new_page()
        self.page.set_default_timeout(4000)
        self.errors = []
        self.page.on('pageerror', lambda e: self.errors.append(str(e)))
        if INLINE:
            html = (ROOT/'prototype/lesson.html').read_text(encoding='utf-8')
            script = (ROOT/'prototype/sql-foundations.js').read_text(encoding='utf-8')
            html = html.replace('<script src="sql-foundations.js"></script>', '<script>'+script+'</script>')
            self.page.set_content(html, wait_until='load')
        else:
            self.page.goto(self.url, wait_until='networkidle', timeout=6000)

    def tearDown(self):
        try:
            self.assertEqual(self.errors, [])
        finally:
            self.context.close()

    def start(self):
        self.page.get_by_role('button', name='К практике', exact=True).click()

    def answer(self, index):
        # Content identity, not display position: correct options are not always second.
        self.page.locator(f'input[name="answer"][value="{index}"]').check()
        self.page.get_by_role('button', name='Проверить ответ', exact=True).click()

    def attempts(self):
        return self.page.evaluate('state.attempts')

    def test_01_initial_explanation(self):
        self.assertTrue(self.page.get_by_role('heading', name='Вспомним SQL. Спокойно, шаг за шагом.').is_visible())
        self.assertEqual(self.page.locator('#intro-table tbody tr').count(), 4)
        self.assertIn('ORDER BY', self.page.locator('#learn').inner_text())
        self.assertEqual(self.attempts(), [])

    def test_02_empty_not_graded(self):
        self.start()
        self.page.locator('#check').click()
        self.assertTrue(self.page.locator('#answer-error').is_visible())
        self.assertEqual(self.attempts(), [])

    def test_03_wrong_has_selected_and_correct_answer(self):
        self.start()
        self.answer(0)
        text = self.page.locator('#feedback').inner_text()
        for expected in ['0 / 5', 'Твой ответ:', 'Правильный ответ:', 'Разберём по шагам']:
            self.assertIn(expected, text)
        self.assertEqual(self.page.locator('#feedback ol li').count(), 3)
        self.assertEqual(self.page.locator('label.correct').count(), 1)
        self.assertEqual(self.page.locator('label.wrong').count(), 1)

    def test_04_correct_and_duplicate_submit(self):
        self.start()
        self.answer(1)
        self.assertIn('5 / 5', self.page.locator('#feedback').inner_text())
        self.page.locator('#answer-form').evaluate("f => f.dispatchEvent(new Event('submit', {bubbles:true,cancelable:true}))")
        self.assertEqual(len(self.attempts()), 1)

    def test_05_hint_not_independent(self):
        self.start()
        self.page.locator('#hint').click()
        self.answer(1)
        self.assertTrue(self.attempts()[0]['assisted'])
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#first-count').inner_text(), '0 / 6')

    @unittest.skipIf(INLINE, 'DOM-only: real origin and reload required')
    def test_06_persistence(self):
        self.start()
        self.answer(1)
        self.page.reload()
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(), '1 / 6')

    def test_07_review_only_errors(self):
        self.start()
        self.answer(0)
        self.page.locator('#next').click()
        self.answer(1)
        self.page.locator('[data-view="results"]').click()
        self.page.locator('#review').click()
        self.assertEqual(self.page.locator('#position').inner_text(), 'Задание 1 из 1')
        self.assertEqual(self.page.evaluate('current().id'), 'sql-select')

    def test_08_complete_six(self):
        self.start()
        for answer in [1,1,1,1,2,1]:
            self.answer(answer)
            self.page.locator('#next').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(), '6 / 6')
        self.assertEqual(self.page.locator('#first-count').inner_text(), '6 / 6')
        self.page.locator('#review').click()
        self.assertIn('Ошибок для повторения нет', self.page.locator('#summary').inner_text())

    @unittest.skipIf(INLINE, 'DOM-only: real origin and reload required')
    def test_09_theme_persists(self):
        self.page.locator('#theme').click()
        self.page.reload()
        self.assertTrue(self.page.locator('body.theme-dark').count())

    def test_10_mobile_long_content(self):
        self.page.set_viewport_size(dict(width=390,height=844))
        self.start()
        for i in range(6):
            self.answer(0)
            self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
            self.page.locator('#next').click()

    @unittest.skipIf(INLINE, 'DOM-only: real origin and reload required')
    def test_11_corrupt_storage(self):
        self.page.evaluate('(k) => localStorage.setItem(k,"{broken")', KEY)
        self.page.reload()
        self.start()
        self.answer(1)
        self.assertEqual(len(self.attempts()), 1)

    def test_12_confirm_reset(self):
        self.start()
        self.answer(1)
        self.page.locator('[data-view="results"]').click()
        self.page.once('dialog', lambda d:d.dismiss())
        self.page.locator('#reset').click()
        self.assertEqual(len(self.attempts()), 1)
        self.page.once('dialog', lambda d:d.accept())
        self.page.locator('#reset').click()
        self.assertEqual(self.attempts(), [])

    def test_13_keyboard(self):
        self.start()
        self.page.locator('input[value="1"]').focus()
        self.page.keyboard.press('Space')
        self.page.locator('#check').focus()
        self.page.keyboard.press('Enter')
        self.assertIn('5 / 5', self.page.locator('#feedback').inner_text())

    def test_14_unavailable_storage_warning(self):
        if not INLINE:
            self.page.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('Blocked','SecurityError')}")
            self.page.reload()
        self.start()
        self.answer(1)
        self.assertTrue(self.page.locator('#storage-warning').is_visible())

    def test_15_reported_and_case(self):
        self.start()
        for answer in [1,1,1]:
            self.answer(answer)
            self.page.locator('#next').click()
        self.assertIn('остаток 0 штук', self.page.locator('#context').inner_text())
        self.assertIn('AND stock > 0', self.page.locator('#query').inner_text())
        self.assertEqual(self.page.locator('#task-table tbody tr').count(), 1)
        self.answer(0)
        text = self.page.locator('#feedback').inner_text()
        self.assertIn('пропустил наличие', text)
        self.assertIn('Правильный ответ: Нет: товар отсутствует на складе.', text)
        self.assertIn('На складе больше нуля единиц? Нет', text)
        self.page.get_by_text('Посмотреть ожидаемый результат SQL', exact=True).click()
        self.assertIn('Нет строк', self.page.locator('#feedback').inner_text())
        screenshot = os.environ.get('QA_SCREENSHOT')
        if screenshot:
            self.page.screenshot(path=screenshot, full_page=True)

    def test_16_each_option_gets_own_feedback(self):
        self.start()
        self.answer(2)
        self.assertIn('Условия stock > 0 в запросе нет', self.page.locator('#feedback').inner_text())

    @unittest.skipIf(INLINE, 'DOM-only: real saved-state migration requires origin')
    def test_17_old_history_retained_not_regraded(self):
        old = dict(version=1, attempts=[dict(id='sql-and',selected=0,assisted=False,at='2026-10-15T00:00:00Z')],theme='light')
        self.page.evaluate('([k,v])=>localStorage.setItem(k,JSON.stringify(v))',[KEY,old])
        self.page.reload()
        self.assertEqual(len(self.attempts()), 1)
        self.assertTrue(self.page.locator('#content-notice').is_visible())
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(), '0 / 6')

if __name__ == '__main__':
    unittest.main(verbosity=2)
