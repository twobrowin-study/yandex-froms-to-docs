import io
import os
from zipfile import ZIP_DEFLATED, ZipFile

from telebot import TeleBot

TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_GROUP_ID = os.environ["TG_GROUP_ID"]


def TgSendDocuments(issue: dict, documents: dict):
    """
    Высылает документы в телеграм группу
    """
    bot = TeleBot(TG_BOT_TOKEN)
    archive_buf = io.BytesIO()
    with ZipFile(archive_buf, "a", ZIP_DEFLATED, False) as archive:
        for filename, document in documents.items():
            archive.writestr(filename, document)
    archive_buf.seek(0)
    archive_bytes = archive_buf.read()
    bot.send_document(
        TG_GROUP_ID,
        archive_bytes,
        visible_file_name=issue["tg_archive_name"],
        caption=issue["tg_caption_md"],
        parse_mode="markdown",
    )
