"""Type definitions for AWS Lambda."""

from typing import Any, TypedDict

LambdaDict = dict[str, Any]


class LambdaCognitoIdentity(TypedDict):
    """Amazon Cognito identity that authorized a request."""

    cognito_identity_id: str
    """The authenticated Amazon Cognito identity."""

    cognito_identity_pool_id: str
    """The Amazon Cognito identity pool that authorized the invocation."""


class LambdaClientContextMobileClient(TypedDict):
    """Mobile client information."""

    app_package_name: str
    """The client app package name."""

    app_title: str
    """The client app title."""

    app_version_code: str
    """The client app version code."""

    app_version_name: str
    """The client app version name."""

    installation_id: str
    """The client installation ID."""


class LambdaClientContext(TypedDict):
    """Client context that's provided to Lambda by the client application."""

    client: LambdaClientContextMobileClient
    """Mobile client information."""

    custom: LambdaDict
    """A dict of custom values set by the mobile client application."""

    env: LambdaDict
    """A dict of environment information provided by the AWS SDK."""


class LambdaContext:
    """When a Function is invoked, it passes a context object to the handler.

    This object provides methods and properties that provide information about
    the invocation, function, and execution environment.

    """

    aws_request_id: str
    """The identifier of the invocation request."""

    client_context: LambdaClientContext | None
    """*(mobile apps)* Client context that's provided to Lambda by the client application."""

    function_name: str
    """The name of the Lambda function."""

    function_version: str
    """The version of the Lambda function."""

    identity: LambdaCognitoIdentity | None
    """*(mobile apps)* Information about the Amazon Cognito identity that authorized the request."""

    invoked_function_arn: str
    """The Amazon Resource Name (ARN) that's used to invoke the function.
    Indicates if the invoker specified a version number or alias.

    """

    log_group_name: str
    """The log group for the function."""

    log_stream_name: str
    """The log stream for the function instance."""

    memory_limit_in_mb: int
    """The amount of memory that's allocated for the function."""

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        """Number of milliseconds left before the execution times out.

        This is a "mock" method that will always return ``0``.

        """
        return 0


class LambdaSqsEventRecordAttributes(TypedDict):
    """Attributes of an SQS message that are set by the SQS service."""

    ApproximateFirstReceiveTimestamp: str
    """The time the message was first received from the queue (epoch time in milliseconds)."""

    ApproximateReceiveCount: str
    """The number of times a message has been received from the queue but not deleted."""

    SenderId: str
    """ID for IAM user/role/etc that sent the message."""

    SentTimestamp: str
    """The time the message was sent to the queue (epoch time in milliseconds)."""


class LambdaSqsEventMessageAttributes(TypedDict):
    """Optional metadata that can be added to an SQS message.

    https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-attributes.html

    """

    Name: str
    """The message attribute value."""

    Type: str
    """The message attribute data type.

    Supported types include ``String``, ``Number``, and ``Binary``.

    """

    Value: bytes | (float | (int | str))
    """The message attribute value."""


class LambdaSqsEventRecord(TypedDict):
    """Record from a Lambda invocation event from an SQS Queue."""

    attributes: LambdaSqsEventRecordAttributes
    """Attributes of an SQS message that are set by the SQS service."""

    awsRegion: str
    """AWS region code where the Queue is located."""

    body: str
    """The message's contents (not URL-encoded)."""

    eventSource: str
    """AWS service that the event came from."""

    eventSourceARN: str
    """ARN of the AWS resource that the event came from."""

    md5OfBody: str
    """An MD5 digest of the non-URL-encoded message body string."""

    messageId: str
    """A unique identifier for the message.

    A messageId is considered unique across all AWS accounts for an extended
    period of time.

    """

    messageAttributes: list[LambdaSqsEventMessageAttributes]
    """Optional metadata that can be added to an SQS message."""

    receiptHandle: str
    """An identifier associated with the act of receiving the message.

    A new receipt handle is returned every time you receive a message.
    When deleting a message, you provide the last received receipt handle to delete the message.

    """


class LambdaSqsEvent(TypedDict):
    """Lambda invocation event from an SQS Queue."""

    Records: list[LambdaSqsEventRecord]
    """List of SQS messages."""
