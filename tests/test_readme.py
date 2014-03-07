import doctest
import os


def test_readme_doctest():
    readme_filename = os.path.join(os.path.dirname(__file__), "..", "README.md")
    with open(readme_filename) as f:
        readme_text = f.read()
        t = doctest.DocTestParser().get_doctest(readme_text, {}, "<readme>", readme_filename, 0)
    result = doctest.DocTestRunner().run(t)
    assert result.failed == 0

