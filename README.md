[![SVG Banners](https://svg-banners.vercel.app/api?type=origin&text1=QQ机器人脚手架%20🤠&width=800&height=400)](https://github.com/Akshay090/svg-banners)

# 😄快速开始

## 安装

```bash
pipx install nb-cli # 安装nonebot cli
# 激活虚拟环境
python -m venv .venv
.venv\Scripts\activate
# 安装依赖
poetry install
```

## 运行

```bash
nb run
```

# 😀子模块

## 课表机器人

### 功能设计

#### 定时任务

- [x] 每天晚上提醒第二天有没有早八（未测试）

- [x] 每天早上发布今天的课表（未测试）

#### 响应

- [x] 课表查询（已测试）

- [ ] 教室查询

- [ ] 自定义提醒


### 课表格式设计

```json
[
    {
        "name":"课程名",
        "start-date":"2024-10-09",
        // 两项中取一项生效
        "delta-weeks":3,
        "gap-weeks":[true,false,true],
        // 两项中取一项生效
        "start-time":"08:00",
        "class-index":2
    },
]
```