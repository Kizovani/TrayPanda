# TODO: add weather app, and see if you can make it show up in the actual taskbar? And also see if you can make it
# automatically send alerts if the weather conditions get really bad, maybe make it ping for weather every couple mins?
# and add a manual refresh button to check weather, but make sure extreme alert only comes up when the app is not
# focused

# TODO: add a regular click mode, and add some sort of setting for "on regular click, do foo", that way user will not
# need to right click then left click for what they want if its just one thing

# TODO: add internet check incase no internet to get requests to display "connection error" or something

# TODO: battery info/screenshot app/implement translucent tb??/panda that follows cursor around?/ask gpt for more ideas

# TODO: I want to make all these "modules" (weather, battery, screenshot etc) toggleable, and possibly a custom
# installer for the ones you want, but I think thats gonna be overkill

import pystray
import PIL.Image
import requests
import threading  # dont think ill need this for now, but should look into using it when app gets big
import psutil
import socket
import ping3

# for info on api for quotes: https://forismatic.com/en/api/

image = PIL.Image.open("bamboo-canes.png")


def get_quote():
    try:
        response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        quote = data.get("quoteText")
        author = data.get("quoteAuthor")
        if not author:
            author = "Unknown"
        return f"{quote} - {author}"
    except Exception as e:
        return f"Error: {e}"


def get_ipconfig_info():
    try:
        info = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        ping_time = ping3.ping('8.8.8.8')

        # Filter out the loopback and non-active interfaces
        active_interfaces = [name for name, stat in stats.items() if
                             stat.isup and name != 'Loopback Pseudo-Interface 1']

        if active_interfaces:
            main_adapter = active_interfaces[0]
            ipv4 = next((addr.address for addr in info[main_adapter] if addr.family == socket.AF_INET), 'N/A')
            ipv6 = next((addr.address for addr in info[main_adapter] if addr.family == socket.AF_INET6), 'N/A')
            mac = next((addr.address for addr in info[main_adapter] if addr.family == psutil.AF_LINK), 'N/A')
            netmask = next((addr.netmask for addr in info[main_adapter] if addr.family == socket.AF_INET), 'N/A')
            broadcast = next((addr.broadcast for addr in info[main_adapter] if addr.family == socket.AF_INET), 'N/A')
            gateway = 'N/A'  # Default gateway logic can be added here if necessary

            return (f"Adapter: {main_adapter}\n"
                    f"IPv4: {ipv4}\n"
                    f"IPv6: {ipv6}\n"
                    f"MAC: {mac}\n"
                    f"Netmask: {netmask}\n"
                    f"Broadcast: {broadcast}\n"
                    f"Default Gateway: {gateway}\n"
                    f"Ping Time (to 8.8.8.8): {ping_time * 1000:.2f} ms")
        else:
            return "No active network adapters found."
    except Exception as e:
        return f"Error: {e}"



# icon is the tray icon and item what is clicked
def on_clicked(icon, item):
    if item.text == "Random Quote":
        icon.notify(get_quote(), "Quote of the day!")
    elif item.text == "IPConfig Info":
        icon.notify(get_ipconfig_info(), "IPConfig Info")


icon = pystray.Icon("Bamboo", image, menu=pystray.Menu(
    pystray.MenuItem("Random Quote", on_clicked),
    pystray.MenuItem("IPConfig Info", on_clicked)
), HAS_NOTIFICATION=True)

icon.run()
