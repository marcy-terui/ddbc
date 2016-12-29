# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import Mock, patch
from nose.tools import eq_, raises
import botocore

from ddbc.cache import Client


class ClientTestCase(TestCase):

    def test__getitem__(self):
        client = Client(table_name='foo')
        client.get = Mock(return_value='bar')
        eq_(client['buz'], 'bar')

    def test_get_from_cache(self):
        client = Client(table_name='foo')
        client._is_available_item = Mock(return_value=True)
        client.cache = {'foo': {'data': 'bar', 'until': -1}}
        eq_(client.get('foo'), 'bar')

    def test_get_from_cache_unavailable(self):
        client = Client(table_name='foo')
        client._is_available_item = Mock(return_value=False)
        client.cache = {'foo': {'data': 'bar', 'until': -1}}
        eq_(client.get('foo', 'buz'), 'buz')

    def test_get_from_table(self):
        client = Client(table_name='foo')
        client._is_available_item = Mock(return_value=True)
        client.read_table_item = Mock(
            return_value={'data': 'qux', 'until': -1})
        eq_(client.get('foo'), 'qux')

    @raises(botocore.exceptions.ClientError)
    def test_get_error(self):
        client = Client(table_name='foo')
        client.report_error = True
        client._is_available_item = Mock(return_value=True)
        client.read_table_item = Mock(
            side_effect=botocore.exceptions.ClientError(
                {'Error': {'Code': 'ResourceNotFoundException'}}, 'get_item'))
        client.get('foo')

    def test__setitem__(self):
        client = Client(table_name='foo')
        client.set = Mock(return_value=True)
        client['bar'] = 'buz'

    def test_set(self):
        client = Client(table_name='foo')
        client.put_table_item = Mock()
        eq_(client.set('bar', 'buz'), True)

    def test_set_error(self):
        client = Client(table_name='foo')
        client.put_table_item = Mock(
            side_effect=botocore.exceptions.ClientError(
                {'Error': {'Code': 'ResourceNotFoundException'}}, 'put_item'))
        eq_(client.set('bar', 'buz'), False)

    @raises(botocore.exceptions.ClientError)
    def test_set_report_error(self):
        client = Client(table_name='foo')
        client.report_error = True
        client.put_table_item = Mock(
            side_effect=botocore.exceptions.ClientError(
                {'Error': {'Code': 'ResourceNotFoundException'}}, 'put_item'))
        client.set('bar', 'buz')

    def test__delitem__(self):
        client = Client(table_name='foo')
        client.delete = Mock()
        del client['bar']

    def test_delete(self):
        client = Client(table_name='foo')
        client.delete_table_item = Mock()
        client.cache['bar'] = 'buz'
        eq_(client.delete('bar'), True)

    def test_delete_not_exist(self):
        client = Client(table_name='foo')
        client.delete_table_item = Mock()
        eq_(client.delete('bar'), True)

    def test_delete_error(self):
        client = Client(table_name='foo')
        client.delete_table_item = Mock(
            side_effect=botocore.exceptions.ClientError(
                {'Error': {'Code': 'ResourceNotFoundException'}},
                'delete_item'))
        client.cache['bar'] = 'buz'
        eq_(client.delete('bar'), False)

    @raises(botocore.exceptions.ClientError)
    def test_delete_report_error(self):
        client = Client(table_name='foo')
        client.report_error = True
        client.delete_table_item = Mock(
            side_effect=botocore.exceptions.ClientError(
                {'Error': {'Code': 'ResourceNotFoundException'}},
                'delete_item'))
        client.cache['bar'] = 'buz'
        client.delete('bar')

    def test_get_until_time_default(self):
        client = Client(table_name='foo')
        eq_(client._get_until_time(), -1)

    def test_get_until_time_custum(self):
        with patch('time.time') as p:
            p.return_value = 100.1
            client = Client(table_name='foo')
            eq_(client._get_until_time(100), 200)

    def test_is_available_item(self):
        with patch('time.time') as p:
            p.return_value = 102.0
            client = Client(table_name='foo')
            eq_(client._is_available_item({}), True)
            eq_(client._is_available_item({'until': 101}), False)

    def test_generate_hash_key(self):
        with patch('hashlib.sha1') as p:
            m = Mock()
            m.hexdigest = Mock(return_value='foo')
            p.return_value = m
            client = Client(table_name='foo')
            eq_(client._generate_hash_key('bar'), 'foo')

    def test_read_table_item(self):
        client = Client(table_name='foo')
        m = Mock()
        m.get_item = Mock(
            return_value={'Item': client._serialize({'data': 'bar'})})
        client.table = m
        eq_(client.read_table_item('buz'), {'data': 'bar'})

    def test_put_table_item(self):
        client = Client(table_name='foo')
        client.table = Mock()
        client.put_table_item('bar', {'data': 'buz'})

    def test_delete_table_item(self):
        client = Client(table_name='foo')
        client.table = Mock()
        client.delete_table_item('bar')

    def test_serialize(self):
        client = Client(table_name='foo')
        eq_(
            client._deserialize(client._serialize({'data': 'bar', 'until': 1.0})),
            {'data': 'bar', 'until': 1}
        )
