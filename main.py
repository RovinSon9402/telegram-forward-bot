import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# 로깅 설정
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 봇 토큰 및 대상 채널/그룹 ID 설정
BOT_TOKEN = "8589917276:AAHc9Gr-CoGPwRXLyuMtTcXlQSdx1Ut_4rU"
TARGET_CHATS = ["@remaist00", "@zionist"]

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """받은 메시지를 지정된 채널/그룹으로 전달합니다."""
    message = update.effective_message
    if not message: # 메시지가 없는 경우 (예: 채널 업데이트 등) 처리하지 않음
        return

    logger.info(f"메시지 수신: {message.chat.id} ({message.chat.username or message.chat.title}) - {message.text or message.caption or message.effective_attachment}")

    for chat_id in TARGET_CHATS:
        try:
            if message.text:
                await context.bot.send_message(chat_id=chat_id, text=message.text)
            elif message.photo:
                # 가장 큰 해상도의 사진을 선택
                photo_file_id = message.photo[-1].file_id
                caption = message.caption if message.caption else None
                await context.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=caption)
            elif message.video:
                video_file_id = message.video.file_id
                caption = message.caption if message.caption else None
                await context.bot.send_video(chat_id=chat_id, video=video_file_id, caption=caption)
            elif message.document:
                document_file_id = message.document.file_id
                caption = message.caption if message.caption else None
                await context.bot.send_document(chat_id=chat_id, document=document_file_id, caption=caption)
            elif message.audio:
                audio_file_id = message.audio.file_id
                caption = message.caption if message.caption else None
                await context.bot.send_audio(chat_id=chat_id, audio=audio_file_id, caption=caption)
            elif message.voice:
                voice_file_id = message.voice.file_id
                caption = message.caption if message.caption else None
                await context.bot.send_voice(chat_id=chat_id, voice=voice_file_id, caption=caption)
            elif message.animation:
                animation_file_id = message.animation.file_id
                caption = message.caption if message.caption else None
                await context.bot.send_animation(chat_id=chat_id, animation=animation_file_id, caption=caption)
            elif message.sticker:
                sticker_file_id = message.sticker.file_id
                await context.bot.send_sticker(chat_id=chat_id, sticker=sticker_file_id)
            elif message.poll:
                # Poll은 직접 전달하는 API가 없으므로, 메시지 텍스트로 정보를 전달하거나, 별도 처리 필요
                # 여기서는 간단히 무시하거나, 텍스트로 변환하여 전달하는 것을 고려할 수 있습니다.
                logger.warning(f"Poll 메시지는 직접 전달할 수 없습니다. chat_id: {chat_id}")
            elif message.location:
                await context.bot.send_location(chat_id=chat_id, latitude=message.location.latitude, longitude=message.location.longitude)
            elif message.contact:
                await context.bot.send_contact(chat_id=chat_id, phone_number=message.contact.phone_number, first_name=message.contact.first_name, last_name=message.contact.last_name)
            else:
                logger.warning(f"지원되지 않는 메시지 타입입니다: {message}. chat_id: {chat_id}")
            logger.info(f"메시지 성공적으로 전달: {chat_id}")
        except Exception as e:
            logger.error(f"메시지 전달 실패 (chat_id: {chat_id}): {e}")

def main() -> None:
    """봇을 시작합니다."""
    application = Application.builder().token(BOT_TOKEN).build()

    # 모든 메시지 타입을 처리하는 핸들러 추가
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_message))

    # 봇 시작
    logger.info("봇 시작...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
