import asyncio
import logging
import re

import aiocron
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from settings import Settings
from bot.snake_client import SnakeClient


PATTERN_SUBSCRIBE_VACANCIES = re.compile(r"subscribe_vacancies:(?P<result>\d)")
PATTERN_SUBSCRIBE_EVENTS = re.compile(r"subscribe_events:(?P<result>\d)")

logger = logging.getLogger(__name__)

config = Settings()

snake_client = None

is_game_run = False

players = {}

players_keyboards = [
    [{"4": "▲"}, {"5": "▼"}],
    [{"3": "◀︎"}, {"2": "▶︎"}],
    [{"8": "▲"}, {"9": "▼"}],
    [{"7": "◀︎"}, {"6": "▶︎"}],
]


def create_keyboard(commands) -> InlineKeyboardMarkup:
    keyboards = []
    for command in commands:
        key, value = list(command.items()).pop()

        keyboards.append(InlineKeyboardButton(value, callback_data=f"2:{key}"))

    return InlineKeyboardMarkup([keyboards])


async def coro_check_game_finish():
    while True:
        recv = snake_client.send("2:ping")

        if "finish" in recv:
            await game_over()
            break

        await asyncio.sleep(1)


def get_team_name():
    recv = snake_client.send("2:ping")

    if "1:T" in recv:
        return recv.split(":")[-1]

    return ""


@aiocron.crontab("* * * * * */1")
async def run_game():
    global is_game_run

    if len(players) < 4:
        return

    if is_game_run:
        return

    is_game_run = True

    snake_client.send("3:finish")
    snake_client.send("2:0")
    snake_client.send("2:1")

    for idx, player in enumerate(players.values()):
        if idx == 2:
            snake_client.send("2:1")

        snake_client.send(f"2:{player['update'].effective_user.username}")
        snake_client.send(f"2:{player['update'].effective_user.username}")

    snake_client.send("2:1")

    await asyncio.sleep(2)

    team1_name = get_team_name()
    team2_name = get_team_name()

    for idx, player in enumerate(players.values()):
        team_name = team1_name if idx < 2 else team2_name
        message_team = ""

        if team_name:
            message_team = f"🤺 Ты в команде '{team_name}'\n\n"

        message = await player["context"].bot.send_message(
            player["update"].effective_user.id,
            f"🐍 Игра началась!\n\n {message_team} Да победит сильнейший! 💪",
            reply_markup=create_keyboard(player["command"]),
        )

        player["keyboard_message_id"] = message.message_id

    asyncio.create_task(coro_check_game_finish())


async def callback_button_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if update.effective_user.id not in players:
        return

    if not is_game_run:
        return

    recv = snake_client.send(query.data)

    if "finish" in recv:
        await game_over()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id

    if telegram_user_id in players:
        await context.bot.send_message(
            telegram_user_id,
            "Вы уже присоединились к игре.\n"
            "Дождитесь, когда все команды будут сформированы или наберите /stop для выходы из игры.",
        )
        return

    if len(players) == 4:
        await context.bot.send_message(telegram_user_id, "Все места заняты 😔")
        return

    players[telegram_user_id] = {
        "command": players_keyboards[len(players)],
        "update": update,
        "context": context,
        "keyboard_message_id": None,
    }

    await context.bot.send_message(
        telegram_user_id,
        "Вы присоединились к игре.\n"
        "Дождитесь, когда все команды буду сформированы или наберите /stop для выходы из игры.",
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id

    if is_game_run:
        await game_over()
        return

    if telegram_user_id in players:
        del players[telegram_user_id]
        await context.bot.send_message(telegram_user_id, "Вы покинули игру")


async def game_over():
    global is_game_run, players

    if not is_game_run:
        return

    for player in players.values():
        await player["context"].bot.delete_message(
            player["update"].effective_user.id, player["keyboard_message_id"]
        )
        await player["context"].bot.send_message(
            player["update"].effective_user.id, "Game over 🏆"
        )
        await player["context"].bot.send_message(
            player["update"].effective_user.id,
            "Спасибо, что приняли участие в игре 😇\n\n",
        )

    snake_client.send("3:finish")
    players = {}
    is_game_run = False


def bot_run():
    global snake_client

    snake_client = SnakeClient(config.SOCKET_POINT, 2048)

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    application.add_handlers(
        [
            CommandHandler("start", start),
            CommandHandler("stop", stop),
            CallbackQueryHandler(callback_button_game, pattern=r"2:\d"),
        ]
    )

    application.run_polling()


if __name__ == "__main__":
    bot_run()
