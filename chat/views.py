from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Chat, Message, User
from .serializers import ChatSerializer, MessageSerializer, AddUserToChatSerializer, AppInfoSerializer
from django.utils import timezone
from rest_framework.views import APIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema

class AppInfoView(APIView):
    serializer_class = AppInfoSerializer
    permission_classes = [AllowAny]
    def get(self, _):
        data = {
            "name": "Chat App",
            "description": "Це простий чат, у якому можна створювати групи для спілкування та обмінюватися "
                           "повідомленнями. Користувачі можуть приєднуватися до групових чатів, "
                           "надсилати текстові повідомлення та переглядати історію розмов.",
            "logo": "💬"
        }
        return Response(data)

@extend_schema_view(
    get=extend_schema(operation_id="chat_list"),
    post=extend_schema(operation_id="chat_create")
)
class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(users=self.request.user) | Chat.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        chat = serializer.save(creator=self.request.user)
        Message.objects.create(
            chat=chat,
            text=f"Чат '{chat.name}' був створений.",
            timestamp=timezone.now()
        )

class ChatDeleteView(generics.DestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(creator=self.request.user)

@extend_schema_view(
    get=extend_schema(operation_id="chat_detail")
)
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs["chat_id"]
        chat = get_object_or_404(Chat, Q(users=self.request.user) | Q(creator=self.request.user), id=chat_id)
        return Message.objects.filter(chat=chat)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, Q(users=self.request.user) | Q(creator=self.request.user),
                                 id=self.request.data.get("chat"))
        serializer.save(user=self.request.user, chat=chat)

class AddUserToChatView(generics.UpdateAPIView):
    serializer_class = AddUserToChatSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, id=self.kwargs["chat_id"])

        if request.user != chat.creator:
            return Response({"detail": "Ви не є адміном цього чату."}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if user in chat.users.all():
            return Response({"detail": f"Користувач {user.username} вже є в чаті."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            user = get_object_or_404(User, id=user_id)
            chat.users.add(user)
            Message.objects.create(
                chat=chat,
                text=f"Користувач {user.username} доданий до чату.",
                timestamp=timezone.now()
            )

            return Response({"detail": f"Користувач {user.username} доданий до чату."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)