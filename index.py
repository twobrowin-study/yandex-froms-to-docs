import os
from base64 import b64decode

from template import FillTemplate
from mail import SendDocuments

from dateutil.parser import parse

def handler(event, context):
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405
        }

    print(f"BODY: {event['body']}")

    body = b64decode(event['body']).decode("utf-8") if event['isBase64Encoded'] else event['body']

    form_answer = {}
    for row in body.split("\n\n"):
        key,val = row.split(":\n")
        val = val.removesuffix("\n")
        
        try:
            val = parse(val).strftime(os.environ['DATE_FORMAT'])
        except ValueError:
            pass
        
        form_answer[f"<{key.upper()}>"] = val
    
    print(f"ANSWERS: {form_answer}")
    
    mail_to = form_answer[os.environ['MAIL_TO_FORM_KEY']]
    documents = [
        (filename, FillTemplate(f"templates/{filename}", form_answer))
        for filename in os.listdir('templates')
    ]
    SendDocuments(mail_to, documents)

    return {
        'statusCode': 200
    }