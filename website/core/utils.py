from mail_templated import send_mail

def send_email(template, to, **kwargs):
    send_mail(
        template,
        kwargs,
        'contact@ava-project.com',
        [to]
    )
