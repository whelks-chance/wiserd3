from django.core.mail.message import EmailMultiAlternatives
from wiserd3.settings import ADMIN_EMAIL_ADDRESSES

__author__ = 'ubuntu'


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

EMAIL_TYPES = enum('REQUEST_ACCESS', 'BUG_REPORT')


def send_email(request_user, email_type, email_data):

    print email_type, email_type == EMAIL_TYPES.REQUEST_ACCESS

    email_text = 'To WISERD DataPortal Administrator\n\n'
    email_text += 'User {} has requested access to {}.\n\n'.format(
        request_user.user.username, email_data['survey_id']
    )
    email_text += 'Thanks.\n\nThis is an automated message, please do not reply.'
    email_text += '\n\nLost Visions/ Illustration Archive, 2015'

    html_text = '<strong>To WISERD DataPortal Administrator</strong><br><br>'
    html_text += '<p>User {} has requested access to {}.</p><br>'.format(
        request_user.user.username,
        email_data['survey_id']
    )
    html_text += '<p>Thanks.</p><p>This is an automated message, please do not reply.</p>'
    html_text += '<br><p>Lost Visions/ Illustration Archive, 2015<p>'

    email = EmailMultiAlternatives('REQUEST ACCESS', email_text, to=ADMIN_EMAIL_ADDRESSES)
    email.attach_alternative(html_text, "text/html")
    res = email.send()
    return res
