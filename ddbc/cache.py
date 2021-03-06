# -*- coding: utf-8 -*-

import botocore
import time
import hashlib
import pickle
from ddbc.utils import get_table


class Client(object):

    cache = {}

    def __init__(
        self,
        table_name,
        region=None,
        default_ttl=-1,
        report_error=False
    ):
        self.table = get_table(table_name, region)
        self.default_ttl = default_ttl
        self.report_error = report_error

    def __contains__(self, key):
        return self.get(key) is not None

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=None):
        item = self.cache.get(key, {})

        if not self._is_available_item(item):
            item = {}

        if item == {}:
            try:
                item = self.read_table_item(key)
            except botocore.exceptions.ClientError:
                if self.report_error:
                    raise

        if not self._is_available_item(item):
            item = {}

        self.cache[key] = item
        return item.get('data', default)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def set(self, key, value, ttl=None):
        item = {
            'data': value,
            'until': self._get_until_time(ttl)
        }

        try:
            self.put_table_item(key, item)
        except botocore.exceptions.ClientError:
            if self.report_error:
                raise
            else:
                return False

        self.cache[key] = item
        return True

    def __delitem__(self, key):
        return self.delete(key)

    def delete(self, key):
        try:
            self.delete_table_item(key)
            del self.cache[key]
        except KeyError:
            pass
        except botocore.exceptions.ClientError:
            if self.report_error:
                raise
            else:
                return False

        return True

    def _get_until_time(self, ttl=None):
        if ttl is None:
            ttl = self.default_ttl

        if not ttl == -1:
            ttl = int(time.time()) + ttl

        return ttl

    def _is_available_item(self, item):
        now = int(time.time())
        until = item.get('until', -1)
        return (until == -1 or now <= until)

    def _generate_hash_key(self, key):
        return hashlib.sha1(key).hexdigest()

    def read_table_item(self, key):
        key = self._generate_hash_key(key)
        item = self.table.get_item(Key={'key': key})
        return self._deserialize(item.get('Item', {}))

    def put_table_item(self, key, item):
        item['key'] = self._generate_hash_key(key)
        self.table.put_item(Item=self._serialize(item))
        self._deserialize(item)

    def delete_table_item(self, key):
        key = self._generate_hash_key(key)
        self.table.delete_item(Key={'key': key})

    def _serialize(self, item):
        item['data'] = pickle.dumps(item['data'])
        return item

    def _deserialize(self, item):
        if 'data' not in item:
            return {}

        item['data'] = pickle.loads(item.get('data', '').decode('utf-8'))

        if 'until' in item:
            item['until'] = int(item['until'])

        return item
