import requests
import sys
import time
import json

# 🔗 Replace with your Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1337518831060516864/APwRw5ZS6URK3z8QKjQdOStFWxxm91IA0S33qamcCik29c9nUNgUgHHc00GQ5n98ZKoY"

def loading_screen():
    """Displays a loading screen."""
    animation = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write("\rLoading " + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")

def get_ip_info(ip):
    """Fetches IP details using ipwho.is API."""
    ipwhois_url = f"http://ipwho.is/{ip}"

    try:
        response = requests.get(ipwhois_url)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching IP info: {e}")
        return None

def truncate(value, limit=1024):
    """Truncates long text to fit within Discord's character limits."""
    return value[:limit] + "..." if len(value) > limit else value

def send_to_discord(ip_info):
    """Sends IP details to Discord webhook in a detailed embed."""
    if not ip_info or not ip_info.get("success"):
        print("❌ Failed to retrieve IP info.")
        return

    # 🌐 Extracting details
    ip_address = ip_info.get("ip", "N/A")
    hostname = ip_info.get("hostname", "N/A")
    city = ip_info.get("city", "N/A")
    region = ip_info.get("region", "N/A")
    country = ip_info.get("country", "N/A")
    isp = ip_info.get("isp", "N/A")
    asn = ip_info.get("asn", {}).get("asn", "N/A")
    asn_org = ip_info.get("asn", {}).get("name", "N/A")
    latitude = ip_info.get("latitude", "N/A")
    longitude = ip_info.get("longitude", "N/A")
    timezone = ip_info.get("timezone", {}).get("utc", "N/A")
    ip_type = ip_info.get("type", "N/A")
    is_vpn = "✅ Yes" if ip_info.get("security", {}).get("vpn") else "❌ No"
    is_proxy = "✅ Yes" if ip_info.get("security", {}).get("proxy") else "❌ No"
    is_tor = "✅ Yes" if ip_info.get("security", {}).get("tor") else "❌ No"
    carrier = ip_info.get("connection", {}).get("isp", "N/A")

    # 📝 Full IP Data in a Code Block (Avoiding Discord Limits)
    full_info = json.dumps(ip_info, indent=2)
    full_info = truncate(full_info, 1024)  # Truncate if too long

    # 🌐 Constructing the Discord embed message
    embed = {
        "title": "🌍 IP Lookup Result",
        "color": 7506394,
        "fields": [
            {"name": "🔹 IP Address", "value": ip_address, "inline": True},
            {"name": "🔎 Hostname", "value": hostname, "inline": True},
            {"name": "📍 Location", "value": truncate(f"{city}, {region}, {country}"), "inline": False},
            {"name": "🌐 ISP", "value": truncate(isp), "inline": False},
            {"name": "🛰️ ASN", "value": truncate(f"{asn} ({asn_org})"), "inline": False},
            {"name": "🗺️ Coordinates", "value": f"{latitude}, {longitude}", "inline": False},
            {"name": "⏰ Timezone", "value": timezone, "inline": False},
            {"name": "🔑 IP Type", "value": ip_type, "inline": False},
            {"name": "🔒 VPN?", "value": is_vpn, "inline": True},
            {"name": "🕵️ Proxy?", "value": is_proxy, "inline": True},
            {"name": "🌐 Tor?", "value": is_tor, "inline": True},
            {"name": "📶 Carrier", "value": truncate(carrier), "inline": False},
            {"name": "📜 Full IP Data", "value": f"```json\n{full_info}\n```", "inline": False},
        ],
        "footer": {
            "text": "Powered by ipwho.is",
            "icon_url": "https://ipwho.is/favicon.ico"
        }
    }

    # Sending the embed to Discord
    try:
        data = {"embeds": [embed]}
        headers = {"Content-Type": "application/json"}
        
        # Debug: Print JSON payload before sending
        print("Sending data to Discord...")
        print(json.dumps(data, indent=4))

        response = requests.post(DISCORD_WEBHOOK_URL, json=data, headers=headers)

        if response.status_code == 204:
            print("✅ IP details sent to Discord successfully!")
        else:
            print(f"❌ Failed to send to Discord. Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending data to Discord: {e}")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\n====================")
        print("      Main Menu     ")
        print("====================")
        print("1. Lookup IP Address")
        print("2. Exit")
        print("====================")
        choice = input("Enter your choice: ")

        if choice == "1":
            ip_address = input("Enter an IP address: ")
            loading_screen()
            ip_info = get_ip_info(ip_address)
            send_to_discord(ip_info)
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
