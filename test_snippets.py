import logging
log = logging.getLogger(__name__)
log.setLevel('DEBUG')
log.addHandler(logging.FileHandler('test_qute-snippets.log'))

import json
import subprocess
import os
from unittest import TestCase, skip

from snippets import get_text, set_text, qute_paste_text, qute_show_message


class SnippetsTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir('testdir')

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir('testdir')


# @skip
class SetTextTest(SnippetsTestCase):

    def setUp(self) -> None:
        self.register_file = 'testdir/snippets.json'

        self.fifo = 'testdir/QUTE_FIFO'
        os.environ['QUTE_FIFO'] = self.fifo

    def tearDown(self) -> None:
        if os.path.isfile(self.register_file):
            os.remove(self.register_file)

        if os.path.isfile(self.fifo):
            os.remove(self.fifo)

    def test_set_text(self):
        log.debug('\n** test_set_text')
        key = '1'
        text = 'Test text'

        set_text(key, text)

        self.assertTrue(os.path.isfile(self.register_file))

        with open(self.register_file) as file:
            saved = json.load(file)

        self.assertIn(key, saved.keys())
        self.assertEqual(text, saved[key])

    def test_set_various_texts(self):
        log.debug('\n** test_set_various_texts')
        entrada = {
            '1': 'Test text',
            '2': 'Other test text'
        }

        for e in entrada:
            set_text(e, entrada[e])

        self.assertTrue(os.path.isfile(self.register_file))

        with open(self.register_file) as file:
            saved = json.load(file)

        self.assertEqual(entrada, saved)

    def test_set_with_missing_text(self):
        log.debug('\n** test_set_with_missing_text')
        self.assertRaises(TypeError, set_text, 'Only one arg')

    def test_show_message_on_set_text(self):
        log.debug('\n** test_show_message_on_set_text')
        key = '1'

        set_text(key, 'Test text')

        self.assertTrue(os.path.isfile(self.fifo))

        with open(self.fifo) as file:
            passed = file.read()

        self.assertEqual('message-info "Text saved on key {}"\n'.format(key), passed)

        self.assertTrue(os.path.isfile(self.register_file))


# @skip
class GetTextTest(SnippetsTestCase):

    def setUp(self) -> None:
        self.register_file = 'testdir/snippets.json'

    def tearDown(self) -> None:
        if os.path.isfile(self.register_file):
            os.remove(self.register_file)

    def test_get_text_key_exists(self):
        log.debug('\n** test_get_text_key_exists')
        key = '1'
        text = 'Test text'

        with open(self.register_file, 'w') as file:
            json.dump({key: text}, file)

        result = get_text(key)

        self.assertEqual(text, result)

    def test_get_text_file_doesnt_exist(self):
        log.debug('\n** test_get_text_file_doesnt_exist')
        key = '1'

        self.assertRaises(FileNotFoundError, get_text, key)

    def test_get_text_key_doesnt_exist(self):
        log.debug('\n** test_get_text_key_doesnt_exist')
        with open(self.register_file, 'w') as file:
            json.dump({'1': 'Test text'}, file)

        key = 'Nonexistent key'

        self.assertRaises(KeyError, get_text, key)

    def test_get_text_other_existing_key(self):
        log.debug('\n** test_get_text_other_existing_key')
        entrada = {
            '1': 'Test text',
            '2': 'Other test text'
        }

        with open(self.register_file, 'w') as file:
            json.dump(entrada, file)

        result = get_text('2')

        self.assertEqual(entrada['2'], result)


# @skip
class QuteShowMessageTest(SnippetsTestCase):

    def setUp(self) -> None:
        self.fifo = 'testdir/QUTE_FIFO'
        os.environ['QUTE_FIFO'] = self.fifo

    def tearDown(self) -> None:
        if os.path.isfile(self.fifo):
            os.remove(self.fifo)

    def test_qute_show_message(self):
        log.debug('\n** test_qute_show_message')
        text = 'Test message'

        qute_show_message(text)

        self.assertTrue(os.path.isfile(self.fifo))

        with open(self.fifo) as file:
            passed = file.read()

        self.assertEqual('message-info "{}"\n'.format(text), passed)


# @skip
class QutePasteTextTest(SnippetsTestCase):

    def setUp(self) -> None:
        self.fifo = 'testdir/QUTE_FIFO'
        os.environ['QUTE_FIFO'] = self.fifo

    def tearDown(self) -> None:
        if os.path.isfile(self.fifo):
            os.remove(self.fifo)

    def test_qute_paste_text(self):
        log.debug('\n** test_qute_paste_text')
        text = 'Test text'

        qute_paste_text(text)

        self.assertTrue(os.path.isfile(self.fifo))

        with open(self.fifo) as file:
            passed = file.read()

        self.assertEqual('insert-text {}\n'.format(text), passed)


# @skip
class InterfaceTest(SnippetsTestCase):

    def setUp(self) -> None:
        self.register_file = 'testdir/snippets.json'
        self.fifo = 'testdir/QUTE_FIFO'
        os.environ['QUTE_FIFO'] = self.fifo
        os.environ['QUTE_CONFIG_DIR'] = 'testdir'

    def tearDown(self) -> None:
        if os.path.isfile(self.fifo):
            os.remove(self.fifo)

        if os.path.isfile(self.register_file):
            os.remove(self.register_file)

    def test_arguments_set_text(self):
        log.debug('\n** test_arguments_set_text')
        key = '1'
        text = 'Test text'

        result = subprocess.run(['python3', 'snippets.py', '--set', key, text])

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.isfile(self.register_file))

        with open(self.register_file) as file:
            saved = json.load(file)

        self.assertIn(key, saved.keys())
        self.assertEqual(text, saved[key])

    def test_arguments_set_implicit(self):
        log.debug('\n** test_arguments_set_implicit')
        key = '1'
        text = 'Test text'

        result = subprocess.run(['python3', 'snippets.py', key, text])

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.isfile(self.register_file))

        with open(self.register_file) as file:
            saved = json.load(file)

        self.assertIn(key, saved.keys())
        self.assertEqual(text, saved[key])

    def test_arguments_get_text(self):
        log.debug('\n** test_arguments_get_text')
        key = '1'
        text = 'Test text'
        with open(self.register_file, 'w') as file:
            json.dump({key: text}, file)

        result = subprocess.run(['python3', 'snippets.py', '--get', key])

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.isfile(self.fifo))

        with open(self.fifo) as file:
            passed = file.read()

        self.assertEqual('insert-text {}\n'.format(text), passed)

    def test_arguments_get_implicit(self):
        log.debug('\n** test_arguments_get_implicit')
        key = '1'
        text = 'Test text'
        with open(self.register_file, 'w') as file:
            json.dump({key: text}, file)

        result = subprocess.run(['python3', 'snippets.py', key])

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.isfile(self.fifo))

        with open(self.fifo) as file:
            passed = file.read()

        self.assertEqual('insert-text {}\n'.format(text), passed)

    # @skip
    def test_arguments_wrong_usage(self):
        log.debug('\n** test_arguments_wrong_usage')

        with open(self.register_file, 'w') as file:
            json.dump({'1': 'Test text'}, file)

        with open('help_output') as helpfile:
            help_output = helpfile.read()

        wrong_input = ['python3', 'snippets.py', 'key', 'text', 'wrong']

        result = subprocess.run(wrong_input, text=True, capture_output=True)

        self.assertNotEqual('0', result.returncode)
        self.assertEqual(help_output, result.stdout)
