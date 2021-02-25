# -*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-11-20 13:12:48
# @Last Modified by:   ander
# @Last Modified time: 2020-04-17 15:02:35
stop_words = ['\u200b', 'c', 'C', '展开', '全文', '$', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '?', '_', '“', '”', '、', '。', '《', '》', '一', '一些', '一何', '一切', '一则', '一方面', '一旦', '一来', '一样', '一般', '一转眼', '万一', '上', '上下', '下', '不', '不仅', '不但', '不光', '不单', '不只', '不外乎', '不如', '不妨', '不尽', '不尽然', '不得', '不怕', '不惟', '不成', '不拘', '不料', '不是', '不比', '不然', '不特', '不独', '不管', '不至于', '不若', '不论', '不过', '不问', '与', '与其', '与其说', '与否', '与此同时', '且', '且不说', '且说', '两者', '个', '个别', '临', '为', '为了', '为什么', '为何', '为止', '为此', '为着', '乃', '乃至', '乃至于', '么', '之', '之一', '之所以', '之类', '乌乎', '乎', '乘', '也', '也好', '也罢', '了', '二来', '于', '于是', '于是乎', '云云', '云尔', '些', '亦', '人', '人们', '人家', '什么', '什么样', '今', '介于', '仍', '仍旧', '从', '从此', '从而', '他', '他人', '他们', '以', '以上', '以为', '以便', '以免', '以及', '以故', '以期', '以来', '以至', '以至于', '以致', '们', '任', '任何', '任凭', '似的', '但', '但凡', '但是', '何', '何以', '何况', '何处', '何时', '余外', '作为', '你', '你们', '使', '使得', '例如', '依', '依据', '依照', '便于', '俺', '俺们', '倘', '倘使', '倘或', '倘然', '倘若', '借', '假使', '假如', '假若', '傥然', '像', '儿', '先不先', '光是', '全体', '全部', '兮', '关于', '其', '其一', '其中', '其二', '其他', '其余', '其它', '其次', '具体地说', '具体说来', '兼之', '内', '再', '再其次', '再则', '再有', '再者', '再者说', '再说', '冒', '冲', '况且', '几', '几时', '凡', '凡是', '凭', '凭借', '出于', '出来', '分别', '则', '则甚', '别', '别人', '别处', '别是', '别的', '别管', '别说', '到', '前后', '前此', '前者', '加之', '加以', '即', '即令', '即使', '即便', '即如', '即或', '即若', '却', '去', '又', '又及', '及', '及其', '及至', '反之', '反而', '反过来', '反过来说', '受到', '另', '另一方面', '另外', '另悉', '只', '只当', '只怕', '只是', '只有', '只消', '只要', '只限', '叫', '叮咚', '可', '可以', '可是', '可见', '各', '各个', '各位', '各种', '各自', '同', '同时', '后', '后者', '向', '向使', '向着', '吓', '吗', '否则', '吧', '吧哒', '吱', '呀', '呃', '呕', '呗', '呜', '呜呼', '呢', '呵', '呵呵', '呸', '呼哧', '咋', '和', '咚', '咦', '咧', '咱', '咱们', '咳', '哇', '哈', '哈哈', '哉', '哎', '哎呀', '哎哟', '哗', '哟', '哦', '哩', '哪', '哪个', '哪些', '哪儿', '哪天', '哪年', '哪怕', '哪样', '哪边', '哪里', '哼', '哼唷', '唉', '唯有', '啊', '啐', '啥', '啦', '啪达', '啷当', '喂', '喏', '喔唷', '喽', '嗡', '嗡嗡', '嗬', '嗯', '嗳', '嘎', '嘎登', '嘘', '嘛', '嘻', '嘿', '嘿嘿', '因', '因为', '因了', '因此', '因着', '因而', '固然', '在', '在下', '在于', '地', '基于', '处在', '多', '多么', '多少', '大', '大家', '她', '她们', '好', '如', '如上', '如上所述', '如下', '如何', '如其', '如同', '如是', '如果', '如此', '如若', '始而', '孰料', '孰知', '宁', '宁可', '宁愿', '宁肯', '它', '它们', '对', '对于', '对待', '对方', '对比', '将', '小', '尔', '尔后', '尔尔', '尚且', '就', '就是', '就是了', '就是说', '就算', '就要', '尽', '尽管', '尽管如此', '岂但', '己', '已', '已矣', '巴', '巴巴', '并', '并且', '并非', '庶乎', '庶几', '开外', '开始', '归', '归齐', '当', '当地', '当然', '当着', '彼', '彼时', '彼此', '往', '待', '很', '得', '得了', '怎', '怎么', '怎么办', '怎么样', '怎奈', '怎样', '总之', '总的来看', '总的来说', '总的说来', '总而言之', '恰恰相反', '您', '惟其', '慢说', '我', '我们', '或', '或则', '或是', '或曰', '或者', '截至', '所', '所以', '所在', '所幸', '所有', '才', '才能', '打', '打从', '把', '抑或', '拿', '按', '按照', '换句话说', '换言之', '据', '据此', '接着', '故', '故此', '故而', '旁人', '无', '无宁', '无论', '既', '既往', '既是', '既然', '时候', '是', '是以', '是的', '曾', '替', '替代', '最', '有', '有些', '有关', '有及', '有时', '有的', '望', '朝', '朝着', '本', '本人', '本地', '本着', '本身', '来', '来着', '来自', '来说', '极了', '果然', '果真', '某', '某个', '某些', '某某', '根据', '欤', '正值', '正如', '正巧', '正是', '此', '此地', '此处', '此外', '此时', '此次', '此间', '毋宁', '每', '每当', '比', '比及', '比如', '比方', '没奈何', '沿', '沿着', '漫说', '焉', '然则', '然后', '然而', '照', '照着', '犹且', '犹自', '甚且', '甚么', '甚或', '甚而', '甚至', '甚至于', '用', '用来', '由', '由于', '由是', '由此', '由此可见', '的', '的确', '的话', '直到', '相对而言', '省得', '看', '眨眼', '着', '着呢', '矣', '矣乎', '矣哉', '离', '竟而', '第', '等', '等到', '等等', '简言之', '管', '类如', '紧接着', '纵', '纵令', '纵使', '纵然', '经', '经过', '结果', '给', '继之', '继后', '继而', '综上所述', '罢了', '者', '而', '而且', '而况', '而后', '而外', '而已', '而是', '而言', '能', '能否', '腾', '自', '自个儿', '自从', '自各儿', '自后', '自家', '自己', '自打', '自身', '至', '至于', '至今', '至若', '致', '般的', '若', '若夫', '若是', '若果 ', '若非', '莫不然', '莫如', '莫若', '虽', '虽则', '虽然', '虽说', '被', '要', '要不', '要不是', '要不然', '要么', '要是', '譬喻', '譬如', '让', '许多', '论', '设使', '设或', '设若', '诚如', '诚然', '该', '说来', '诸', '诸位', '诸如', '谁', '谁人', '谁料', '谁知', '贼死', '赖以', '赶', '起', '起见', '趁', '趁着', '越是', '距', '跟', '较', '较之', '边', '过', '还', '还是', '还有', '还要', '这', '这一来', '这个', '这么', '这么些', '这么样', '这么点儿', '这些', '这会儿', '这儿', '这就是说', '这时', '这样', '这次', '这般', '这边', '这里', '进而', '连', '连同', '逐步', '通过', '遵循', '遵照', '那', '那个', '那么', '那么些', '那么样', '那些', '那会儿', '那儿', '那时', '那样', '那般', '那边', '那里', '都', '鄙人', '鉴于', '针对', '阿', '除', '除了', '除外', '除开', '除此之外', '除非', '随', '随后', '随时', '随着', '难道说', '非但', '非徒', '非特', '非独', '靠', '顺', '顺着', '首先', '！', '，', '：', '；', '？', ]
stop_words += ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']