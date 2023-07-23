from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from config import API_ID, API_HASH, SESSION, CHANNELS


client = TelegramClient(SESSION, API_ID, API_HASH)


async def dump_all_messages(channels):
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 100   # максимальное число записей, передаваемых за один раз

    all_messages = []   # список всех сообщений
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    for channel in channels:
        while True:
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break

            messages = history.messages

            for message in messages:
                all_messages.append(message.message)
            offset_msg = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        with open(f'{channel.split("/")[-1]}.txt', 'w', encoding='utf8') as outfile:
            for message in all_messages:
                outfile.write(message + '\n')


async def main():
    await dump_all_messages(channels=CHANNELS)


if __name__ == '__main__':
    print("Program is running...")
    client.start()
    client.loop.run_until_complete(main())

