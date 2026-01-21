from accounts.models import Session


class SimpleSessionMiddleware:
    COOKIE_NAME = "simple_session_id"

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.COOKIES.get("simple_session_id")
        session = None

        if session_key:
            session = Session.get_valid_session(session_key=session_key)

        request.simple_session = session
        request.simple_user = session.user if session else None

        response = self.get_response(request)

        if hasattr(request, "_new_session") and request._new_session:
            response.set_cookie(
                self.COOKIE_NAME,
                request._new_session.session_key,
                max_age=60 * 60 * 24 * 7,
                httponly=True,
            )

        if hasattr(request, "_delete_session") and request._delete_session:
            response.delete_cookie(self.COOKIE_NAME)

        return response
        