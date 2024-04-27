# commands/new_member_handler.py

from pyrogram.types import ChatPermissions

# Define the handler for new member join events
def new_member_join(client, message):
    for member in message.new_chat_members:
        # Check if the new member is the bot itself, if so, skip
        if member.id == client.get_me().id:
            continue
        # Automatically approve the new member
        client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=member.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )
