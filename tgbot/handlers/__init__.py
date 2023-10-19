"""Import all routers and add them to routers_list."""
from tgbot.handlers.form import form_router

routers_list = [
    form_router,
]

__all__ = [
    "routers_list",
]
