import index

if __name__ == '__main__':
    with open('test-body.json', 'r') as content:
        body = content.read()
    index.handler(
        {
            'body': body,
            'isBase64Encoded': False
        },
        {
            'test': True
        }
    )
