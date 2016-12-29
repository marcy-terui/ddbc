# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch
from contextlib import nested
from nose.tools import raises
import botocore

from ddbc.utils import (
    get_table,
    create_table,
    get_dynamodb_resource
)


class UtilsTestCase(TestCase):

    def test_get_dynamodb_resource(self):
        with patch('boto3.resource'):
            get_dynamodb_resource('us-east-1')
            get_dynamodb_resource(None)

    def test_get_table(self):
        with patch('ddbc.utils.get_dynamodb_resource'):
            get_table('foo', 'us-east-1')

    def test_create_table_exists(self):
        with patch('ddbc.utils.get_table'):
            create_table('foo', 'us-east-1')

    def test_create_table_not_exists(self):
        with nested(
            patch('ddbc.utils.get_table'),
            patch('ddbc.utils.get_dynamodb_resource')
        ) as (p, _):
            p.side_effect = botocore.exceptions.ClientError(
                {'Error': {'Code': 'ResourceNotFoundException'}},
                'create_table')
            create_table('foo', 'us-east-1')

    @raises(botocore.exceptions.ClientError)
    def test_create_table_unexpected_error(self):
        with nested(
            patch('ddbc.utils.get_table'),
            patch('ddbc.utils.get_dynamodb_resource')
        ) as (p, _):
            p.side_effect = botocore.exceptions.ClientError(
                {'Error': {'Code': 'FooException'}},
                'create_table')
            create_table('foo', 'us-east-1')
