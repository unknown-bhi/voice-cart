from datetime import datetime
from livekit.agents import function_tool

@function_tool()
async def get_current_time():

    return datetime.now().strftime('%I:%M %p')

@function_tool()
async def check_order_status(order_id : str):

    return {
        'order_id':order_id,
        'status': 'shipped',
        'estimated_delivery' : 'Tommorrow, 5 PM',
        'courier' : 'TCS Express'
    }

@function_tool()
async def get_order_summary(platform :str, period :str):

    return {
        'platform' : platform,
        'period' : period,
        'total_orders': 24,
        'pending' : 3,
        'shipped' : 15,
        'delivered' : 6,
        'total_reveneu' : '$1,450'
    }