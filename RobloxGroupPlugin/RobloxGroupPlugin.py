import discord
import asyncio
import requests
import json
from datetime import datetime, timedelta
from discord.ext import tasks, commands

class RobloxGroupPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 455189806180466701 # Replace with the ID of the channel where you want to post the members
        self.group_id = 2572027 # Replace with the ID of your ROBLOX group
        self.auth_cookie =   _|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_AE492D2A4BD8B066298583FC5B0C17EF98564E85130F0AD24ED2E94AABE4C646D4305F335634EBF2C6298AF3D010650B6A4A1577C3C0376A9051EC52E99951BECC2CB5E3050F6A03D7A09C4BC708306E07295109CBF4AB27E2294FA8D71AC492E44DED11014655E03A725F878D291EE73D9522C60DE477D2274B8EC3C4C4AA868CB0D5E64AF485FE7F9739D94B09A5F75966A2FBB0E59FF106860988984DBBE41A53EEFB74E6DFC60DAB8A18ED71D342A1AC96C9B12E2C1CF36B0FBEE7023CDBDB5B2DEB0C465FFA7E97EF7C23F833626AC39B9F5846886AB12758E6A1D11E0EF6FE71DBAFC5B3BCCC1D6EEC4F205FFF67EB8BFB6533E058821342DD16AD83900D41BD43442B848EC845B78F47851385D65023C65C9B09573933D121E975862D8ACF4D42F13493A45F28AD3C19BF5430066421455541E30BD3B171F3162830D81545F78A30F71925713361DFAB3689BA6E00FA7C4EC30DDE4F334AA443A2C2E2018744BB # Replace with your ROBLOX authentication cookie
        self.post_members.start()

    def cog_unload(self):
        self.post_members.cancel()

    @tasks.loop(hours=24.0)
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

    @post_members.before_loop
    async def before_post_members(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(RobloxGroupPlugin(bot))

