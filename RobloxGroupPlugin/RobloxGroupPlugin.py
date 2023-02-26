import discord
import asyncio
import requests
import json
from datetime import datetime, timedelta

class RobloxGroupPlugin:
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = "channel_id_here" # Replace with the ID of the channel where you want to post the members
        self.group_id = "group_id_here" # Replace with the ID of your ROBLOX group
        self.auth_cookie = "auth_cookie_here" # Replace with your ROBLOX authentication cookie
        self.delay = 86400 # Delay in seconds, 86400 = 24 hours

    async def post_members(self):
        try:
            url = f"https://groups.roblox.com/v1/groups/{self.group_id}/roles"
            headers = {"cookie": f".ROBLOSECURITY={self.auth_cookie}"}
            response = requests.get(url, headers=headers)
            roles = json.loads(response.text)["roles"]
            members = {}
            for role in roles:
                url = f"https://groups.roblox.com/v1/groups/{self.group_id}/roles/{role['id']}/users"
                response = requests.get(url, headers=headers)
                users = json.loads(response.text)["data"]
                for user in users:
                    if user["id"] not in members:
                        members[user["id"]] = {"username": user["name"], "role": role["name"]}
            members_list = []
            for member_id, member_data in members.items():
                members_list.append(f"{member_data['username']} ({member_data['role']})")
            members_list.sort()
            members_str = "\n".join(members_list)
            channel = self.bot.get_channel(self.channel_id)
            await channel.send(f"Members of {self.group_id}:\n{members_str}")
        except:
            pass

    async def start_posting(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.post_members()
            await asyncio.sleep(self.delay)

def setup(bot):
    bot.add_cog(RobloxGroupPlugin(bot))
