from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_notify_email(name,receiver,phone_number):
    # Creating message subject and sender
    subject = 'Upload Documents for approval'
    sender = 'ekmuraya@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/uploademail.txt',{"name": name,"phone_number":phone_number})
    html_content = render_to_string('email/uploademail.html',{"name": name,"phone_number":phone_number})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()

def send_notifyandDelete_email(name,receiver,phone_number):
    # Creating message subject and sender
    subject = 'Reupload Documents for approval'
    sender = 'cocohvee@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/uploadDeleteemail.txt',{"name": name,"phone_number":phone_number})
    html_content = render_to_string('email/uploadDeleteemail.html',{"name": name,"phone_number":phone_number})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()

def send_success_email(name,receiver):
    # Creating message subject and sender
    subject = 'Welcome to Digital360'
    sender = 'cocohvee@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('email/successemail.txt',{"name": name})
    html_content = render_to_string('email/successemail.html',{"name": name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
