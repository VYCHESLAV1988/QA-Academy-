"""Browser checks for the isolated lesson prototype, not the full application."""
import functools
import http.server
import os
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
INLINE = os.environ.get('QA_INLINE_HTML') == '1'

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

class LessonBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT / 'prototype')))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}/lesson.html'
        cls.pw = sync_playwright().start()
        executable = os.environ.get('QA_CHROMIUM_PATH')
        options = dict(headless=True)
        if executable:
            options['executable_path'] = executable
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
        self.errors = []
        self.page.on('pageerror', lambda err: self.errors.append(str(err)))
        if INLINE:
            self.page.set_content((ROOT / 'prototype/lesson.html').read_text(encoding='utf-8'), wait_until='load')
        else:
            self.page.goto(self.url)
            self.page.wait_for_load_state('networkidle')

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.context.close()

    def start(self):
        self.page.get_by_role('button', name='К практике', exact=True).click()

    def answer(self, index):
        self.page.get_by_role('radio').nth(index).check()
        self.page.get_by_role('button', name='Проверить ответ', exact=True).click()

    def attempts(self):
        if INLINE:
            return self.page.evaluate('state.attempts')
        return self.page.evaluate("JSON.parse(localStorage.getItem('qa-academy-lesson-v1') || '{}').attempts || []")

    def test_01_initial_screen(self):
        self.assertTrue(self.page.get_by_role('heading', name='Вспомним SQL. Спокойно, шаг за шагом.').is_visible())
        self.assertEqual(self.page.locator('table tbody tr').count(), 4)
        self.assertEqual(self.attempts(), [])

    def test_02_unselected_answer_not_graded(self):
        self.start()
        self.page.get_by_role('button', name='Проверить ответ', exact=True).click()
        self.assertTrue(self.page.locator('#answer-error').is_visible())
        self.assertEqual(self.attempts(), [])

    def test_03_wrong_answer_explained(self):
        self.start()
        self.answer(0)
        self.assertIn('0 / 5', self.page.locator('#feedback').inner_text())
        self.assertIn('только name', self.page.locator('#feedback').inner_text())
        self.assertEqual(len(self.attempts()), 1)

    def test_04_correct_answer_and_duplicate_submit(self):
        self.start()
        self.answer(1)
        self.assertIn('5 / 5', self.page.locator('#feedback').inner_text())
        self.page.locator('#answer-form').evaluate("form => form.dispatchEvent(new Event('submit', {bubbles:true,cancelable:true}))")
        self.assertEqual(len(self.attempts()), 1)

    def test_05_hint_recorded_separately(self):
        self.start()
        self.page.get_by_role('button', name='Нужна подсказка').click()
        self.answer(1)
        self.assertTrue(self.attempts()[0]['assisted'])
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#first-count').inner_text(), '0 / 6')

    @unittest.skipIf(INLINE, 'Inline DOM mode does not verify real origin/localStorage persistence')
    def test_06_persistence_after_reload(self):
        self.start()
        self.answer(1)
        self.page.reload()
        self.page.locator('[data-view="results"]').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(), '1 / 6')

    def test_07_review_only_wrong(self):
        self.start()
        self.answer(0)
        self.page.get_by_role('button', name='Следующее задание').click()
        self.answer(1)
        self.page.locator('[data-view="results"]').click()
        self.page.get_by_role('button', name='Повторить ошибки').click()
        self.assertEqual(self.page.locator('#position').inner_text(), 'Задание 1 из 1')
        self.assertIn('SELECT name', self.page.locator('legend').inner_text())

    def test_08_complete_lesson(self):
        self.start()
        for i, answer in enumerate([1,1,1,1,2,1]):
            self.answer(answer)
            self.page.locator('#next').click()
        self.assertEqual(self.page.locator('#done-count').inner_text(), '6 / 6')
        self.assertEqual(self.page.locator('#first-count').inner_text(), '6 / 6')
        self.page.get_by_role('button', name='Повторить ошибки').click()
        self.assertIn('Ошибок для повторения нет', self.page.locator('#summary').inner_text())

    @unittest.skipIf(INLINE, 'Inline DOM mode does not verify real origin/localStorage persistence')
    def test_09_theme_persists(self):
        self.page.get_by_role('button', name='Тёмная тема').click()
        self.page.reload()
        self.assertTrue(self.page.locator('body.theme-dark').count())
        self.assertTrue(self.page.get_by_role('button', name='Светлая тема').is_visible())

    def test_10_mobile_no_page_overflow(self):
        self.page.set_viewport_size(dict(width=390, height=844))
        for view in ['learn','practice','results']:
            self.page.locator(f'[data-view="{view}"]').click()
            self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), view)

    @unittest.skipIf(INLINE, 'Inline DOM mode does not verify real origin/localStorage persistence')
    def test_11_corrupt_storage_does_not_crash(self):
        self.page.evaluate("localStorage.setItem('qa-academy-lesson-v1', '{broken')")
        self.page.reload()
        self.start()
        self.answer(1)
        self.assertEqual(len(self.attempts()), 1)

    def test_12_reset_requires_confirmation(self):
        self.start()
        self.answer(1)
        self.page.locator('[data-view="results"]').click()
        self.page.once('dialog', lambda d: d.dismiss())
        self.page.get_by_role('button', name='Очистить прогресс').click()
        self.assertEqual(len(self.attempts()), 1)
        self.page.once('dialog', lambda d: d.accept())
        self.page.get_by_role('button', name='Очистить прогресс').click()
        self.assertEqual(self.attempts(), [])

    def test_13_keyboard_radio_and_submit(self):
        self.start()
        radio = self.page.get_by_role('radio').nth(1)
        radio.focus()
        self.page.keyboard.press('Space')
        self.page.get_by_role('button', name='Проверить ответ').focus()
        self.page.keyboard.press('Enter')
        self.assertIn('5 / 5', self.page.locator('#feedback').inner_text())

    def test_14_storage_disabled_has_warning(self):
        if not INLINE:
            self.page.add_init_script("Storage.prototype.setItem = function(){throw new DOMException('Blocked','SecurityError')}")
            self.page.reload()
        self.start()
        self.answer(1)
        self.assertTrue(self.page.locator('#storage-warning').is_visible())

if __name__ == '__main__':
    unittest.main(verbosity=2)
