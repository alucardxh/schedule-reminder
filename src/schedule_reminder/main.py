import asyncio
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from schedule_reminder.event import Event
from schedule_reminder.reminder_service import ReminderService
from schedule_reminder.telegram_notifier import TelegramNotifier
import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

# 显式断言：告诉类型检查器，这两个变量绝对不能为 None
assert TG_TOKEN is not None, "错误：环境变量 TG_TOKEN 未配置！"
assert TG_CHAT_ID is not None, "错误：环境变量 TG_CHAT_ID 未配置！"


NOTIFIER = TelegramNotifier(token=TG_TOKEN, chat_id=TG_CHAT_ID)
REMINDER_SERVICE = ReminderService(notifier=NOTIFIER)


async def send_reminder_job():
    """定时任务触发时：只加载动态的数据，复用已经创建好的服务"""
    print(f"⏰ 定时任务触发...")
    events = Event.load_from_file("data/events.json")
    await REMINDER_SERVICE.execute_daily_reminders(events, date.today())


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder_job, trigger='cron', hour=20, minute=0)
    #scheduler.add_job(send_reminder_job, trigger='interval', minutes=5)
    scheduler.start()

    print("🚀 定时提醒服务已启动，Notifier 和 Service 已经就绪...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())