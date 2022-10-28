import os
import logging
# import getipinfo
import nlp_lr
# import public_ip as ip
from aiogram import Bot, Dispatcher, executor, types
import streamlit as st
# from config import TOKEN

import asyncio

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = st.secrets["TOKEN"]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    # text = f"Hello, {user_name},\nyou are from {getipinfo.get_info(ip.get())}\n"
    text = f"Hello, {user_name}!"
    logging.info(f"{user_name=} send message: {message.text}")
    print(text)
    st.write(text)
    await message.reply(text)

@dp.message_handler()
async def send_echo(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_id
    text = f"The comment is: {nlp_lr.common_func(message.text)}"
    logging.info(f"{user_name=} send message: {message.text}")    
    st.write(text)
    await bot.send_message(user_id, text)
    #await bot.send_message(admin_id, text)

# this part of code needed in Streamlit - whatever it's mean
def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()
asyncio.set_event_loop(st.session_state.loop)


if __name__ == '__main__':
    executor.start_polling(dp)
