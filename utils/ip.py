# imports
from colorama import Fore, Style


# functions
def format_ip(json: dict) -> str:

    if not json['success']:
        return f'``{json["ip"]}`` is not a valid IP address'

    formatted = f'''
```ansi
{Style.BRIGHT}{Fore.BLUE}===   IP INFORMATION   ==={Style.RESET_ALL}
{Style.BRIGHT}{Fore.MAGENTA}IP{Style.RESET_ALL} {json['ip']}
{Style.BRIGHT}{Fore.MAGENTA}Type{Style.RESET_ALL} {json['type']}
{Style.BRIGHT}{Fore.BLUE}===   LOCATION INFORMATION   ==={Style.RESET_ALL}
{Style.BRIGHT}{Fore.MAGENTA}Continent{Style.RESET_ALL} {json['continent']}
{Style.BRIGHT}{Fore.MAGENTA}Continent Code{Style.RESET_ALL} {json['continent_code']}
{Style.BRIGHT}{Fore.MAGENTA}Country{Style.RESET_ALL} {json['country']}
{Style.BRIGHT}{Fore.MAGENTA}Country Code{Style.RESET_ALL} {json['country_code']}
{Style.BRIGHT}{Fore.MAGENTA}Region{Style.RESET_ALL} {json['region']}
{Style.BRIGHT}{Fore.MAGENTA}Region Code{Style.RESET_ALL} {json['region_code']}
{Style.BRIGHT}{Fore.MAGENTA}City{Style.RESET_ALL} {json['city']}
{Style.BRIGHT}{Fore.MAGENTA}Latitude{Style.RESET_ALL} {json['latitude']}
{Style.BRIGHT}{Fore.MAGENTA}Longitude{Style.RESET_ALL} {json['longitude']}
{Style.BRIGHT}{Fore.MAGENTA}Postal Code{Style.RESET_ALL} {json['postal']}
{Style.BRIGHT}{Fore.BLUE}===   Country Information   ==={Style.RESET_ALL}
{Style.BRIGHT}{Fore.MAGENTA}Calling Code{Style.RESET_ALL} +{json['calling_code']}
{Style.BRIGHT}{Fore.MAGENTA}Capital{Style.RESET_ALL} {json['capital']}
{Style.BRIGHT}{Fore.BLUE}===   Timezone Information   ==={Style.RESET_ALL}
{Style.BRIGHT}{Fore.MAGENTA}ID{Style.RESET_ALL} {json['timezone']['id']}
{Style.BRIGHT}{Fore.MAGENTA}Abbreviation{Style.RESET_ALL} {json['timezone']['abbr']}
{Style.BRIGHT}{Fore.MAGENTA}Is Daylight Savings{Style.RESET_ALL} {json['timezone']['is_dst']}
{Style.BRIGHT}{Fore.MAGENTA}UTC Offset{Style.RESET_ALL} {json['timezone']['utc']}
{Style.BRIGHT}{Fore.MAGENTA}Current Time{Style.RESET_ALL} {json['timezone']['current_time']}
{Style.BRIGHT}{Fore.BLUE}===   Network Information   ==={Style.RESET_ALL}
{Style.BRIGHT}{Fore.MAGENTA}Autonomous System Number (ASN){Style.RESET_ALL} {json['connection']['asn']}
{Style.BRIGHT}{Fore.MAGENTA}Organization{Style.RESET_ALL} {json['connection']['org']}
{Style.BRIGHT}{Fore.MAGENTA}Internet Service Provider (ISP){Style.RESET_ALL} {json['connection']['isp']}
{Style.BRIGHT}{Fore.MAGENTA}Domain{Style.RESET_ALL} {json['connection']['domain']}
```'''

    return formatted