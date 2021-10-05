import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption

client = ComponentsBot(command_prefix = "drb$")

@client.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def dropdown(ctx, msg_text, placeholder_text, channel : discord.TextChannel, roles : commands.Greedy[discord.Role]):
    options = []
    for role in roles:
        options.append(SelectOption(label = role.name, value= role.id))
    msg = await channel.send(content=msg_text, components = [Select(placeholder = placeholder_text, options=options)] )

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
    roleOptions = interaction.message.components[0].components[0].options
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