import json
import sys


def main(input_parameter):
    print(json.dumps({ 'var_source': 'python', 'topic': input_parameter }, ensure_ascii=False))

if __name__ == "__main__":
    input = sys.stdin.read()
    input_json = json.loads(input)
    main(input_parameter=input_json.get('topic_name'))