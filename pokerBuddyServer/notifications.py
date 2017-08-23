from exponent_server_sdk import DeviceNotRegisteredError,PushClient,PushMessage
from exponent_server_sdk import PushResponseError,PushServerError
from requests.exceptions import ConnectionError, HTTPError


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
            body=message,
            data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        print({
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        print({'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    try:
    # We got a response back, but we don't know whether it's an error yet.
    # This call raises errors so we can handle them with normal exception
    # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        print({
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise self.retry(exc=exc)