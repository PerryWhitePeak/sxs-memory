# S×S Memory — Alan × Sun Podcast Skill

把一场 **4 小时 22 分**的中文长对话，编译成一个可以调用的 AI Skill：先用证据思考，再用两个声音回答，并把「原文说过什么」和「这次新写了什么」分开标注。

完全离线，只依赖 Python 3 标准库。

```
一场播客  →  2,442 行逐字稿  →  1,190 条证据  →  1 个 SKILL.md
```

## 它做什么

输入一个问题，输出两段：

1. **模拟回答** — 邵艾伦（Alan）与孙宇晨（Sun）两个第一人称声音，各自回答你的问题。回答是新写的模拟，不是录音，也不代表本人立场。
2. **依据与边界** — 每个声音最强的原文段落、说话人、显示时间或章节、`references/transcript.md:L<行号>`；并明确区分：
   - 他们**直接说过**的；
   - 属于**我的解读**的；
   - 没有原文依据、属于**新推断**的。

如果某个说话人对该话题没有直接材料，Skill 会照实说明，并把这一侧的置信度标低，而不是补写一段像原文的话。

## 快速开始

```bash
# 1. 检索（按词法相似度排序，返回带行号的证据）
python scripts/explore.py search "大学生 变现 复利"

# 2. 分说话人对比
python scripts/explore.py compare "财富自由之后 人生 做什么"

# 3. 主题连接：两组证据，以及它们最接近的一对
python scripts/explore.py connect "复利" "薄肌"

# 4. 回查上下文：某条证据前后的几个话轮
python scripts/explore.py context <evidence_id> --radius 3
```

`search` 还有 `--limit N` 与 `--full`（不截断正文）。

把 Skill 交给支持 Skill 的 Agent 时，入口是 [`SKILL.md`](SKILL.md)。

## 结构

```
SKILL.md                     Skill 定义：能力、输出结构、引用规则、边界
references/
  transcript.md              逐字稿，2,442 行、682 个话轮、74,472 字
  evidence.jsonl             1,190 条证据（说话人 / 显示时间 / 行号 / 原文）
  voice-guide.md             两个声音的写作线索
  field-guide.md             证据边界、引用与措辞规则
  provenance.json            来源与校验和
scripts/
  explore.py                 离线检索：search / compare / connect / context
  build_corpus.py            从逐字稿重建 evidence.jsonl
tests/
  test_retrieval.py          检索与引用规则的回归测试
```

## 语料与来源

| 项 | 值 |
| --- | --- |
| 节目 | 邵艾伦 Alan 访谈孙宇晨 Sun，单集约 4 小时 22 分 |
| 逐字稿 | 2,442 行、682 个话轮、74,472 个中文字符 |
| 证据 | 1,190 条，逐条可在逐字稿中找到对应行 |
| 来源 | 公开节目 + 公开完整逐字稿（见 `references/provenance.json` 的 SHA-256） |

`scripts/explore.py` 在启动时会比对逐字稿与证据文件的校验和，不一致会提示。

## 测试

```bash
python -m unittest discover -s tests -v
```

## 使用边界

- **不是本人**。回答是依据逐字稿新写的模拟，不以邵艾伦或孙宇晨本人的名义发言，也不声称复刻他们。
- **不是投资建议**。节目里关于 Crypto、买不买房、择业的表述是个人立场，照搬到其他人身上可能得出相反结论。
- **时间码是段落锚点**，不是逐字级的音频对齐；转写有噪声，多处带「（存疑）」标记。
- **不联网**。没有实时检索、没有语音、没有自动发布。

## 许可

代码（`scripts/`、`tests/`）可自由复用，注明出处即可。

逐字稿与引文来自公开节目，版权归原节目与两位说话人所有；本仓库仅用于研究与个人学习，不主张对原始内容的版权。如果你是权利人并希望下架相关内容，请开 issue，我会处理。

本项目与邵艾伦、孙宇晨及节目制作方无隶属关系。
