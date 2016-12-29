# -*- coding: utf-8 -*-

import boto3
import botocore


def get_dynamodb_resource(region):
    if region is None:
        return boto3.resource('dynamodb')
    else:
        return boto3.resource('dynamodb', region)


def get_table(table_name, region):
    return get_dynamodb_resource(region).Table(table_name)


def create_table(table_name, region=None, read_units=5, write_units=5):
    try:
        get_table(table_name, region).creation_date_time
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            raise
        else:
            table = get_dynamodb_resource(region).create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'key',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'key',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'data',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'until',
                        'AttributeType': 'N'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_units,
                    'WriteCapacityUnits': write_units
                }
            )
            table.meta.client.get_waiter('table_exists').wait(
                TableName=table_name)
