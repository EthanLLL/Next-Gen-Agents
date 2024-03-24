def get_ip_from_headers(headers):
    return '2.2.2.2'

def get_current_location(ip):
    print(ip)
    # Mock response
    return 'Guangzhou'

def get_current_weather(location, unit='celsius'):
    # Mock response
    print(f'location: {location}')
    if location == 'Guangzhou':
        return 'Guangzhou: Sunny at 25 degrees Celsius.'
    elif location == 'Beijing':
        return ' Beijing: Rainy at 30 degrees'
    return 'It\'s a normal sunny day~'

function_map = {
    'get_current_location': get_current_location,
    'get_current_weather': get_current_weather,
    'get_ip_from_headers': get_ip_from_headers
}