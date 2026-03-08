from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TopicRequest(BaseModel):
    niche: str
    benchmark_topics: List[str] = []
    trends: List[str] = []
    platform: str = 'xiaohongshu'
    goal: str = '涨粉'


@router.post('/generate')
async def generate_topics(req: TopicRequest):
    niche = req.niche or '通用'
    trend = req.trends[0] if req.trends else '本周热点'
    benchmark = req.benchmark_topics[0] if req.benchmark_topics else '高赞模板'
    platform = req.platform or 'xiaohongshu'
    goal = req.goal or '涨粉'

    goal_map = {
        '涨粉': ('更适合做情绪钩子和共鸣传播', '把第一屏做得更抓眼'),
        '转化': ('更适合做结果承诺和案例证明', '在中段补充结果和信任细节'),
        '接单': ('更适合展示专业度和服务能力', '结尾增加“我能怎么帮你”'),
        '案例展示': ('更适合讲过程和前后变化', '补充案例前后对比和关键动作'),
    }
    strategy, action_tip = goal_map.get(goal, goal_map['涨粉'])

    topics = [
        {
            'title': f'{niche}如何结合「{trend}」快速起量',
            'type': '热点融合',
            'angle': '趋势解读',
            'format': '清单/图文' if platform == 'xiaohongshu' else '短视频/口播',
            'hook': '开头用对比数据或反常识制造停留',
            'points': [
                f'{trend}背后的用户情绪',
                f'{niche}可直接套用的3个切入点',
                action_tip,
            ],
            'hashtags': [f'#{niche}', f'#{trend}', f'#{goal}'],
            'goal_fit': strategy,
        },
        {
            'title': f'{benchmark}拆解：{niche}内容结构复用',
            'type': '对标拆解',
            'angle': '结构复用',
            'format': '长图文/步骤' if platform == 'xiaohongshu' else '拆解口播',
            'hook': '第一屏先给结论，再讲为什么有效',
            'points': [
                '标题公式与封面关键词',
                '内容节奏（开场-展开-行动）',
                f'针对{goal}的结尾引导',
            ],
            'hashtags': [f'#{niche}', '#对标分析', '#爆款拆解'],
            'goal_fit': strategy,
        },
        {
            'title': f'{niche}{goal}避坑：90%人忽略的细节',
            'type': '避坑清单',
            'angle': '反常识切入',
            'format': '短图文/条列' if platform == 'xiaohongshu' else '短口播/快节奏',
            'hook': '前3句先打破用户原有认知',
            'points': [
                '常见误区 + 反例',
                '正确做法 + 最小行动',
                '可复用检查表',
            ],
            'hashtags': [f'#{niche}', f'#{goal}', '#干货'],
            'goal_fit': strategy,
        },
    ]

    return {'success': True, 'data': topics}
