from dataclasses import dataclass, field
from typing import Any


@dataclass
class Response(object):
    ok: bool = field(default=False)
    data: Any = field(default=None)
    message: str = field(default='')
