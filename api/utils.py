from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_verification_email(email, token):
    try:
        subject = 'welcome to Hot Offers'
        message = 'Hello'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        html_c = get_template('mail.html')
        context = {
            'token': token,
            'url': f'http://127.0.0.1:8000/api/verify-email/{token}'
        }
        html_content = html_c.render(context)
        msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    except Exception as e:
        print(e)
        return False 
    
    return True