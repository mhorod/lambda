import unittest

from lmd.cooking.tokens import *
from lmd.util.error import *
from lmd.parsing.parse import parse_tokens

from .common import *


class TestParseTopLevel(unittest.TestCase):
    def test_parse_const_value_definition(self):
        tokens = [
            ('const', Keyword(KeywordType.CONST)),
            ('x', Identifier()),
            ('=', Symbol(SymbolType.ASSIGN)),
            ('x', Identifier()),
        ]

        tokens = make_tokens(tokens)

        expected_ast = program_node(
            const_node(
                tokens[0],
                TokenNode(tokens[1]),
                tokens[2],
                ExpressionNode([TokenNode(tokens[3])]),
            )
        )

        report = ErrorReport()
        actual_ast = parse_tokens(tokens, report)
        self.assertEqual(actual_ast, expected_ast)
        self.assertEqual(len(report.errors), 0)

    def test_parse_pub_const_value_definition(self):
        tokens = [
            ('pub', Keyword(KeywordType.PUB)),
            ('const', Keyword(KeywordType.CONST)),
            ('x', Identifier()),
            ('=', Symbol(SymbolType.ASSIGN)),
            ('x', Identifier()),
        ]

        tokens = make_tokens(tokens)

        expected_ast = program_node(
            pub_node(
                tokens[0],
                const_node(
                    tokens[1],
                    TokenNode(tokens[2]),
                    tokens[3],
                    ExpressionNode([TokenNode(tokens[4])]),
                )
            )
        )

        report = ErrorReport()
        actual_ast = parse_tokens(tokens, report)
        self.assertEqual(actual_ast, expected_ast)
        self.assertEqual(len(report.errors), 0)
