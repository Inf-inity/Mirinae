from discord import (
    AutoModAction,
    Guild,
    Invite,
    Member,
    Message,
    RawBulkMessageDeleteEvent,
    RawMemberRemoveEvent,
    RawMessageDeleteEvent,
    RawMessageUpdateEvent
)
from discord.utils import utcnow

from library.cog import Cog
from library.contributor import Contributor
from library.database import Point, cache


class EventCog(Cog):
    CONTRIBUTORS = [Contributor.Infinity]

    @Cog.listener()
    async def on_automod_action(self, execution: AutoModAction):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_automod_action", 1
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
                "events"
            ).field(
                "on_guild_available", 1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_unavailable(self, guild: Guild):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_guild_available", -1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_guild_join", 1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_guild_join", -1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_invite_create(self, invite: Invite):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_invite_create", 1
            ).tag(
                "guild_id", invite.guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_invite_create", -1
            ).tag(
                "guild_id", invite.guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_join(self, member: Member):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_member_join", 1
            ).tag(
                "guild_id", member.guild.id
            ).tag(
                "bot", member.bot
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_member_join", -1
            ).tag(
                "guild_id", member.guild.id
            ).tag(
                "bot", member.bot
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_member_join", -1
            ).tag(
                "guild_id", payload.guild_id
            ).tag(
                "bot", payload.user.bot
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_ban(self, guild: Guild, _: Member):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_member_ban", 1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_member_unban(self, guild: Guild, _: Member):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_member_ban", -1
            ).tag(
                "guild_id", guild.id
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_message(self, message: Message):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_message", 1
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
                "events"
            ).field(
                "on_message_edit", 1
            ).tag(
                "guild_id", before.guild.id
            ).tag(
                "bot", str(before.author.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_raw_message_edit(self, payload: RawMessageUpdateEvent):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_message_edit", 1
            ).tag(
                "guild_id", payload.guild_id
            ).tag(
                "bot", str(None)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_message", -1
            ).tag(
                "guild_id", message.guild.id
            ).tag(
                "bot", str(message.author.bot)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent):
        cache.point_cache.append(
            Point(
                "events"
            ).field(
                "on_message", -1
            ).tag(
                "guild_id", payload.guild_id
            ).tag(
                "bot", str(None)
            ).time(utcnow())
        )

    @Cog.listener()
    async def on_bulk_message_delete(self, messages: list[Message]):
        for i in range(len(messages)):
            cache.point_cache.append(
                Point(
                    "events"
                ).field(
                    "on_message", -1
                ).tag(
                    "guild_id", messages[i].guild.id
                ).tag(
                    "bot", str(messages[i].author.bot)
                ).time(utcnow())
            )

    @Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: RawBulkMessageDeleteEvent):
        for _ in range(len(payload.message_ids)):
            cache.point_cache.append(
                Point(
                    "events"
                ).field(
                    "on_message", -1
                ).tag(
                    "guild_id", payload.guild_id
                ).tag(
                    "bot", str(None)
                ).time(utcnow())
            )
