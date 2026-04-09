import pika
import requests
import json
import sys
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------
# RabbitMQ AMQP Configuration (Direct NodePort access)
# ---------------------------------------------------------
RABBITMQ_HOST = '172.21.5.76'
RABBITMQ_PORT = 31572
RABBITMQ_USER = 'admin'
RABBITMQ_PASS = 'J4VPegzqSKC6Syji9ga6w1JDcTRgrvDQ'
QUEUE_NAME = 'jenkins_deploy_queue'

# ---------------------------------------------------------
# Jenkins REST API Configuration
# ---------------------------------------------------------
# Replace with your actual Jenkins VM IP/localhost and the Token you generated
JENKINS_URL = 'https://jenkins.devops-db.internal' 
JENKINS_JOB_PATH = 'job/infrastructure/job/pipelines/job/tests/job/RabbitMQ-Example1'
JENKINS_USER = 'fbranco'
JENKINS_API_TOKEN = '11168682ae86c6a8abe39b219fb1d0424e'

def trigger_jenkins_pipeline(payload):
    print(f"Triggering Jenkins pipeline with raw JSON payload via REST API...")
    
    build_url = f"{JENKINS_URL}/{JENKINS_JOB_PATH}/buildWithParameters"
    auth_credentials = (JENKINS_USER, JENKINS_API_TOKEN)
    
    # We wrap the entire JSON object into a single parameter named 'PAYLOAD_JSON'
    jenkins_parameters = {
        'PAYLOAD_JSON': json.dumps(payload)
    }
    
    try:
        response = requests.post(
            build_url, 
            auth=auth_credentials, 
            data=jenkins_parameters, # Passing the single wrapped parameter here
            verify=False
        )
        response.raise_for_status()
        print(f"Jenkins build triggered successfully! HTTP Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as err:
        print(f"CRITICAL: Failed to communicate with Jenkins API. Error: {err}")
        return False

def process_message(channel, method, properties, body):
    print("\n--------------------------------------------------")
    print(f"[x] Received message from RabbitMQ: {body.decode()}")
    
    try:
        payload = json.loads(body)
        success = trigger_jenkins_pipeline(payload)
        
        if success:
            print("Acknowledging message.")
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Erro no Jenkins? Requeue para tentar de novo
            print("Requeueing message due to Jenkins error.")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    except json.JSONDecodeError:
        print("Invalid JSON! Sending to Dead Letter Exchange...")
        # AQUI é onde o DLX entra em ação: requeue=False move para a DLX
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

def start_worker():
    try:
        print(f"Connecting to AMQP Broker at {RABBITMQ_HOST}:{RABBITMQ_PORT}...")
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        print("AMQP connection established successfully.")

        # Ensure the queue exists before trying to consume from it
        queue_args = {
            'x-dead-letter-exchange': 'jenkins_dlx'
        }

        # Altera a declaração da fila para incluir os argumentos
        channel.queue_declare(queue=QUEUE_NAME, durable=True, arguments=queue_args)

        # Prefetch count ensures the worker only gets 1 message at a time (Fair Dispatch)
        channel.basic_qos(prefetch_count=1)
        
        # Bind the processing function to the queue
        channel.basic_consume(
            queue=QUEUE_NAME, 
            on_message_callback=process_message, 
            auto_ack=False # We handle acknowledgements manually for reliability
        )

        print(f"[*] Worker is listening to '{QUEUE_NAME}'. To exit press CTRL+C")
        # This will create an infinite loop listening for messages
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as err:
        print(f"CRITICAL: Failed to connect to AMQP broker. Error: {err}")
        sys.exit(1)
    except Exception as err:
        print(f"CRITICAL: Worker process failed unexpectedly. Error: {err}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user (CTRL+C). Shutting down gracefully...")
        sys.exit(0)