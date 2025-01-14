from django.urls import path

from .views import (
    MessengerListView,
    ProfileDetailView,
    ProfileListView,
    accept_invitation,
    my_friends_view,
    my_profile_view,
    received_invites_view,
    reject_invitation,
    remove_friend,
    search_profiles,
    send_invitation,
    sent_invites_view,
    show_profile_view,
    switch_follow,
    toggle_ban_view
)

app_name = "profiles"

urlpatterns = [
    path("", ProfileListView.as_view(), name="all-profiles-view"),
    path("show_profile/<int:id>/", show_profile_view, name="show-profile-view"),
    path("my_profile/", my_profile_view, name="my-profile-view"),
    path("toggle_ban/<int:profile_id>/", toggle_ban_view, name="toggle-ban-view"),
    path("users/<slug>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("messenger/", MessengerListView.as_view(), name="messenger-list-view"),
    path("search/", search_profiles, name="search-profiles-view"),
    path("my_friends/", my_friends_view, name="my-friends-view"),
    path("received_invites/", received_invites_view, name="received-invites-view"),
    path("sent_invites/", sent_invites_view, name="sent-invites-view"),
    path("switch_follow/", switch_follow, name="switch-follow-view"),
    path("send-invite/", send_invitation, name="send-invite"),
    path("remove-friend/", remove_friend, name="remove-friend"),
    path("received_invites/accept/", accept_invitation, name="accept-invite"),
    path("received_invites/reject/", reject_invitation, name="reject-invite"),
]
