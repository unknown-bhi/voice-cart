from app.modules.tools.mock_tools import (
    get_current_time,
    check_order_status,
    
)

from app.modules.tools.ecommerce_tools import get_real_order_summary

def get_all_tools():

    return [
        get_current_time,
        check_order_status,
        get_real_order_summary
    ]