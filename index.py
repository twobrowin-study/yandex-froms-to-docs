import os
from base64 import b64decode

from template import FillTemplate
from mail import SendDocuments

def handler(event, context):
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405
        }

    print(f"DEBUG: original body is \n{event['body']}\n")

    body = b64decode(event['body']).decode("utf-8") if event['isBase64Encoded'] else event['body']

    form_answer = {}
    for row in body.split("\n\n"):
        key,val = row.split(":\n")
        form_answer[f"<{key.upper()}>"] = val.removesuffix("\n")
    
    print(f"DEBUG: form answers dict is \n{form_answer}\n")
    
    mail_to = form_answer[os.environ['MAIL_TO_FORM_KEY']]
    documents = [
        (filename, FillTemplate(f"templates/{filename}", form_answer))
        for filename in os.listdir('templates')
    ]
    SendDocuments(mail_to, documents)

    return {
        'statusCode': 200
    }