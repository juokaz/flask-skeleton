from . import TestCase

from ..utils import send_mail, format_currency, nl2br
from collections import namedtuple


class UtilsTest(TestCase):
    def test_send_meil(self):
        mail = self.app.extensions.get('mail')

        with mail.record_messages() as outbox:
            send_mail('Welcome!', 'user@example.com',
                      'confirmation_instructions', True, user=1)

        self.assertEquals(1, len(outbox))
        self.assertEquals('Welcome!', outbox[0].subject)

    def test_format_currency(self):
        self.assertEquals('$10.12', format_currency(10.123))
        self.assertEquals('', format_currency(None))

    def test_nl2br(self):
        d = {"autoescape": True}
        context = namedtuple('Context', d.keys())(*d.values())

        self.assertEquals('', nl2br(context, None))

        result = str(nl2br(context, "Hello\nworld"))
        self.assertEquals("Hello<br>\nworld<br />", result)
