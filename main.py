# TODO: Basic IPConfig working, remove old code since cant be used in under 4 lines for windows notification

# TODO: add a regular click mode, and add some sort of setting for "on regular click, do foo", that way user will not
# need to right click then left click for what they want if its just one thing, this doesnt seem that useful tbh

# TODO: add internet check incase no internet to get requests to display "connection error" or something
# THIS IS ONLY NEEDED FOR QUOTES SO FAR

# TODO: battery info/screenshot app/implement translucent tb??/panda that follows cursor around?/ask gpt for more ideas
# translucent is so weird, maybe I could port it in? But idk I dont think its open source, we can check later
# maybe my own script to change the system sounds levels

# TODO: I want to make all these "modules" (weather, battery, screenshot etc) toggleable, and possibly a custom
# installer for the ones you want, but I think thats gonna be overkill

import threading
import time
import pystray
import PIL.Image
import requests
import psutil
import socket
import ping3

image = PIL.Image.open("bamboo-canes.png")

# Global timing variables
timer_running = False
timer_thread = None


def twenty_twenty_twenty_timer():
    global timer_running, timer_thread
    if timer_running:
        icon.notify("Time for a 20-20-20 break!", "TrayPanda")
        print("Time for a 20-20-20 break!")
        # Schedule the next break after 20 minutes
        timer_thread = threading.Timer(20 * 60, twenty_twenty_twenty_timer)
        timer_thread.start()


def toggle_timer(icon, item):
    global timer_running, timer_thread
    if not timer_running:
        print("Timer started.")
        icon.notify("20-20-20 timer started", "TrayPanda")
        timer_running = True
        # Start the timer initially after 20 minutes
        timer_thread = threading.Timer(20 * 60, twenty_twenty_twenty_timer)
        timer_thread.start()
    else:
        print("Timer stopped.")
        icon.notify("20-20-20 timer stopped", "TrayPanda")
        timer_running = False
        # Cancel any running timer thread
        if timer_thread:
            timer_thread.cancel()


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

        active_interfaces = [name for name, stat in stats.items() if
                             stat.isup and name != 'Loopback Pseudo-Interface 1']

        if active_interfaces:
            main_adapter = active_interfaces[0]
            ipv4 = next((addr.address for addr in info[main_adapter] if addr.family == socket.AF_INET), 'N/A')
            ipv6 = next((addr.address for addr in info[main_adapter] if addr.family == socket.AF_INET6), 'N/A')
            mac = next((addr.address for addr in info[main_adapter] if addr.family == psutil.AF_LINK), 'N/A')

            return (f"Adapter: {main_adapter}\n"
                    f"IPv4: {ipv4}\n"
                    f"IPv6: {ipv6}\n"
                    f"MAC: {mac}\n")
        else:
            return "No active network adapters found."
    except Exception as e:
        return f"Error: {e}"


def on_clicked(icon, item):
    if item.text == "Random Quote":
        icon.notify(get_quote(), "Quote of the day!")
    elif item.text == "IPConfig Info":
        icon.notify(get_ipconfig_info(), "IPConfig Info")
    elif item.text == "Toggle Timer":
        toggle_timer(icon, item)


icon = pystray.Icon("Bamboo", image, menu=pystray.Menu(
    pystray.MenuItem("Random Quote", on_clicked),
    pystray.MenuItem("IPConfig Info", on_clicked),
    pystray.MenuItem("Toggle Timer", on_clicked)
), HAS_NOTIFICATION=True)

icon.run()
