ddbc
=======

[![Version](https://img.shields.io/pypi/v/ddbc.svg)](https://pypi.python.org/pypi/ddbc)
[![Build Status](https://img.shields.io/travis/marcy-terui/ddbc/master.svg)](http://travis-ci.org/marcy-terui/ddbc)
[![Coverage](https://img.shields.io/coveralls/marcy-terui/ddbc.svg)](https://coveralls.io/github/marcy-terui/ddbc)

# Description

Amazon DynamoDB as a cache store.

# Requirements

- Python2.7
- pip

# Installation

## PyPI

```sh
pip install ddbc
```

# Setup

- Create IAM Role or User

Policy example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "dynamodb:CreateTable",
              "dynamodb:DeleteItem",
              "dynamodb:GetItem",
              "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:<region>:<account-id>:table/<cache-table>"
        }
    ]
}
```

- Create the DynamoDB table for cache

Script Example:

```python
#!/usr/bin/env python

import ddbc.utils

ddbc.utils.create_table(
    table_name='cache_table',
    region='us-east-1', # optional
    read_units=10,      # default: 5
    write_units=10      # default: 5
)
```

# Usage

```python
import ddbc.cache
import time

cache = ddbc.cache.Client(
    table_name='cache_table',
    region='us-east-1', # optional
    default_ttl=100,    # default: -1 (Infinity)
    report_error=True   # default: False
)
cache['foo'] = 'bar'
print(cache['foo']) # => 'bar'

time.sleep(100)
print(cache['foo']) # => None

cache.set('foo', 'bar', 1000)
time.sleep(100)
print(cache['foo']) # => 'bar'

del cache['foo']
print(cache.get('foo', 'buz')) # => 'buz'
```

Development
-----------

-   Source hosted at [GitHub](https://github.com/marcy-terui/ddbc)
-   Report issues/questions/feature requests on [GitHub
    Issues](https://github.com/marcy-terui/ddbc/issues)

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1.  Fork the repo
2.  Create your feature branch (`git checkout -b my-new-feature`)
3.  Commit your changes (`git commit -am 'Added some feature'`)
4.  Push to the branch (`git push origin my-new-feature`)
5.  Create new Pull Request

Authors
-------

Created and maintained by [Masashi Terui](https://github.com/marcy-terui) (<marcy9114@gmail.com>)

License
-------

MIT License (see [LICENSE](https://github.com/marcy-terui/ddbc/blob/master/LICENSE))
