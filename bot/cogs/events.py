from discord import (
    AutoModAction,
    Guild,
    Invite,
    Member,
    Message,
    RawMemberRemoveEvent,
)
from discord.utils import utcnow

from library.cog import Cog
from library.contributor import Contributor
from library.database import Fields, Measurements, Point, cache


class EventCog(Cog):
    CONTRIBUTORS = [Contributor.Infinity]

    @Cog.listener()
    async def on_automod_action(self, execution: AutoModAction):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_auto_mod_action.name, 1
            ).tag(
                "guild_id", execution.guild_id
            ).tag(
                "type", execution.action.type.name
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_available(self, guild: Guild):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_guild_available.name, 1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_unavailable(self, guild: Guild):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_guild_available.name, -1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_guild_join.name, 1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_guild_remove.name, 1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_invite_create(self, invite: Invite):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_invite_create.name, 1
            ).tag(
                "guild_id", invite.guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_invite_create.name, -1
            ).tag(
                "guild_id", invite.guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_join(self, member: Member):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_member_join.name, 1
            ).tag(
                "guild_id", member.guild.id
            ).tag(
                "bot", str(member.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_member_remove.name, 1
            ).tag(
                "guild_id", member.guild.id
            ).tag(
                "bot", str(member.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_member_remove.name, 1
            ).tag(
                "guild_id", payload.guild_id
            ).tag(
                "bot", str(payload.user.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_ban(self, guild: Guild, member: Member):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_member_ban.name, 1
            ).tag(
                "guild_id", guild.id
            ).tag(
                "bot", str(member.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_unban(self, guild: Guild, member: Member):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_member_unban.name, 1
            ).tag(
                "guild_id", guild.id
            ).tag(
                "bot", str(member.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_message(self, message: Message):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_message.name, 1
            ).tag(
                "guild_id", message.guild.id
            ).tag(
                "bot", str(message.author.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_message_edit(self, before: Message, _: Message):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_message_edit.name, 1
            ).tag(
                "guild_id", before.guild.id
            ).tag(
                "bot", str(before.author.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        cache.point_cache.append(
            Point(
                Measurements.events.name
            ).field(
                Fields.on_message_delete.name, 1
            ).tag(
                "guild_id", message.guild.id
            ).tag(
                "bot", str(message.author.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_bulk_message_delete(self, messages: list[Message]):
        for i in range(len(messages)):
            cache.point_cache.append(
                Point(
                    Measurements.events.name
                ).field(
                    Fields.on_message_delete.name, 1
                ).tag(
                    "guild_id", messages[i].guild.id
                ).tag(
                    "bot", str(messages[i].author.bot)
                ).time(utcnow())
            )
