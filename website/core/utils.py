from mail_templated import EmailMessage

from core.context_processors import base_url

def merge_two_dicts(x, y):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    """
    z = x.copy()
    z.update(y)
    return z


def send_email(template, to, **kwargs):
    message = EmailMessage()
    message.template_name = template
    message.context = merge_two_dicts(kwargs, base_url())
    message.from_email = 'contact@ava-project.com'
    message.to = [to] if isinstance(to, str) else to
    message.send()
