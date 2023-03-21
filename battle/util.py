import random


MISSMSG = "{0}试图攻击，但是被{1}闪避了！"
BEFOREATTACKMSG = "{0}试图攻击，但是{1}在被打前发动了反击！"
AFTERATTACKMSG = "{0}被攻击后，发动了反击！"
WEAPONHITMSG = "{0}使用武器{1}对{2}造成了{3}次共{4}点伤害！"
HITMSG = '{0}赤手空拳，{1}受到了{2}点伤害！'
WEAPONBIZHONGMSG = '{0}想躲避{1}的攻击，但是{2}的武器{3}是必中的！'
TIMEOUTMSG = '大战了{}回合，{}取得了血量优胜！'
JIASIMSG = '{}突然躺在了地上，躲过了致命一击！'
DOTMSG = '{0}受到技能{1}造成的持续伤害，生命值损失{2}点，剩余{3}回合！'
IGNOREJIASI = '{}想躺地上装死，不料被{}识破！'
SKILLBIZHONGMSG = '{0}想躲避{1}的攻击，但是{2}的技能{3}是必中的！'
SKILLMSG = '{}使用技能{}对{}造成{}点伤害！'
REMOVEHPMSG = '{}被{}的技能{}命中，生命值降低到了{}点！'
REMOVEHPMISSMSG = '{}想使用技能{}来直接移除{}的生命值，不料被闪避了！'
DOTDAMAGEMSG = '{}使用技能{}给以{}造成每回合{}点的持续性伤害，持续{}回合！'
SKILLTURNPASSMSG = '{}的技能{}打了{}一个措手不及，{}的下{}个回合被跳过了！'
WEAPONTURNPASSMSG = '{}的武器{}打了{}一个措手不及，{}的下{}个回合被跳过了！'
RECOVERHPMSG = '{}使用技能{}恢复了{}点生命值！'
RESETDOTMSG = '由于技能{}的效果，{}所受的持续伤害被驱散了！'
NOTHROWWEAPONSMSG = '{}发动了技能{}却发现自己没有武器可扔，愣在了原地！'
THROWWEAPONSMSG = '{}发动技能{}，如暴风骤雨般使用武器！'
CANTFANJIMSG = '{}在挨打前想发动反击，不料{}无法被反击！'
LIMITSKILLMISSMSG = '{}想使用技能{}来限制{}的行动，不料被闪避了！'
LIMITSKILLMSG = '{}使用技能{}成功限制了{}的行动，{}只能进行{}程攻击！'
LIMITACTIVEMSG = '{}想使用{}程攻击，可是被技能{}限制住了！'
TARGETTHROWWEAPONMSG = '{}的技能{}附带了额外效果，{}的武器：'
BUFFMSG = '{}的{}{}附带了额外效果，{}的{}增加{}点，持续{}回合！'
SPEEDEFFECTMSG = '{}的速度比{}快了不少，{}被白白挨打了1回合'
FANJIMISSMSG = '{}想发动反击，不料被{}闪避了！'
ABSORBMSG = '{}的{}附带吸血效果，{}的生命值恢复了{}点！'
DHWLMSG = '{}的伤害被{}的被动技能大海无量反伤了{}点血！'
RESTMSG = '{}的武器使自己休息了1回合！'
SECKILLMSG = '{}的武器触发了秒杀！{}被秒杀了！'


def get_probability(probability: int) -> bool:
    return random.randint(0, 100) < probability
