from django.urls import path
from .views import (ChatListCreateView, ChatDeleteView, MessageListView,
                    MessageCreateView, AppInfoView, AddUserToChatView)

urlpatterns = [
    path("", ChatListCreateView.as_view(), name="chat-list-create"),
    path("<int:pk>/delete/", ChatDeleteView.as_view(), name="chat-delete"),
    path("<int:chat_id>/", MessageListView.as_view(), name="chat-messages"),
    path("<int:chat_id>/join_user/", AddUserToChatView.as_view(), name="add-user-to-chat"),
    path("message/", MessageCreateView.as_view(), name="message-create"),
    path("about/", AppInfoView.as_view(), name="about"),
]
