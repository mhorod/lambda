import unittest
from lang.result import *

class TestParsingResult(unittest.TestCase):
    def test_ok_is_ok(self):
        result = Ok(1, [])
        self.assertEqual(result.is_ok(), True)

    def test_ok_is_not_err(self):
        result = Ok(1, [])
        self.assertEqual(result.is_err(), False)

    def test_fatal_err_is_not_ok(self):
        result = Err(1, [], True)
        self.assertEqual(result.is_ok(), False)

    def test_fatal_err_is_err(self):
        result = Err(1, [], True)
        self.assertEqual(result.is_err(), True)

    def test_non_fatal_err_is_ok(self):
        result = Err(1, [], False)
        self.assertEqual(result.is_ok(), True)

    def test_non_fatal_err_is_not_err(self):
        result = Err(1, [], False)
        self.assertEqual(result.is_err(), False)
    
    def test_and_then_on_fatal_error_does_not_append_tokens(self):
        result = Err(1, [], True)
        result = result.and_then(lambda x: Ok(x, [1]))
        self.assertEqual(result.is_err(), True)
        self.assertEqual(result.tokens, [])

    def test_and_then_on_ok_appends_tokens(self):
        result = Ok(1, [])
        result = result.and_then(lambda x: Ok(x, [1]))
        self.assertEqual(result.is_err(), False)
        self.assertEqual(result.tokens, [1])


if __name__ == '__main__':
    print("Testing ParsingResult")
    unittest.main()