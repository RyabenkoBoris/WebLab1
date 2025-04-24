from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Chat, Message, User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task(queue='email_queue')
def send_email_to_chat_users(chat_id, message, user_id):
    chat = Chat.objects.get(id=chat_id)
    channel_layer = get_channel_layer()
    # Get all users in chat except user who wrote message.
    users_to_notify = chat.users.exclude(id=user_id)

    email_subject = f"New message in chat: {chat.name}"
    email_body = f"Hello,\n\nYou have a new message in the chat '{chat.name}': {message}\n"
    email_addresses = [user.email for user in users_to_notify if user.email]
    data = ["Відправка повідомлення користувачам чату", f"Chat ID: {chat_id}, User ID: {user_id}, Message: {message[:50]}..."]
    try:
        send_mail(email_subject, email_body, 'no-reply@testdomain.com', email_addresses)
        result = f"Було успішно відправлено {len(email_addresses)} EMAIL повідомлень з чату {chat.name}"
        data.append(result)
        async_to_sync(channel_layer.group_send)(
            "admin_updates",
            {
                "type": "send_operation_status",
                "data": data,
            }
        )
        return result
    except Exception as e:
        error_message = f"Помилка при відправці email: {str(e)}"
        data.append(error_message)
        async_to_sync(channel_layer.group_send)(
            "admin_updates",
            {
                "type": "send_operation_status",
                "data": data,
            }
        )

        return error_message

@shared_task(queue='chat_queue')
def add_user_to_chat_task(chat_id, user_id):
    channel_layer = get_channel_layer()
    data = ["Додавання користувача до чату", f"Chat ID: {chat_id}, User ID: {user_id}"]
    try:
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)

        if user in chat.users.all():
            result = f"Користувач {user.username} вже є в чаті."
        else:
            chat.users.add(user)
            Message.objects.create(
                chat=chat,
                text=f"Користувач {user.username} доданий до чату.",
                timestamp=timezone.now()
            )
            result = f"Користувач {user.username} доданий до чату."

        data.append(result)

        async_to_sync(channel_layer.group_send)(
            "admin_updates",
            {
                "type": "send_operation_status",
                "data": data,
            }
        )
        return result

    except Exception as e:
        error_message = f"Помилка: {str(e)}"
        data.append(error_message)
        async_to_sync(channel_layer.group_send)(
            "admin_updates",
            {
                "type": "send_operation_status",
                "data": data,
            }
        )
        return error_message