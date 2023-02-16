import json
import index

if __name__ == '__main__':
    with open("test-event.json", "r") as content:
        event = json.load(content)
    print(index.handler(event, {"test": True}))
