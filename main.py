import os
import sys

W = '\033[0m'   # White
L = '\033[90m'  # Grey
R = '\033[31m'  # Red
G = '\033[32m'  # Green
Y = '\033[33m'  # Yellow

try:
    import time
    import json
    import pystyle
    import requests
    import datetime
    from concurrent.futures import ThreadPoolExecutor

except ModuleNotFoundError:
    os.system("""
    pip install time
    pip install json
    pip install pystyle
    pip install requests
    pip install datetime
    pip install concurrent
    """)

class console:
    def get_info():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time
    
    def info(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] " + content)

    def error(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] {R}ERROR: {W}" + content)

    def success(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] {G}SUCCESS: {W}" + content)

    def ratelimited(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] {Y}RATELIMITED: {W}" + content)

    def failed(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] {R}FAILED: {W}" + content)

    def captcha(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] {Y}CAPTCHA: {W}" + content)

try:
    sessions = requests.Session()
except Exception as e:
    console.error(str(e))

class BypassRules:
    def accepting_rules(guild_id, token):
        try:
            headers = {
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "authorization": token,
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDExIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc5ODgyLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMDMwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
            }

            get_verification = sessions.get(f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false", headers=headers).json()
            session = sessions.put(f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me", headers=headers, json=get_verification)

            if session.status_code == 201:
                console.success(f"Rules accepted {L}{token[:26]}***")

            elif session.status_code == 200:
                console.success(f"Rules accepted {L}{token[:26]}***")

            elif session.status_code == 429:
                rate = session.json()
                console.ratelimited(f"For {rate['retry_after']} seconds")

            else:
                console.failed(f"Cannot accept the rules on this guild. {L}status: {session.status_code}")

        except Exception as e:
            console.error(str(e))

class Joining:
    def join(invite, guild_id, delay, threads, token, headers):
        try:
            session = sessions.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={})

            if session.status_code == 200:
                console.success(f"Joined {L}{token[:26]}***")

            elif session.status_code == 201:
                console.success(f"Joined {L}{token[:26]}***")

            elif session.status_code == 400:
                console.captcha(f"{token[:26]}***")

            elif session.status_code == 429:
                rate = session.json()
                console.ratelimited(f"For {rate['retry_after']} seconds")

            else:
                console.failed(f"Cannot join tokens to this guild, {L}status: {session.status_code}")

        except Exception as e:
            console.error(str(e))

        BypassRules.accepting_rules(guild_id, token)

class JoinerTokens:
    def banner():
        print(pystyle.Center.XCenter("""\n\n
╔╗ ╦ ╦╔═╗╦╔═╗╦╔╗╔╔═╗╦═╗
╠╩╗╚╦╝╠═╝║║ ║║║║║║╣ ╠╦╝
╚═╝ ╩ ╩ ╚╝╚═╝╩╝╚╝╚═╝╩╚═ v0.2
        """))

    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        JoinerTokens.banner()
        with open("tokens.txt", "r") as file:
            tokens = file.read().strip().splitlines()
            if len(tokens) <= 1:
                console.error("No tokens in tokens.txt, please input you tokens")
                time.sleep(3)
                sys.exit()
        
        #with open("proxies.txt", "r") as file:
        #    proxies = file.read().strip().splitlines()

        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            #"authorization": token,
            "referer": "https://discord.com/channels/@me",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDExIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc5ODgyLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMDMwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
        }
            
        while True:
            try:
                invite = input(" INVITE: ")
                if invite.startswith("https:"):
                    console.error("Only the invite code")
                    time.sleep(2)
                    JoinerTokens()
                guild_id = int(input(" GUILD ID: "))

                delay = input(" DELAY (Enter to skip): ")

                if delay == "":
                    delay = 0

                delay = int(delay)
                counttokens = len(tokens)
                threads = int(input(f" THREADS (1-{counttokens}): "))
                    
                if threads > counttokens:
                    threads = int(counttokens)

                break
            except ValueError:
                console.error("Invalid input")
                time.sleep(2)
                JoinerTokens()

        executor = ThreadPoolExecutor(max_workers=int(threads))
        for token in tokens:
            try:
                headers.update({"authorization": token})
                executor.submit(Joining.join, invite, guild_id, delay, threads, token, headers)
            except Exception as e:
                console.error(str(e))

if __name__ == "__main__":
    JoinerTokens()
