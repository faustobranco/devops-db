import pika
import requests
import json
import sys
import urllib3
import argparse # Adicionado para lidar com argumentos

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Infrastructure Connection Parameters
RABBITMQ_HOST = '172.21.5.76'
RABBITMQ_PORT = 31572
RABBITMQ_USER = 'admin'
RABBITMQ_PASS = 'J4VPegzqSKC6Syji9ga6w1JDcTRgrvDQ'
EXCHANGE_NAME = 'jenkins_exchange' # Exchange central

# Jenkins Configuration
JENKINS_URL = 'https://jenkins.devops-db.internal' 
JENKINS_JOB_PATH = 'job/infrastructure/job/pipelines/job/tests/job/RabbitMQ-Example1'
JENKINS_USER = 'fbranco'
JENKINS_API_TOKEN = '11168682ae86c6a8abe39b219fb1d0424e'

# Health API Configuration
HEALTH_API_URL = 'https://dns-api.devops-db.internal/health'

def trigger_jenkins_pipeline(payload):
    print(f"Triggering Jenkins pipeline...")
    build_url = f"{JENKINS_URL}/{JENKINS_JOB_PATH}/buildWithParameters"
    auth_credentials = (JENKINS_USER, JENKINS_API_TOKEN)
    jenkins_parameters = {'PAYLOAD_JSON': json.dumps(payload)}
    
    try:
        response = requests.post(build_url, auth=auth_credentials, data=jenkins_parameters, verify=False)
        response.raise_for_status()
        print(f"Jenkins build triggered! Status: {response.status_code}")
        return True
    except Exception as err:
        print(f"Jenkins Error: {err}")
        return False

def trigger_health_api(payload):
    print(f"Checking Health API (GET): {HEALTH_API_URL}")
    try:
        response = requests.get(HEALTH_API_URL, verify=False, timeout=5)
        response.raise_for_status()
        print(f"Health API is UP! Status: {response.status_code}")
        return True
    except Exception as err:
        print(f"Health API Error: {err}")
        return False

def process_message(channel, method, properties, body, worker_type):
    print("\n--------------------------------------------------")
    print(f"[x] Worker ({worker_type}) received: {body.decode()}")
    
    try:
        payload = json.loads(body)
        
        if worker_type == 'jenkins':
            success = trigger_jenkins_pipeline(payload)
        else:
            success = trigger_health_api(payload)
        
        if success:
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    except json.JSONDecodeError:
        print("Invalid JSON! Rejecting...")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

def start_worker(worker_type):
    # Definir nome da fila com base no worker
    queue_name = 'jenkins_deploy_queue' if worker_type == 'jenkins' else 'health_monitor_queue'
    
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
        channel = connection.channel()

        # 1. Garantir que a Exchange existe (deve ser fanout para duplicar mensagens)
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout', durable=True)

        # 2. Declarar a fila específica deste worker
        channel.queue_declare(queue=queue_name, durable=True, arguments={'x-dead-letter-exchange': 'jenkins_dlx'})

        # 3. Ligar a fila à Exchange (Bind)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

        channel.basic_qos(prefetch_count=1)
        
        # Usar lambda para passar o worker_type para o callback
        callback_func = lambda ch, method, props, body: process_message(ch, method, props, body, worker_type)
        
        channel.basic_consume(queue=queue_name, on_message_callback=callback_func)

        print(f"[*] Worker {worker_type} listening on '{queue_name}'...")
        channel.start_consuming()

    except Exception as err:
        print(f"CRITICAL: {err}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RabbitMQ Multi-Worker')
    parser.add_argument('--type', choices=['jenkins', 'health'], required=True, help='Worker type')
    args = parser.parse_args()

    try:
        start_worker(args.type)
    except KeyboardInterrupt:
        sys.exit(0)