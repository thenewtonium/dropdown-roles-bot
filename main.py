import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption
#from math import ceil
from itertools import chain
import typing

client = ComponentsBot(command_prefix = "drb$")


class SplitRoles(commands.RoleConverter):
    async def convert(self, ctx, argument):
        lists = argument.split(" | ")
        print(lists)
        dropdowns = []
        for roles in lists:
            options = []
            roleslist = roles.split(" ")
            print(roleslist)
            for roletext in roleslist:
                try:
                    role = await super().convert(ctx, roletext)
                    options.append(role)
                except Exception as e:
                    print(e)

            dropdowns.append(options)

        return dropdowns

@client.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def dropdown(ctx, channel : discord.TextChannel, msg_text, placeholder_texts, dropdowns : SplitRoles):
    placeholder_texts = placeholder_texts.split(" | ")
    """avg_opts = len(roles) / (ceil(len(roles) / 25))
    switch_opts = avg_opts
    opt_no = 1
    dropdown_index = 0
    components = []
    options = []
    for role in roles:
        options.append(SelectOption(label = role.name, value = role.id))
        opt_no += 1
        if opt_no > switch_opts:
            switch_opts += avg_opts
            components.append(Select(placeholder = placeholder_texts[dropdown_index], options=options))
            options = []
            dropdown_index += 1"""
    ddi = 0
    components = []
    for dd in dropdowns:
        components.append ( Select(placeholder = placeholder_texts[ddi], options = [SelectOption(label = role.name, value = role.id) for role in dd]))
        ddi += 1
    msg = await channel.send(content=msg_text, components = components )

@client.command()
@commands.guild_only()
@commands.has_permissions(manage_roles=True)
async def mass_create_roles(ctx, mentionable : bool, hoist : bool, *, role_names):
    role_names = role_names.split("\n")
    created_role_mentions = []
    for rn in role_names:
        new_role = await ctx.guild.create_role(name=rn,mentionable=mentionable, hoist=hoist)
        created_role_mentions.append(new_role.mention)
    await ctx.send (f"Created roles {' '.join(created_role_mentions)}")



@client.event
async def on_select_option(interaction):
    removed_mentions = []

    # remove prev role
    roleOptions = [comp.components[0].options for comp in interaction.message.components]
    roleOptions = list(chain(*roleOptions)) # flattern above list

    umbrella_options = [comp.components[0].placeholder for comp in interaction.message.components]

    userRolesIds = [role.id for role in interaction.user.roles]
    for roleOption in roleOptions:
        rid = int(roleOption.value)
        if rid in userRolesIds:
            role = interaction.guild.get_role(rid)
            try:
                await interaction.user.remove_roles(role)
                removed_mentions.append(role.mention)
            except Exception as e:
                print(e)

    for uo in umbrella_options:
        ur = discord.utils.get(interaction.guild.roles,name=uo)
        if ur.id in userRolesIds:
            try:
                await interaction.user.remove_roles(ur)
            except Exception as e:
                print(e)

    ur = discord.utils.get(interaction.guild.roles,name=interaction.component.placeholder)
    if ur != None:
        try:
            await interaction.user.add_roles(ur)
        except Exception as e:
            print(e)

    role = interaction.guild.get_role(int(interaction.values[0]))
    await interaction.user.add_roles(role)

    if len(removed_mentions) == 0:
        send_text =  f"Gave you the role {role.mention}."
    elif len(removed_mentions) == 1:
        send_text = f"Removed your role {' '.join(removed_mentions)}, gave you the role {role.mention}."
    else:
        send_text = f"Removed your roles {' '.join(removed_mentions)}, gave you the role {role.mention}."
    await interaction.send(send_text)





from dotenv import dotenv_values
config = dotenv_values(".env")
client.run(config["BOTKEY"])