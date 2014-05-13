"""
Test the autocomplete mode
"""
from PyQt4.QtTest import QTest
from pyqode.core import frontend
from pyqode.python.frontend import modes as pymodes
from ...helpers import editor_open


def get_mode(editor):
    return frontend.get_mode(editor, pymodes.PyAutoCompleteMode)


def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


@editor_open(__file__)
def test_basic(editor):
    QTest.keyPress(editor, '(')
    editor.clear()
    QTest.keyPress(editor, '(')


def test_autocomple_func_parens(editor):
    editor.clear()
    editor.setPlainText('def foo', 'text/x-python', 'utf-8')
    frontend.goto_line(editor, 1, len('def foo'))
    QTest.keyPress(editor, '(')
    assert editor.toPlainText() == 'def foo():'


def test_autocomple_method_parens(editor):
    editor.clear()
    editor.setPlainText('class\n    def foo', 'text/x-python', 'utf-8')
    frontend.goto_line(editor, 2, len('    def foo'))
    QTest.keyPress(editor, '(')
    assert editor.toPlainText() == 'class\n    def foo(self):'


def test_class_docstrings(editor):
    editor.clear()
    editor.setPlainText('class Foo:\n    ', 'text/x-python', 'utf-8')
    frontend.goto_line(editor, 2, len('    '))
    QTest.keyPress(editor, '"')
    QTest.keyPress(editor, '"')
    assert editor.toPlainText() == 'class Foo:\n    """\n    \n    """'


def test_fct_docstrings(editor):
    editor.clear()
    editor.setPlainText('def foo(bar, spam, eggs):\n    ',
                        'text/x-python', 'utf-8')
    frontend.goto_line(editor, 2, len('    '))
    QTest.keyPress(editor, '"')
    QTest.keyPress(editor, '"')
    assert editor.toPlainText() == 'def foo(bar, spam, eggs):\n    """\n    \n    :param bar:\n    :param spam:\n    :param eggs:\n    """'
