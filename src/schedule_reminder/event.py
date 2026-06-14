from datetime import date
from pydantic import BaseModel, TypeAdapter


# 继承 BaseModel 即可，不再需要 @dataclass 装饰器
class Event(BaseModel):
    title: str
    event_date: date
    description: str = ""

    model_config = {
        "extra": "forbid",  # 禁止传入未定义的额外字段，类似 slots 的安全约束
        "frozen": False,    # 如果希望像 frozen=True 一样不可变，可以设为 True
    }

    def days_left(self, today: date) -> int:
        return (self.event_date - today).days

    def build_reminder_message(self, today: date) -> str:
        """生成优雅的通知文本"""
        days = self.days_left(today)

        # 1. 算出中文的星期几
        # weekday() 返回 0~6（周一到周日）
        weekdays_map = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday_str = weekdays_map[self.event_date.weekday()]

        # 2. 算出人性化的“几天后”
        if days == 1:
            time_human = "明天"
        elif days == 2:
            time_human = "后天"
        elif days == 3:
            time_human = "大后天"
        else:
            time_human = f"{days}天后"

        # 3. 组装成优雅的形态
        # 格式：📅 提醒：后天（6月16日 星期二）有【游泳课】
        return (
            f"📅 提醒：{time_human}（{self.event_date.month}月{self.event_date.day}日 "
            f"{weekday_str}）有【{self.title}】"
        )

    @classmethod
    def load_from_file(cls, file_path: str) -> list["Event"]:
        """静态工厂方法：传入文件路径，直接返回 Event 对象列表"""
        with open(file_path, encoding="utf-8") as f:
            # 使用 Pydantic 的 TypeAdapter 批量反序列化
            return TypeAdapter(list[cls]).validate_json(f.read())