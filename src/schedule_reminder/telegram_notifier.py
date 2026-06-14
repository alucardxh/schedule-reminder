from telegram import Bot


class TelegramNotifier:

    def __init__(
            self,
            token: str,
            chat_id: str | int,
    ) -> None:
        self._bot = Bot(token)
        self._chat_id = chat_id

    async def send_message(
            self,
            message: str,
    ) -> None:
        await self._bot.send_message(
            chat_id=self._chat_id,
            text=message,
        )