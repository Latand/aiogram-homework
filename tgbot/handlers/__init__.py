"""Import all routers and add them to routers_list."""
from .inline_buttons_1 import inline_buttons_router as task_1
from .inline_buttons_2 import inline_buttons_router as task_2

routers_list = [
    task_1,
    task_2,
]

__all__ = [
    "routers_list",
]
