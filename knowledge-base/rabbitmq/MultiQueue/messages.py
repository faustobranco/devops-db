import pika
import sys
import json
import argparse

# Infrastructure Connection Parameters
RABBITMQ_HOST = '172.21.5.76'
RABBITMQ_PORT = 31572
RABBITMQ_USER = 'admin'
RABBITMQ_PASS = 'J4VPegzqSKC6Syji9ga6w1JDcTRgrvDQ'
EXCHANGE_NAME = 'jenkins_exchange'
ROUTING_KEY = 'deploy_app'

def send_message(corrupt=False):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
        channel = connection.channel()

        if corrupt:
            # Sending a plain string that is NOT a valid JSON
            message_body = "INVALID_DATA_NOT_JSON_FORMAT"
            print("[!] Sending CORRUPT message to test DLX...")
        else:
            # Sending the standard valid JSON payload
            deployment_payload = {
                "application": "frontend-service",
                "environment": "production",
                "version": "v1.4.2",
                "author": "devops-team"
            }
            message_body = json.dumps(deployment_payload)
            print("[+] Sending VALID JSON message...")

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=message_body,
            properties=pika.BasicProperties(delivery_mode=2, content_type='text/plain')
        )

        print("Done. Message published.")
        connection.close()

    except Exception as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    # Using argparse to handle the --corrupt flag
    parser = argparse.ArgumentParser(description='RabbitMQ Message Producer')
    parser.add_argument('--corrupt', action='store_true', help='Send an invalid non-JSON message')
    args = parser.parse_args()

    send_message(corrupt=args.corrupt)