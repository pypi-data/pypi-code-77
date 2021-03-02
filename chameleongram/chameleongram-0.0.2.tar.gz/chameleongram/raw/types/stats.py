from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class BroadcastStats(TL):
    ID = 0xbdf78394

    def __init__(cls, period: TL, followers: TL, views_per_post: TL, shares_per_post: TL, enabled_notifications: TL, growth_graph: TL, followers_graph: TL, mute_graph: TL, top_hours_graph: TL, interactions_graph: TL, iv_interactions_graph: TL, views_by_source_graph: TL, new_followers_by_source_graph: TL, languages_graph: TL, recent_message_interactions: List[TL]):
        cls.period = period
        cls.followers = followers
        cls.views_per_post = views_per_post
        cls.shares_per_post = shares_per_post
        cls.enabled_notifications = enabled_notifications
        cls.growth_graph = growth_graph
        cls.followers_graph = followers_graph
        cls.mute_graph = mute_graph
        cls.top_hours_graph = top_hours_graph
        cls.interactions_graph = interactions_graph
        cls.iv_interactions_graph = iv_interactions_graph
        cls.views_by_source_graph = views_by_source_graph
        cls.new_followers_by_source_graph = new_followers_by_source_graph
        cls.languages_graph = languages_graph
        cls.recent_message_interactions = recent_message_interactions

    @staticmethod
    def read(data) -> "BroadcastStats":
        period = data.getobj()
        followers = data.getobj()
        views_per_post = data.getobj()
        shares_per_post = data.getobj()
        enabled_notifications = data.getobj()
        growth_graph = data.getobj()
        followers_graph = data.getobj()
        mute_graph = data.getobj()
        top_hours_graph = data.getobj()
        interactions_graph = data.getobj()
        iv_interactions_graph = data.getobj()
        views_by_source_graph = data.getobj()
        new_followers_by_source_graph = data.getobj()
        languages_graph = data.getobj()
        recent_message_interactions = data.getobj()
        return BroadcastStats(period=period, followers=followers, views_per_post=views_per_post, shares_per_post=shares_per_post, enabled_notifications=enabled_notifications, growth_graph=growth_graph, followers_graph=followers_graph, mute_graph=mute_graph, top_hours_graph=top_hours_graph, interactions_graph=interactions_graph, iv_interactions_graph=iv_interactions_graph, views_by_source_graph=views_by_source_graph, new_followers_by_source_graph=new_followers_by_source_graph, languages_graph=languages_graph, recent_message_interactions=recent_message_interactions)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.period.getvalue())
        data.write(cls.followers.getvalue())
        data.write(cls.views_per_post.getvalue())
        data.write(cls.shares_per_post.getvalue())
        data.write(cls.enabled_notifications.getvalue())
        data.write(cls.growth_graph.getvalue())
        data.write(cls.followers_graph.getvalue())
        data.write(cls.mute_graph.getvalue())
        data.write(cls.top_hours_graph.getvalue())
        data.write(cls.interactions_graph.getvalue())
        data.write(cls.iv_interactions_graph.getvalue())
        data.write(cls.views_by_source_graph.getvalue())
        data.write(cls.new_followers_by_source_graph.getvalue())
        data.write(cls.languages_graph.getvalue())
        data.write(Vector().getvalue(cls.recent_message_interactions))
        return data.getvalue()


class MegagroupStats(TL):
    ID = 0xef7ff916

    def __init__(cls, period: TL, members: TL, messages: TL, viewers: TL, posters: TL, growth_graph: TL, members_graph: TL, new_members_by_source_graph: TL, languages_graph: TL, messages_graph: TL, actions_graph: TL, top_hours_graph: TL, weekdays_graph: TL, top_posters: List[TL], top_admins: List[TL], top_inviters: List[TL], users: List[TL]):
        cls.period = period
        cls.members = members
        cls.messages = messages
        cls.viewers = viewers
        cls.posters = posters
        cls.growth_graph = growth_graph
        cls.members_graph = members_graph
        cls.new_members_by_source_graph = new_members_by_source_graph
        cls.languages_graph = languages_graph
        cls.messages_graph = messages_graph
        cls.actions_graph = actions_graph
        cls.top_hours_graph = top_hours_graph
        cls.weekdays_graph = weekdays_graph
        cls.top_posters = top_posters
        cls.top_admins = top_admins
        cls.top_inviters = top_inviters
        cls.users = users

    @staticmethod
    def read(data) -> "MegagroupStats":
        period = data.getobj()
        members = data.getobj()
        messages = data.getobj()
        viewers = data.getobj()
        posters = data.getobj()
        growth_graph = data.getobj()
        members_graph = data.getobj()
        new_members_by_source_graph = data.getobj()
        languages_graph = data.getobj()
        messages_graph = data.getobj()
        actions_graph = data.getobj()
        top_hours_graph = data.getobj()
        weekdays_graph = data.getobj()
        top_posters = data.getobj()
        top_admins = data.getobj()
        top_inviters = data.getobj()
        users = data.getobj()
        return MegagroupStats(period=period, members=members, messages=messages, viewers=viewers, posters=posters, growth_graph=growth_graph, members_graph=members_graph, new_members_by_source_graph=new_members_by_source_graph, languages_graph=languages_graph, messages_graph=messages_graph, actions_graph=actions_graph, top_hours_graph=top_hours_graph, weekdays_graph=weekdays_graph, top_posters=top_posters, top_admins=top_admins, top_inviters=top_inviters, users=users)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.period.getvalue())
        data.write(cls.members.getvalue())
        data.write(cls.messages.getvalue())
        data.write(cls.viewers.getvalue())
        data.write(cls.posters.getvalue())
        data.write(cls.growth_graph.getvalue())
        data.write(cls.members_graph.getvalue())
        data.write(cls.new_members_by_source_graph.getvalue())
        data.write(cls.languages_graph.getvalue())
        data.write(cls.messages_graph.getvalue())
        data.write(cls.actions_graph.getvalue())
        data.write(cls.top_hours_graph.getvalue())
        data.write(cls.weekdays_graph.getvalue())
        data.write(Vector().getvalue(cls.top_posters))
        data.write(Vector().getvalue(cls.top_admins))
        data.write(Vector().getvalue(cls.top_inviters))
        data.write(Vector().getvalue(cls.users))
        return data.getvalue()


class MessageStats(TL):
    ID = 0x8999f295

    def __init__(cls, views_graph: TL):
        cls.views_graph = views_graph

    @staticmethod
    def read(data) -> "MessageStats":
        views_graph = data.getobj()
        return MessageStats(views_graph=views_graph)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(cls.views_graph.getvalue())
        return data.getvalue()
