from loader import dp
from .admin import AdminFilter


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
