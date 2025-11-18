import asyncio
import random
import config
from datetime import datetime
from typing import Dict, Tuple
from aiogram import Bot, Dispatcher
from aiogram.types import (
    ChatJoinRequest,
    PollAnswer
)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

pending_requests: Dict[int, Dict] = {}
timers: Dict[int, asyncio.Task] = {}


def generate_captcha() -> Tuple[str, int, list]:
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    correct_answer = a + b
    question = f"{a} + {b}"
    
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong = random.randint(1, 40)
        if wrong != correct_answer and wrong not in wrong_answers:
            wrong_answers.append(wrong)
    
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)
    correct_index = all_answers.index(correct_answer)
    
    return question, correct_index, all_answers


async def send_captcha_poll(user_id: int, chat_id: int):
    question, correct_index, answers = generate_captcha()
    
    try:
        poll = await bot.send_poll(
            chat_id=user_id,
            question=question,
            options=[str(ans) for ans in answers],
            is_anonymous=False,
            open_period=600
        )
        
        pending_requests[user_id] = {
            "chat_id": chat_id,
            "poll_id": poll.poll.id,
            "correct_index": correct_index,
            "timestamp": datetime.now(),
            "answered": False
        }
        
        timer_task = asyncio.create_task(handle_timeout(user_id))
        timers[user_id] = timer_task
        
    except Exception:
        await bot.decline_chat_join_request(chat_id=chat_id, user_id=user_id)


async def handle_timeout(user_id: int):
    await asyncio.sleep(600)
    
    if user_id in pending_requests and not pending_requests[user_id]["answered"]:
        request_data = pending_requests[user_id]
        try:
            await bot.decline_chat_join_request(
                chat_id=request_data["chat_id"],
                user_id=user_id
            )
        except:
            pass
        
        if user_id in pending_requests:
            del pending_requests[user_id]
        if user_id in timers:
            timers[user_id].cancel()
            del timers[user_id]


@dp.chat_join_request()
async def handle_join_request(event: ChatJoinRequest):
    user_id = event.from_user.id
    chat_id = event.chat.id
    
    await send_captcha_poll(user_id, chat_id)


@dp.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id
    
    if user_id not in pending_requests:
        return
    
    request_data = pending_requests[user_id]
    
    if request_data["poll_id"] != poll_id:
        return
    
    if request_data["answered"]:
        return
    
    request_data["answered"] = True
    
    if user_id in timers:
        timers[user_id].cancel()
        del timers[user_id]
    
    selected_option = poll_answer.option_ids[0] if poll_answer.option_ids else None
    correct_index = request_data["correct_index"]
    
    try:
        if selected_option == correct_index:
            await bot.approve_chat_join_request(
                chat_id=request_data["chat_id"],
                user_id=user_id
            )
        else:
            await bot.decline_chat_join_request(
                chat_id=request_data["chat_id"],
                user_id=user_id
            )
    except:
        pass
    
    if user_id in pending_requests:
        del pending_requests[user_id]


async def main():
    await dp.start_polling(bot)

print("Bot started")

if __name__ == "__main__":
    asyncio.run(main())

