"""
recap.py - 前情提要
从每日更新的追剧数据中读取最新集数，结合预设摘要和AI生成
用法：python recap.py "剧名" 集数
"""

import sys
import random
from datetime import datetime

# 导入数据管理器，读取最新追剧数据
from data_manager import get_drama_info, get_all_dramas


# ============================================================
# 预设摘要数据（可扩展）
# 实际场景可接入 AI API 自动生成
# ============================================================

MOCK_RECAPS = {
    "黑暗荣耀": {
        1: {
            "events": ["文东恩高中时期遭受校园霸凌", "朴妍珍是霸凌事件的主谋", "文东恩决定退学并开始复仇计划"],
            "key_line": "『我不会原谅任何人。』",
            "foreshadowing": "文东恩的复仇之路即将开始"
        },
        2: {
            "events": ["文东恩成为小学教师", "朴妍珍结婚成为豪门太太", "文东恩开始接近朴妍珍的丈夫"],
            "key_line": "『你以为你赢了？我会让你失去一切。』",
            "foreshadowing": "文东恩开始接近朴妍珍的丈夫"
        },
        3: {
            "events": ["文东恩与河道英初次见面", "朴妍珍发现文东恩出现在自己生活中", "朱如炡对文东恩产生好感"],
            "key_line": "『这个世界没有巧合。』",
            "foreshadowing": "朴妍珍开始察觉文东恩的意图"
        },
        4: {
            "events": ["文东恩开始实施复仇第一步", "朴妍珍调查文东恩的背景", "河道英对文东恩产生兴趣"],
            "key_line": "『复仇是一盘棋，每一步都要算好。』",
            "foreshadowing": "朴妍珍即将发现文东恩的真实身份"
        },
        5: {
            "events": ["朴妍珍的过去被揭开一角", "文东恩与朱如炡的关系更进一步", "河道英开始怀疑朴妍珍"],
            "key_line": "『每个人都有不愿提起的过去。』",
            "foreshadowing": "河道英对朴妍珍的信任开始动摇"
        },
        6: {
            "events": ["文东恩成功让朴妍珍陷入危机", "朱如炡发现文东恩的秘密", "河道英面临选择"],
            "key_line": "『风暴要来了。』",
            "foreshadowing": "朱如炡与文东恩的关系面临考验"
        },
        7: {
            "events": ["文东恩发现河道英的真实身份", "朴妍珍开始调查文东恩的过去", "朱如炡表白被拒"],
            "key_line": "『你以为你赢了？游戏才刚刚开始。』",
            "foreshadowing": "河道英的过去即将揭晓"
        },
        8: {
            "events": ["文东恩的复仇进入关键阶段", "朴妍珍丈夫发现真相", "朱如炡决定全力帮助"],
            "key_line": "『我不需要你的同情，我只需要你的帮助。』",
            "foreshadowing": "朴妍珍即将面临重大危机"
        },
        9: {
            "events": ["朴妍珍丈夫选择站在文东恩这边", "朴妍珍孤立无援", "文东恩准备最后一步"],
            "key_line": "『你失去一切的时候，会是什么表情？』",
            "foreshadowing": "最终对决即将到来"
        },
        10: {
            "events": ["朴妍珍彻底崩溃", "文东恩完成复仇", "朱如炡始终陪伴在文东恩身边"],
            "key_line": "『谢谢你，让我重新活了一次。』",
            "foreshadowing": "文东恩能否真正放下过去？"
        }
    },
    "繁花": {
        1: {
            "events": ["90年代的上海，阿宝初到黄河路", "阿宝结识各路商界人物", "股票市场的风云变幻"],
            "key_line": "『上海滩的风，吹得人眼花缭乱。』",
            "foreshadowing": "阿宝的传奇人生即将开始"
        },
        2: {
            "events": ["阿宝开始接触股票市场", "汪小姐与阿宝相识", "爷叔暗中观察阿宝"],
            "key_line": "『赚钱的机会，在每个人的口袋里。』",
            "foreshadowing": "汪小姐与阿宝的关系将影响后续剧情"
        },
        3: {
            "events": ["阿宝第一次炒股获利", "商界对手开始关注阿宝", "汪小姐对阿宝产生感情"],
            "key_line": "『股市如人生，起起落落。』",
            "foreshadowing": "阿宝的对手即将出手"
        },
        4: {
            "events": ["阿宝遭遇第一次投资失败", "爷叔出手相助", "汪小姐成为阿宝的得力助手"],
            "key_line": "『失败是成功路上的必经之路。』",
            "foreshadowing": "爷叔的真实身份成为谜团"
        },
        5: {
            "events": ["阿宝重振旗鼓", "商界格局发生变化", "黄河路上的饭店相继开业"],
            "key_line": "『上海滩的繁华，从来不缺主角。』",
            "foreshadowing": "新的对手即将登场"
        },
        6: {
            "events": ["阿宝与对手第一次正面交锋", "汪小姐遇到危机", "爷叔暗中布局"],
            "key_line": "『商场如战场，一步都不能错。』",
            "foreshadowing": "阿宝的朋友可能成为敌人"
        },
        7: {
            "events": ["阿宝获得阶段性胜利", "汪小姐的父亲去世", "阿宝成为黄河路的风云人物"],
            "key_line": "『站在高处的时候，要看清脚下的路。』",
            "foreshadowing": "阿宝的成功引来了更多对手"
        },
        8: {
            "events": ["阿宝的饭店成为黄河路第一", "汪小姐与阿宝的绯闻传开", "爷叔亮明身份"],
            "key_line": "『上海滩，从来都是英雄的舞台。』",
            "foreshadowing": "爷叔的身份关系到阿宝的成败"
        },
        9: {
            "events": ["阿宝面临更大的商业挑战", "汪小姐选择离开", "爷叔给阿宝留下忠告"],
            "key_line": "『人这一辈子，最重要的是看清自己。』",
            "foreshadowing": "阿宝能否守住自己的江山？"
        },
        10: {
            "events": ["阿宝在商界彻底站稳脚跟", "黄河路进入新时代", "阿宝回忆起自己的初心"],
            "key_line": "『上海滩的繁华，不是一个人的戏。』",
            "foreshadowing": "下一章，阿宝将面临新的挑战"
        },
        11: {
            "events": ["阿宝的事业进入新阶段", "新的竞争对手出现", "汪小姐的回归"],
            "key_line": "『人生如戏，戏如人生。』",
            "foreshadowing": "阿宝与汪小姐的感情线再度开启"
        },
        12: {
            "events": ["宝总在股市中遭遇重大挫折", "汪小姐与宝总的关系出现裂痕", "爷叔暗中布局"],
            "key_line": "『上海滩的繁荣，不是一个人的戏。』",
            "foreshadowing": "宝总的对手即将浮出水面"
        }
    },
    "庆余年2": {
        1: {
            "events": ["范闲离开京都出使北齐", "北齐之行危机重重", "范闲发现更大的阴谋"],
            "key_line": "『这朝堂之上，每一步都是棋局。』",
            "foreshadowing": "北齐之行的真相远比想象中复杂"
        },
        2: {
            "events": ["范闲在北齐遭遇刺杀", "海棠朵朵暗中相助", "范闲发现神庙的秘密"],
            "key_line": "『这个世界，远比你想象的更大。』",
            "foreshadowing": "神庙的秘密关系到整个世界的真相"
        },
        3: {
            "events": ["范闲成功完成任务返回京都", "庆帝对范闲的态度发生变化", "二皇子开始拉拢势力"],
            "key_line": "『人心难测，帝王之心更难测。』",
            "foreshadowing": "庆帝的真实目的开始浮现"
        },
        4: {
            "events": ["范闲与二皇子的矛盾开始激化", "林婉儿发现范闲的秘密", "五竹叔在暗中保护范闲"],
            "key_line": "『有些事情，知道得越少越好。』",
            "foreshadowing": "范闲的身份之谜即将揭晓"
        },
        5: {
            "events": ["范闲被卷入皇权争斗", "庆帝安排范闲参与朝政", "范闲开始组建自己的势力"],
            "key_line": "『朝堂之上，没有永远的朋友。』",
            "foreshadowing": "范闲将成为各方势力争夺的对象"
        },
        6: {
            "events": ["范闲与二皇子正面交锋", "林婉儿成为范闲的软肋", "五竹叔展现真正实力"],
            "key_line": "『为了保护重要的人，我可以做任何事。』",
            "foreshadowing": "范闲将面临艰难的选择"
        },
        7: {
            "events": ["范闲在朝堂上站稳脚跟", "二皇子联合其他势力反扑", "范闲发现幕后黑手的线索"],
            "key_line": "『在这场权力的游戏里，没有人可以独善其身。』",
            "foreshadowing": "幕后黑手可能是范闲最亲近的人"
        },
        8: {
            "events": ["范闲与二皇子的矛盾全面爆发", "林婉儿遭遇危险", "五竹叔展现超凡实力"],
            "key_line": "『我这一生，从不后悔自己的选择。』",
            "foreshadowing": "范闲的敌人不止一个"
        },
        9: {
            "events": ["范闲成功化解二皇子的阴谋", "庆帝对范闲的评价发生改变", "范闲开始调查父亲的往事"],
            "key_line": "『每一个父亲，都有自己的秘密。』",
            "foreshadowing": "范闲父亲的过去关系到大东山之战的真相"
        },
        10: {
            "events": ["范闲发现大东山之战的内幕", "庆帝的真实目的暴露", "范闲面临最终抉择"],
            "key_line": "『天下兴亡，匹夫有责。』",
            "foreshadowing": "范闲将如何选择自己的道路？"
        },
        11: {
            "events": ["范闲在朝堂上影响力大增", "庆帝的身体出现状况", "各皇子开始争夺皇位"],
            "key_line": "『权力的游戏，永远不会结束。』",
            "foreshadowing": "庆帝的秘密将颠覆所有人的认知"
        },
        12: {
            "events": ["范闲与庆帝对峙", "范闲身世之谜揭晓", "各方势力的最终对决开始"],
            "key_line": "『我是谁，我自己说了算！』",
            "foreshadowing": "最终决战即将展开"
        },
        13: {
            "events": ["范闲的过去被揭露", "庆帝的真实目的全部曝光", "范闲联合各方势力"],
            "key_line": "『这朝堂之上，每一步都是棋局。』",
            "foreshadowing": "范闲面临最大的挑战"
        },
        14: {
            "events": ["范闲与庆帝的关系破裂", "范闲决定反抗", "五竹叔展现真正的能力"],
            "key_line": "『你教会了我一切，但你教会不了我屈服。』",
            "foreshadowing": "范闲的成长将决定胜负"
        },
        15: {
            "events": ["范闲与二皇子的矛盾升级", "林婉儿发现范闲的秘密", "五竹叔出手相助，展现强大实力"],
            "key_line": "『这朝堂之上，每一步都是棋局。』",
            "foreshadowing": "范闲面临更大的阴谋"
        }
    },
    "狂飙": {
        1: {
            "events": ["2000年，高启强还是个小鱼贩", "安欣第一次见到高启强", "高启强因打架被拘留"],
            "key_line": "『我不想过这样的日子了。』",
            "foreshadowing": "高启强的人生即将改变"
        },
        2: {
            "events": ["高启强结识了黑社会老大", "安欣开始关注高启强", "高启强开始走上不同的人生道路"],
            "key_line": "『人要是不想被人欺负，就得往上爬。』",
            "foreshadowing": "高启强的命运正在改变"
        },
        3: {
            "events": ["高启强开始涉足黑道", "安欣成为警察", "两人的人生轨迹开始分岔"],
            "key_line": "『这世上没有绝对的黑与白。』",
            "foreshadowing": "高启强与安欣的较量才刚刚开始"
        },
        4: {
            "events": ["高启强在黑道上崛起", "安欣在警界崭露头角", "第一次正面对峙"],
            "key_line": "『游戏才刚刚开始。』",
            "foreshadowing": "高启强的真正对手是安欣"
        },
        5: {
            "events": ["高启强在商界开始布局", "安欣的调查受到阻挠", "高启强的背景越来越复杂"],
            "key_line": "『在这个城市里，谁才是真正的主人？』",
            "foreshadowing": "高启强的势力正在渗透各行各业"
        },
        6: {
            "events": ["高启强遭遇信任危机", "安欣找到关键证据", "双方都面临艰难的选择"],
            "key_line": "『信任这东西，一旦破碎就很难修复。』",
            "foreshadowing": "高启强身边的人开始动摇"
        },
        7: {
            "events": ["高启强在商界彻底站稳脚跟", "安欣的家人受到威胁", "两人之间的矛盾全面爆发"],
            "key_line": "『我们都在用自己认为对的方式活着。』",
            "foreshadowing": "真正的较量才刚刚开始"
        },
        8: {
            "events": ["高启强的犯罪证据逐渐浮出水面", "安欣的执着追查", "高启强面临前所未有的危机"],
            "key_line": "『你以为你赢了？还没有结束。』",
            "foreshadowing": "高启强的命运将如何收场？"
        },
        9: {
            "events": ["高启强的犯罪证据逐渐浮出水面", "安欣的执着追查", "高启强面临前所未有的危机"],
            "key_line": "『在这个城市里，谁才是真正的主人？』",
            "foreshadowing": "最终的对决即将到来"
        }
    },
    "三体": {
        1: {
            "events": ["物理学界发生诡异事件", "杨冬的遗书留下神秘信息", "汪淼开始调查纳米材料的真相"],
            "key_line": "『物理学不存在了？』",
            "foreshadowing": "三体世界的存在即将揭晓"
        },
        2: {
            "events": ["汪淼发现宇宙闪烁现象", "史强警官加入调查", "红岸基地的秘密开始浮现"],
            "key_line": "『我们看到的宇宙，只是它的表象。』",
            "foreshadowing": "叶文洁的过去将成为关键"
        },
        3: {
            "events": ["叶文洁的过去被揭开", "红岸基地的真相曝光", "三体世界首次被提及"],
            "key_line": "『用魔法打败魔法。』",
            "foreshadowing": "三体舰队正在向地球进发"
        },
        4: {
            "events": ["三体世界的细节被揭晓", "地球三体组织的成立", "汪淼发现更大的阴谋"],
            "key_line": "『这个世界远比你想象的复杂。』",
            "foreshadowing": "人类面临生死存亡的威胁"
        },
        5: {
            "events": ["人类与三体文明的首次对话", "地球三体组织的行动升级", "汪淼承担更大责任"],
            "key_line": "『置之死地而后生。』",
            "foreshadowing": "人类将如何应对三体危机？"
        },
        6: {
            "events": ["三体文明的真相被完全揭晓", "人类的恐惧与希望交织", "汪淼做出重大决定"],
            "key_line": "『宇宙就是一座黑暗森林。』",
            "foreshadowing": "宇宙的真相远比想象的更残酷"
        }
    },
    "莲花楼": {
        1: {
            "events": ["李莲花是江湖上最年轻的城主", "莲花楼的生意遍布天下", "李莲花收到神秘来信"],
            "key_line": "『在这个世上，没有什么是不可能的。』",
            "foreshadowing": "李莲花的真实身份即将揭晓"
        },
        2: {
            "events": ["李莲花开始调查一桩案件", "方多病成为新的伙伴", "江湖上的势力开始暗流涌动"],
            "key_line": "『江湖就是这样，你永远不知道明天会发生什么。』",
            "foreshadowing": "李莲花的过去将成为关键"
        },
        3: {
            "events": ["李莲花的真实身份被揭开", "他是百年前消失的大侠", "江湖各派都想拉拢他"],
            "key_line": "『百年过去，江湖还是那个江湖。』",
            "foreshadowing": "李莲花的真正目的正在浮现"
        },
        4: {
            "events": ["李莲花发现自己的过去有更多秘密", "方多病遇到危险", "李莲花出手相助"],
            "key_line": "『我这一生，见过太多的悲欢离合。』",
            "foreshadowing": "李莲花的身世之谜即将揭晓"
        }
    },
    "长相思2": {
        1: {
            "events": ["小夭重返清水镇", "涂山璟和相柳之间的纷争再度升级", "小夭面临全新的选择"],
            "key_line": "『有些事，一旦错过就是一生。』",
            "foreshadowing": "小夭的命运将走向何方？"
        },
        2: {
            "events": ["涂山璟发现当年真相", "相柳展开新的行动", "小夭被迫卷入更大的纷争"],
            "key_line": "『这世间最难解的，是人心。』",
            "foreshadowing": "三人的命运再度交织"
        },
        3: {
            "events": ["小夭发现自己的身份之谜", "涂山璟和相柳的态度都发生了变化", "新的势力开始登场"],
            "key_line": "『命运不会放过任何一个人。』",
            "foreshadowing": "小夭的命运将彻底改变"
        },
        4: {
            "events": ["小夭面临终极选择", "涂山璟和相柳的真相全部揭晓", "大结局"],
            "key_line": "『有些人，注定要错过。』",
            "foreshadowing": "一切终将尘埃落定"
        }
    },
    "边水往事": {
        1: {
            "events": ["金三角地区的危险交易", "沈星为还清债务来到边水", "意外卷入地下交易"],
            "key_line": "『在边水，人命是最不值钱的东西。』",
            "foreshadowing": "沈星的人生即将被彻底改变"
        },
        2: {
            "events": ["沈星被迫加入秘密行动", "达班大哥的信任与考验", "沈星的过去逐渐被揭开"],
            "key_line": "『想要活下去，就得学会规则。』",
            "foreshadowing": "沈星正在一步步走向深渊"
        },
        3: {
            "events": ["沈星面临道德与生存的选择", "关键人物出场", "边水的真实面目正在展开"],
            "key_line": "『在这里，只有强者才能活。』",
            "foreshadowing": "沈星将成为改变边水的关键人物"
        }
    },
    "白夜追凶": {
        1: {
            "events": ["关宏峰和关宏宇是双胞胎兄弟", "一起灭门惨案将两人卷入", "关宏峰成为嫌疑犯"],
            "key_line": "『我相信我弟弟是无辜的。』",
            "foreshadowing": "灭门案的真相扑朔迷离"
        },
        2: {
            "events": ["关宏峰决定私下调查案件", "兄弟两人开始互换身份", "周巡警官加入调查"],
            "key_line": "『在这个世界上，最了解你的人，是你的对手。』",
            "foreshadowing": "兄弟两人的身份互换计划即将开始"
        },
        3: {
            "events": ["关宏峰在明处调查，关宏宇在暗处配合", "两人互换身份的冒险", "灭门案的新线索不断浮现"],
            "key_line": "『正义可能会迟到，但永远不会缺席。』",
            "foreshadowing": "两人互换身份的风险越来越大"
        },
        4: {
            "events": ["关宏峰发现内部有鬼", "关宏宇的身份面临暴露风险", "灭门案的真相逐渐浮出水面"],
            "key_line": "『最危险的地方，就是最安全的地方。』",
            "foreshadowing": "真正的凶手就在他们身边"
        },
        5: {
            "events": ["关宏峰和关宏宇联手破案", "兄弟之间的羁绊更深", "灭门案的真凶现身"],
            "key_line": "『我们是兄弟，永远都是。』",
            "foreshadowing": "真正的幕后黑手即将现身"
        }
    },
    "隐秘的角落": {
        1: {
            "events": ["三个孩子在景区意外拍到谋杀视频", "张东升是杀人犯", "孩子们决定不报警"],
            "key_line": "『每个人都有自己隐秘的角落。』",
            "foreshadowing": "孩子们的选择将改变所有人的命运"
        },
        2: {
            "events": ["张东升发现有人拍到了证据", "开始追查三个孩子", "孩子们的秘密面临暴露"],
            "key_line": "『你的秘密，就是你的软肋。』",
            "foreshadowing": "张东升的追查将越来越近"
        },
        3: {
            "events": ["三个孩子面临巨大危险", "朱朝阳的家庭问题被揭开", "张东升的过去也浮出水面"],
            "key_line": "『每个人都有想要隐藏的过去。』",
            "foreshadowing": "所有人的秘密都将被揭开"
        }
    },
    "沉默的真相": {
        1: {
            "events": ["江阳检察官接手一个看似普通的自杀案", "自杀案背后隐藏着巨大的秘密", "江阳的执着调查"],
            "key_line": "『真相可能会迟到，但永远不会缺席。』",
            "foreshadowing": "这个案件远比想象的更复杂"
        },
        2: {
            "events": ["江阳的调查触动了某些人的利益", "受到威胁和阻挠", "妻子劝他放弃"],
            "key_line": "『有些事，必须有人去做。』",
            "foreshadowing": "江阳的选择将影响他的一生"
        },
        3: {
            "events": ["江阳的好友卷入案件", "更大的阴谋被揭开", "江阳面临生死考验"],
            "key_line": "『在这个世界上，真相是需要代价的。』",
            "foreshadowing": "江阳付出的代价远超想象"
        }
    }
}


def generate_ai_recap(drama_name: str, episode: int) -> dict:
    """
    AI 智能生成前情提要（基于剧情模式和上下文推断）
    实际场景可替换为真实的 AI API 调用
    """
    
    # 从预设摘要中获取相同剧集的数据作为参考
    drama_recaps = MOCK_RECAPS.get(drama_name, {})
    existing = drama_recaps.get(episode, {})
    
    if existing:
        return existing
    
    # 如果没有预设，AI 动态生成
    events = [
        f"《{drama_name}》第{episode}集剧情持续推进",
        "主要角色面临新的挑战和选择",
        "关键线索正在逐步浮出水面"
    ]
    
    # 尝试根据前后集推断内容
    prev = drama_recaps.get(episode - 1, {})
    if prev:
        events.append(f"接续上集：{prev.get('events', ['剧情继续发展'])[0][:20]}...")
    
    key_lines = [
        "『真相往往比你想象的更复杂。』",
        "『每个人都有自己的选择。』",
        "『命运不会放过任何人。』"
    ]
    
    return {
        "events": events,
        "key_line": random.choice(key_lines),
        "foreshadowing": f"第{episode + 1}集将有重要突破",
        "ai_generated": True
    }


def get_latest_episode_from_data(drama_name: str) -> int:
    """
    从每日更新的数据中获取最新集数
    """
    info = get_drama_info(drama_name)
    if info:
        return info.get('latest_episode', 0)
    return 0


def get_my_episode_from_data(drama_name: str) -> int:
    """
    从每日更新的数据中获取我的集数
    """
    info = get_drama_info(drama_name)
    if info:
        return info.get('my_episode', 0)
    return 0


def generate_recap(drama_name: str, episode: int) -> str:
    """
    生成前情提要，结合每日更新的数据
    """
    
    # 从数据中获取最新更新
    latest = get_latest_episode_from_data(drama_name)
    my_ep = get_my_episode_from_data(drama_name)
    
    # 获取摘要
    drama_recaps = MOCK_RECAPS.get(drama_name, {})
    recap = drama_recaps.get(episode)
    
    # 如果没有预设，使用 AI 生成
    if not recap:
        recap = generate_ai_recap(drama_name, episode)
    
    output = []
    output.append("=" * 60)
    output.append(f"📝 《{drama_name}》第 {episode} 集 前情提要")
    output.append("=" * 60)
    output.append("")
    
    # 显示追剧进度信息（结合每日更新数据）
    if latest > 0 or my_ep > 0:
        output.append("📊 追剧进度：")
        if my_ep > 0:
            output.append(f"   ├─ 你看到：第 {my_ep} 集")
        if latest > 0:
            output.append(f"   ├─ 最新更新：第 {latest} 集")
        if my_ep > 0 and latest > 0:
            behind = latest - my_ep
            if behind > 0:
                output.append(f"   └─ 你还落后 {behind} 集")
            elif behind == 0:
                output.append(f"   └─ ✅ 已追平最新更新！")
        output.append("")
        output.append("-" * 60)
        output.append("")
    
    # 剧情摘要
    output.append("📌 主要事件：")
    for event in recap.get('events', []):
        output.append(f"  - {event}")
    output.append("")
    
    output.append("💬 关键台词：")
    output.append(f'  "{recap.get("key_line", "精彩继续！")}"')
    output.append("")
    
    output.append("🔮 本集伏笔：")
    output.append(f"  - {recap.get('foreshadowing', '新的线索正在展开')}")
    output.append("")
    
    if recap.get('ai_generated'):
        output.append("🤖 （本摘要由AI自动生成）")
        output.append("")
    
    output.append("👉 继续看下一集吧！")
    output.append("📌 提示：用 parser.py 更新你的追剧进度")
    
    return "\n".join(output)


def main():
    """
    主函数 - 支持命令行参数和交互模式
    """
    
    # 检查是否提供了命令行参数
    if len(sys.argv) >= 3:
        drama_name = sys.argv[1]
        try:
            episode = int(sys.argv[2])
        except ValueError:
            print("❌ 集数必须是数字")
            return
    else:
        # 交互模式
        print("=" * 60)
        print("📝 前情提要工具")
        print("=" * 60)
        print()
        
        # 显示在追剧集列表
        all_dramas = list(get_all_dramas().keys())
        if all_dramas:
            print("📺 你正在追的剧：")
            for i, name in enumerate(all_dramas, 1):
                info = get_drama_info(name)
                latest = info.get('latest_episode', 0) if info else 0
                my_ep = info.get('my_episode', 0) if info else 0
                print(f"   {i}. 《{name}》 - 看到第{my_ep}集，最新第{latest}集")
            print()
        
        drama_name = input("请输入剧名：").strip()
        if not drama_name:
            print("❌ 请提供剧名")
            return
        
        try:
            episode = int(input("请输入集数：").strip())
        except ValueError:
            print("❌ 集数必须是数字")
            return
    
    print()
    print(generate_recap(drama_name, episode))


if __name__ == "__main__":
    main()
