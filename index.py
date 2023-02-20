import os
from base64 import b64decode

from template import FillTemplate
from mail import SendDocuments

from dateutil.parser import parse

import json
import re

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
        
        key = key.replace('\n', '')
        key = f"<{key.upper()}>"
        
        val = val.replace('\n', '')
        
        try:
            if '-' in val:
                val = parse(val).strftime(os.environ['DATE_FORMAT'])
        except Exception:
            pass
        
        form_answer[key] = val

    additional_answers = json.loads(os.environ['ADDITIONAL_ANSWERS'])

    for key,items in additional_answers.items():
        for add_key,add_desc in items.items():
            val = form_answer[key]
            if val in add_desc:
                form_answer[add_key] = add_desc[val]
                for rps_key in re.findall(r"<[^<]*>", form_answer[add_key]):
                    if rps_key in form_answer:
                        form_answer[add_key] = form_answer[add_key].replace(rps_key, form_answer[rps_key])
    
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