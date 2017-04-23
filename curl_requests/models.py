import json

from .status_codes import codes


#: The set of HTTP status codes that indicate an automatically
#: processable redirect.
REDIRECT_STATI = (
    codes.moved_permanently,   # 301
    codes.found,               # 302
    codes.see_other,           # 303
    codes.temporary_redirect,  # 307
    codes.permanent_redirect,  # 308
)


class Request:
    __slots__ = ()


class PreparedRequest:
    __slots__ = ()


class Response:
    __slots__ = ('content', 'headers', '_status_code')

    @property
    def status_code(self):
        return self._status_code._idx

    def __repr__(self):
        return '<Response [{}]>'.format(self.status_code)

    @property
    def is_permanent_redirect(self):
        """True if this Response one of the permanent versions of redirect"""
        return ('location' in self.headers and self.status_code in
                (codes.moved_permanently, codes.permanent_redirect))

    @property
    def is_redirect(self):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        return ('location' in self.headers
                and self.status_code in REDIRECT_STATI)
        return self.status_code in range(300, 399)

    @property
    def text(self):
        return self.content.decode('utf-8')

    def json(self):
        return json.loads(self.text)
