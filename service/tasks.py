#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import re

from celery import task

from restclient import GET, POST, PUT, DELETE
from datetime import datetime
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage
import json
import time

def email_send_with_api(subject, to, msg, fr=None):
    if not fr:
        fr = 'Voidtraining'
    url = 'http://www.tokowebku.com/api/email_sender/'
    form_fields = {
        "from": fr,
        "subject": subject,
        "to": to,
        "msg": msg
    }
    result = POST(url, async=False, params=form_fields)
    return result

def send_sms(no, text):
    while True:
        if '+62' in no:
            no = no.replace('+62', '0')
        no = no.split('/')[0]
        no = ''.join(re.findall(r'[\d]+', no))
        url = 'http://www.freesms4us.com/kirimsms.php'
        data = {'user':'synl0rd', 'pass':'bl00d13z', 'isi': text, 'no':no}
        data = urllib.urlencode(data)
        complete_url = url + '?' + data
        resp = GET(complete_url)
        if 'GAGAL' not in resp:
            break

    email_send_with_api('SMS REPORT STATUS', 'hadi.wijaya@voidsolution.com', 'Resp: %s<br><br>Text:%s' % (resp, text))
    return resp


@task()
def send_sms_task(no, text):
    return send_sms(no, text)

@task()
def send_email_task(subject, to, msg, from_email='Voidtraining <support@voidtraining.com>', reply_to=None):
    from voidtraining.models import *
    time.sleep(1)
    print 'subject: %s' % subject
    print 'to: %s' % to
    headers = {'Reply-To': 'support@voidtraining.com'}
    if reply_to:
        headers = {'Reply-To': reply_to}

    while True:
        try:
            subject = subject
            html_content = msg
            to = to
            e = EmailMessage(subject, html_content, from_email, json.loads(to), headers=headers)
#            if attachment_id:
#                for i in json.loads(attachment_id):
#                    f = Attachment.objects.get(id=i)
#                    e.attach(f.file.name, f.file.read())
            e.content_subtype = "html"
            e.send(fail_silently=False)
        except Exception, err:
            print err
        else:
            print 'Email Status: Success to: %s' % to
            break
    return True


# send_nofitication(subject= , to= ,msg_email= ,msg_sms= ,notif_type= ,ref_id= )
@task()
def send_notification(**kwargs):
    from voidtraining.models import *
    time.sleep(1)
    u = User.objects.filter(id__in=json.loads(kwargs['to']))
    subject = kwargs['subject']
    to = [i.email for i in u]
    msg_email = kwargs['msg_email']
    msg_sms = kwargs['msg_sms']

    send_email_task.delay(subject, json.dumps(to), msg_email)

    for i in u:
        phone = i.student_set.get().phone
        send_sms_task.delay(phone, msg_sms)
        n = Notification()
        n.timestamp = datetime.utcnow()
        n.notif_type = kwargs['notif_type']
        n.to = i
        n.ref_id = kwargs['ref_id']
        if kwargs.get('note'):
            n.note = kwargs.get('note')
        n.save()
    return True