from mail_templated import EmailMessage


def send_email(template, to, **kwargs):
    message = EmailMessage()
    message.template_name = template
    message.context = kwargs
    message.from_email = 'contact@ava-project.com'
    message.to = [to] if isinstance(to, str) else to
    message.send()
