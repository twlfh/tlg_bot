from aiogram import Bot, Dispatcher, types
from config import TOKEN
import asyncio
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class MenuStates(StatesGroup):
    MENU_1 = State()#Education
    MENU_2 = State()#Targeting
    MENU_3 = State()#Live Photo
    MENU_4 = State()#Cards
    MENU_5 = State()#
    MENU_6 = State()#


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Lets Go!')]
    ],
    resize_keyboard=True,
    one_time_keyboard = True
)
back_button = KeyboardButton(text='Back')
buy_now_button = KeyboardButton(text='Buy now')
confirm_button = KeyboardButton(text='Confirm')

actions_keyboard = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text='Education')],
        [KeyboardButton(text='Book a photo shot')],
        [KeyboardButton(text='Quit')]
    ],
    resize_keyboard=True
)
course_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Targeting')],
        [KeyboardButton(text='Live photo')],
        [back_button]
    ]
)
course_keyboard_action = ReplyKeyboardMarkup(
    keyboard=[
        [buy_now_button],
        [back_button]
    ],
    resize_keyboard=True
)
payment_methods = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Cards')],
        [KeyboardButton(text='Pay Pal')],
        [KeyboardButton(text='Crypto')],
        [back_button]
    ],
    resize_keyboard=True
)
confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [confirm_button],
        [back_button]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer('Press the button and le go',
                         reply_markup=start_keyboard)

@dp.message(lambda message: message.text == 'Lets Go!')
async def lets_go_button(message: types.Message):
    await message.answer('Choose your parameter',
                         reply_markup=actions_keyboard)

@dp.message(lambda message: message.text == 'Education')
async def learn_button(message: types.Message, state: FSMContext):
    await state.set_state(MenuStates.MENU_1)
    await message.answer('Choose your course',
                         reply_markup=course_keyboard)

@dp.message(lambda message: message.text == 'Targeting')
async def targeting_button(message: types.Message, state: FSMContext):
    await state.set_state(MenuStates.MENU_2)
    await message.answer('This course will teach you how to properly set up targeting as a photographer.\n'
                         'Choose yor payment method.',
                         reply_markup=payment_methods)

@dp.message(lambda message: message.text == 'Live photo')
async def live_photo_button(message: types.Message, state:FSMContext):
    await state.set_state(MenuStates.MENU_3)
    await message.answer('This course will teach you how to make a live photo.',
                         reply_markup=course_keyboard_action)

@dp.message(lambda message: message.text == 'Cards')
async def cards_payment_button(message: types.Message, state:FSMContext):
    await state.set_state(MenuStates.MENU_4)
    await message.answer('Your course: Targeting. Price: 100 euros. To continue, click Buy now.',
                         reply_markup=course_keyboard_action)

#@dp.message(lambda message: message.text == 'Confirm')
#async def live_photo_button(message: types.Message, state:FSMContext):
#    await state.set_state(MenuStates.MENU_3)
#    await message.answer('Your course: Targeting. Price: 100 euros. To confirm, click Buy now.',
#                         reply_markup=course_keyboard_action)

#@dp.message(lambda message: message.text == 'Confirm')
#async def confirm_button(message: types.Message, state:FSMContext):
    #current_state = await state.get_state()
    #if current_state == MenuStates.MENU_5

@dp.message(lambda message: message.text == 'Buy now')
async def buy_now_button(message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    if current_state == MenuStates.MENU_4:
        await message.answer('Please send the specified amount to this bank card:\n'
                             '\n 8888 8888 8888 8888.\n'
                             '\n'
                             'The payment will be processed within 10 minutes.\n'
                             '\n'
                             'After making the payment, please click the Confirm button.\n'
                             '\n'
                             'After that, you will receive a link to the course channel',
                             reply_markup=confirm_keyboard)

@dp.message(lambda message: message.text == 'Back')
async def back_button(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == MenuStates.MENU_1.state:
        await state.clear()
        await message.answer('Back to menu',reply_markup=actions_keyboard)
    elif current_state == MenuStates.MENU_2.state:
        await state.set_state(MenuStates.MENU_1)
        await message.answer('Back to courses',reply_markup=course_keyboard)
    elif current_state == MenuStates.MENU_3.state:
        await state.set_state(MenuStates.MENU_1)
        await message.answer('Back to courses',reply_markup=course_keyboard)
    elif current_state == MenuStates.MENU_4.state:
        await state.set_state(MenuStates.MENU_3)
        await message.answer('Back to payment methods', reply_markup=payment_methods)


@dp.message(lambda message: message.text == 'Quit')
async def quit_button(message: types.Message):
    await message.answer('See you later',
                         reply_markup=ReplyKeyboardRemove())

async def polling():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(polling())



