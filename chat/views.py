from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from .models import Chat, Message, User
from .serializers import ChatSerializer, MessageSerializer,  AddUserToChatSerializer, AppInfoSerializer
from rest_framework.views import APIView


class AppInfoView(APIView):
    serializer_class = AppInfoSerializer
    permission_classes = [AllowAny]
    def get(self, _):
        print("⚠️ AppInfoView.get() was called")
        data = {
            "name": "Chat App",
            "description": "Це простий чат, у якому можна створювати групи для спілкування та обмінюватися "
                           "повідомленнями. Користувачі можуть приєднуватися до групових чатів, "
                           "надсилати текстові повідомлення та переглядати історію розмов.",
            "logo": "💬"
        }
        return Response(data)

class ChatViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(Q(users=self.request.user) | Q(creator=self.request.user)).distinct()

    @extend_schema(operation_id="chat_list", responses=ChatSerializer(many=True))
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(operation_id="chat_create", request=ChatSerializer, responses=ChatSerializer)
    def create(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save(creator=request.user)
            Message.objects.create(
                chat=chat,
                text=f"Чат '{chat.name}' був створений.",
                timestamp=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        chat = get_object_or_404(Chat, id=pk, creator=request.user)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(operation_id="add_user_to_chat", request=AddUserToChatSerializer)
    @action(detail=True, methods=["post"], url_path="add-user", url_name="add_user")
    def add_user(self, request, pk=None):
        chat = get_object_or_404(Chat, id=pk)
        if request.user != chat.creator:
            return Response({"detail": "Ви не є адміном цього чату."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AddUserToChatSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            user = get_object_or_404(User, id=user_id)
            if user in chat.users.all():
                return Response({"detail": f"Користувач {user.username} вже є в чаті."}, status=status.HTTP_400_BAD_REQUEST)

            chat.users.add(user)
            Message.objects.create(
                chat=chat,
                text=f"Користувач {user.username} доданий до чату.",
                timestamp=timezone.now()
            )
            return Response({"detail": f"Користувач {user.username} доданий до чату."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="chat_detail")
    @action(detail=False, methods=["get"], url_path=r'(?P<chat_id>\d+)', url_name="by_chat")
    def by_chat(self, request, chat_id=None):
        chat = get_object_or_404(Chat, Q(users=request.user) | Q(creator=request.user), id=chat_id)
        messages = Message.objects.filter(chat=chat)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @extend_schema(request=MessageSerializer, responses=MessageSerializer)
    def create(self, request):
        chat = get_object_or_404(Chat, Q(users=request.user) | Q(creator=request.user), id=request.data.get("chat"))
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, chat=chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

