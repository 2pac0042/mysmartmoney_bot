import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from locales import LOCALES

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_lang = {}

@dp.message_handler(commands=['start'])
async def cmd_start(m: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🇷🇺 Русский", "🇺🇿 O‘zbekcha")
    await m.answer(LOCALES['ru']['choose_language'], reply_markup=kb)

@dp.message_handler(lambda m: m.text in ["🇷🇺 Русский", "🇺🇿 O‘zbekcha"])
async def set_lang(m: types.Message):
    lang = 'ru' if 'Рус' in m.text else 'uz'
    user_lang[m.from_user.id] = lang
    text = LOCALES[lang]['welcome']
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(LOCALES[lang]['indicators'], LOCALES[lang]['courses'])
    kb.add(LOCALES[lang]['strategies'], LOCALES[lang]['subscribe'])
    kb.add(LOCALES[lang]['support'])
    await m.answer(f"{text}\n\n{LOCALES[lang]['menu']}", reply_markup=kb)

@dp.message_handler(lambda m: m.from_user.id in user_lang)
async def menu(m: types.Message):
    lang = user_lang[m.from_user.id]
    if m.text in [LOCALES[lang][k] for k in ['indicators','courses','strategies','subscribe']]:
        await m.answer(LOCALES[lang]['coming_soon'])
    elif m.text == LOCALES[lang]['support']:
        await m.answer("✉️ Здесь будет контакт поддержки.")
    else:
        await m.answer(LOCALES[lang]['menu'])

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
