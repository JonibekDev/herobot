import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'YOUR_API_TOKEN'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Hello {message.from_user.full_name}. It is HeroBot. Just send your favourite hero's name")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("This bot can help you to find information about heroes of Marvel/DC.\nSend message like "
                        "Ironman, Thor, Captain America")


@dp.message_handler()
async def sendHero(message: types.Message):
    hero = message.text
    url = "https://superheroapi.com/api/114330201294707/search/" + hero
    r = requests.get(url)
    res = r.json()

    if res['response'] == 'success':
        uzunlik = len(res['results'])
        for i in range(uzunlik):
            intelligence = res['results'][i]['powerstats']['intelligence']
            strength = res['results'][i]['powerstats']['strength']
            speed = res['results'][i]['powerstats']['speed']
            durability = res['results'][i]['powerstats']['durability']
            power = res['results'][i]['powerstats']['power']
            combat = res['results'][i]['powerstats']['combat']

            fullName = res['results'][i]['biography']['full-name']
            placeOfBirth = res['results'][i]['biography']['place-of-birth']
            gender = res['results'][i]['appearance']['gender']
            race = res['results'][i]['appearance']['race']
            height = res['results'][i]['appearance']['height'][1]
            weight = res['results'][i]['appearance']['weight'][1]
            img = res['results'][i]['image']['url']
            media = types.MediaGroup()
            media.attach_photo(f'{img}', f"Name: {fullName}\nRace: {race}\nGender: {gender}\nPlace of Birth: {placeOfBirth}\nHeight: {height}\nWeight: {weight}\n"
                f"Strength: {strength}\nSpeed: {speed}\nIntelligence: {intelligence}\nDurability: {durability}\nPower: {power}\nCombat: {combat}")

            await message.answer_media_group(media=media)
    else:
        await message.reply("I can't find hero. Please check name again.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
