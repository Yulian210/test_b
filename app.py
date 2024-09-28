import os

from flask.cli import load_dotenv
from telebot.types import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()


def get_phone_numbers():
    if os.path.exists("contacts.txt"):
        with open("contacts.txt", "r") as file:
            numbers = file.readlines()
        return [number.strip() for number in numbers]
    else:
        return []


async def show_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    numbers = get_phone_numbers()
    if numbers:
        response = "\n".join(numbers)
    else:
        response = "The list of phone numbers is empty."

    await update.message.reply_text(response)


async def add_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_number = " ".join(context.args)
    if new_number:
        with open("contacts.txt", "a") as file:
            file.write(f"{new_number}\n")
        await update.message.reply_text(f"number {new_number} added.")
    else:
        await update.message.reply_text("Please enter the number after the /add command")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I am a bot for working with phone numbers. Use the /add and /show commands")


def main():
    TOKEN = os.getenv('BOT_TOKEN')

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("show", show_numbers))
    app.add_handler(CommandHandler("add", add_number))

    app.run_polling()


if __name__ == "__main__":
    main()