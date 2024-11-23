from nonebot import get_driver
from nonebot.adapters import Bot
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from datetime import datetime, timedelta, time, date
from pathlib import Path
import json
from typing import Set, Dict

bot: Bot | None = None
driver = get_driver()
config = driver.config

group_id = config.group_id


@driver.on_bot_connect
async def global_bot(_bot: Bot):
    logger.success(f"机器人连接成功，id为{_bot.self_id}")


timetable: Dict[date, object] = dict()  # datetime格式
early_days: Set[date] = set()  # 早八日

meta_time = [
    time(hour=8, minute=20),  # 早八
    time(hour=10, minute=20),
    time(hour=14, minute=0),  # 下午第一节
    time(hour=16, minute=0),
    time(hour=19, minute=0),  # 晚课
]


def set_early_days_alarm():
    # 设置次日早八提醒
    for early_day in early_days:
        logger.info(early_day)
        scheduler.add_job(
            publish,
            "date",
            run_date=datetime.combine(
                early_day - timedelta(days=1), time(hour=21, minute=0)
            ),
            args=["淦，明天有早八。"],
        )  # 早八前一天晚上九点提醒


def show_today_classes():
    # 提醒今天的课表
    for _date, classes_info in timetable.items():
        logger.info(_date)
        notice = "\n".join([
            f"{class_info["datetime"]}:{class_info["name"]}"
            for class_info in classes_info
        ])
        scheduler.add_job(
            publish,
            "date",
            run_date=datetime.combine(_date, time(hour=7, minute=30)),
            args=[notice,],
        )  # 提醒今日课表


@driver.on_startup
def start_up():
    load_timetable_and_early_days()  # 加载课程表和早八
    set_early_days_alarm()  # 设置早八提醒
    show_today_classes()


def load_timetable_and_early_days():
    with Path("timetable.json").open("r", encoding="utf-8") as tb_raw:
        origin_timetable = json.load(tb_raw)
    for c in origin_timetable:
        # 课表每一项对应的日期和时间
        day = datetime.strptime(c["start-date"], "%Y-%m-%d").date()
        _time = meta_time[c["class-index"] - 1]

        if c["class-index"] == 1:  # 早八
            early_days.add(day)

        for weeks in range(c["delta-weeks"]):
            day += timedelta(weeks=weeks)
            if day not in timetable:
                timetable[day] = []
            timetable[day].append(
                {
                    "datetime": datetime.combine(
                        day,
                        _time,
                    ),
                    "name": c["name"],
                }
            )


async def publish(message: str):
    if bot is None:
        logger.error("机器人未初始化")
        return
    await bot.send_group_msg(group_id=group_id, message=message)

