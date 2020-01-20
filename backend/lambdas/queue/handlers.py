"""
Queue handlers
"""
import datetime
import random
import json
import os
import uuid

import boto3
from aws_xray_sdk.core import xray_recorder
from boto3.dynamodb.conditions import Attr

from decorators import with_logger, request_validator, catch_errors, load_schema, add_cors_headers

sfn_client = boto3.client("stepfunctions")
dynamodb_resource = boto3.resource("dynamodb")
deletion_queue_table = dynamodb_resource.Table(os.getenv("DeletionQueueTable", "S3F2_DeletionQueue"))
jobs_table = dynamodb_resource.Table(os.getenv("JobTable", "S3F2_Jobs"))
bucket_count = int(os.getenv("GSIBucketCount", 1))


@with_logger
@xray_recorder.capture('EnqueueHandler')
@add_cors_headers
@request_validator(load_schema("queue_item"), "body")
@catch_errors
def enqueue_handler(event, context):
    body = json.loads(event["body"])
    match_id = body["MatchId"]
    data_mappers = body.get("DataMappers", [])
    item = {
        "MatchId": match_id,
        "DataMappers": data_mappers,
    }
    deletion_queue_table.put_item(Item=item, ConditionExpression=Attr("MatchId").not_exists())

    return {
        "statusCode": 201,
        "body": json.dumps(item)
    }


@with_logger
@xray_recorder.capture('GetQueueHandler')
@add_cors_headers
@catch_errors
def get_handler(event, context):
    items = deletion_queue_table.scan()["Items"]

    return {
        "statusCode": 200,
        "body": json.dumps({"MatchIds": items})
    }


@with_logger
@xray_recorder.capture('CancelDeletionHandler')
@add_cors_headers
@request_validator(load_schema("cancel_handler"), "body")
@catch_errors
def cancel_handler(event, context):
    body = json.loads(event["body"])
    match_ids = body["MatchIds"]
    with deletion_queue_table.batch_writer() as batch:
        for match_id in match_ids:
            batch.delete_item(Key={
                "MatchId": match_id
            })

    return {
        "statusCode": 204
    }


@with_logger
@xray_recorder.capture('ProcessDeletionHandler')
@add_cors_headers
@catch_errors
def process_handler(event, context):
    job_id = str(uuid.uuid4())
    item = {
        "Id": job_id,
        "Sk": job_id,
        "Type": "Job",
        "JobStatus": "QUEUED",
        "GSIBucket": str(random.randint(0, bucket_count - 1)),
        "CreatedAt": round(datetime.datetime.now().timestamp()),
    }
    jobs_table.put_item(Item=item)

    return {
        "statusCode": 202,
        "body": json.dumps(item)
    }
