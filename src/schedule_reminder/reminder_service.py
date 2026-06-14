import asyncio
from datetime import date
from schedule_reminder.event import Event
from schedule_reminder.telegram_notifier import TelegramNotifier


class ReminderService:

    def __init__(self, notifier: TelegramNotifier) -> None:
        # 通过构造函数注入你的 Telegram 通知组件
        self._notifier = notifier

    def find_events_to_remind(self, events: list[Event], today: date) -> list[Event]:
        """过滤出 1-3 天内发生的事件"""
        return [e for e in events if 1 <= e.days_left(today) <= 3]

    async def execute_daily_reminders(self, events: list[Event], today: date) -> None:
        """核心业务流：找出事件 -> 批量并发发送 Telegram 通知"""
        # 1. 过滤事件
        target_events = self.find_events_to_remind(events, today)

        if not target_events:
            print(f"[{today}] 没有需要提醒的事件。")
            return

        # 2. 为每个事件生成消息，并创建对应的发送协程任务 (Task)
        tasks = [
            self._notifier.send_message(event.build_reminder_message(today))
            for event in target_events
        ]

        # 3. 使用 gather 并发执行所有发送任务，速度飞快
        await asyncio.gather(*tasks)
        print(f"[{today}] 成功并发推送了 {len(target_events)} 条提醒消息！")