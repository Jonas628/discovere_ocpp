from ocpp_d.v16 import call_result


async def handle_status_notification(connector_id, error_code, status, **kwargs):

    return call_result.StatusNotificationPayload()