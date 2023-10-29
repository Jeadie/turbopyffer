import json
from typing import Any, Callable, Dict, Literal, Optional, Union
from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry

from.error import TurboPufferError


HttpMethod = Literal['POST', 'GET', 'PUT', 'HEAD', 'POST']


class HttpRequests:
    def __init__(self, base_url: str, headers: Dict[str, str]) -> None:
        self.session = self._create_session(headers)
        self.base_url = base_url

    def send_request(
        self,
        method: HttpMethod,
        path: str,
        param: Optional[Dict[str, Any]] = None,
        body: Optional[Union[Any, bytes, str]] = None,
    ) -> Any:
        if not isinstance(body, (bytes, str)) and body is not None:
            body = json.dumps(body)

        response: Response = self._operation(method)(
            url=f"{self.base_url}{path}",
            data=body,
            params=param.copy() if param else None,
            verify=True,
        )
        response.raise_for_status()
        return response.json()

    def _operation(self, method: HttpMethod) -> Callable[[], Response]:
        if method == "GET":
            _call = self.session.get
        elif method == "POST":
            _call = self.session.post
        elif method == "PUT":
            _call = self.session.put
        elif method == "HEAD":
            _call = self.session.head
        elif method == "DELETE":
            _call = self.session.delete
        else:
            raise TurboPufferError(f"{method} is not a valid HTTP operation")
        return _call

    def _create_session(self, headers: Dict[str, str]) -> Session:
        sess = Session()
        sess.headers = headers
        sess.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    backoff_factor=2,
                    # Only retry 500s on GET so we don't unintionally mutute data
                    allowed_methods=["GET"],
                    # https://support.cloudflare.com/hc/en-us/articles/115003011431-Troubleshooting-Cloudflare-5XX-errors
                    status_forcelist=[
                        429,
                        500,
                        502,
                        503,
                        504,
                        520,
                        521,
                        522,
                        523,
                        524,
                        526,
                        527,
                    ],
                )
            ),
        )
        return sess