import os
import elasticapm
from elasticapm import capture_span
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)

apm_client = elasticapm.Client(
    service_name=os.environ.get("ELASTIC_APM_SERVICE_NAME"),
    server_url=os.environ.get("ELASTIC_APM_SERVER_URL"),
    secret_token=os.environ.get("ELASTIC_APM_SECRET_TOKEN"),
    environment=os.environ.get("ENVIRONMENT", "development"),
    log_level="debug",
    verify_server_cert=False,
)

def lambda_handler(event, context):
    apm_client.begin_transaction("request")
    print("APM client is active:", apm_client.config)
    apm_client.capture_message("Test message from Lambda")

    try:
        result = my_function()
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        apm_client.capture_exception()
        raise
    finally:
        apm_client.end_transaction("lambda_handler", "success")

@capture_span(span_type="custom", span_subtype="logic")
def my_function():
    import time
    time.sleep(0.2)
    return "Success"
