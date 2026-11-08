# Field guide

## Evidence boundaries

- The exact wording comes from `transcript.md`; `evidence.jsonl` is a compact, searchable map to that manuscript. `provenance.json` holds both SHA-256 hashes. `explore.py` checks hashes and verifies each cited line against the manuscript.
- `time_scope=display_anchor` means the manuscript displays that time on the turn. `time_scope=turn_start` means a continuation paragraph inherits its parent turn's displayed start. Do not call either a word-level timestamp. The script reports audio alignment status when available.
- The speakers are 邵艾伦 (Alan, interviewer) and 孙宇晨 (Sun, guest). Interviewer questions are not automatically his endorsed views. A brief “对” is not enough to infer a full independent position.
- Transcription is manually reviewed but preserves spoken disfluency and occasional marked uncertainty. Quote only the exact text shown. Prefer paraphrase if a passage contains `〔存疑` or is unclear.
- Retrieval is lexical (Chinese character n-grams plus Latin terms), with no external packages. A high score or high term coverage only says the wording is similar. Abstract paraphrases can be missed; retry with a shorter concept, a synonym from the transcript, and neighboring context. A low score does not prove absence.

## Discovery routes

Use these as questions to investigate, not as pre-written conclusions:

1. **个人操作系统**: search `AI 文档 记录`, then `认知 升级 孙学` and `主动健康 数据`. How does making experience legible to an AI relate to the speakers' broader idea of upgrading oneself? Where does the analogy stop?
2. **执行与社会摩擦**: connect `薄肌 健康 财富自由` with `黄毛理论 嘲笑 执行`. Is the proposed answer to resistance a practical method, a personal attitude, or both? Compare with Alan's framing in nearby turns.
3. **自由之后**: compare `财富自由 目标` and search `工作 意义 自由`. Does the conversation treat freedom as an endpoint, a means, or a changing question? Look across the interview rather than relying on one slogan.

For a user's real problem, form two or three possible bridges, retrieve evidence for each endpoint, and retain only those that survive reading the neighboring context. A new bridge may still be useful without direct support, but label it as extrapolation. Present at least one constraint or counterpoint from the conversation when available. If none is available, label your caution as your own reasoning.

## Output patterns

Lead with **模拟回答** in two first-person voices. Then use **依据与边界** to cite what each actually said and distinguish interpretation from extrapolation. For comparisons, identify a genuine difference if the evidence supports one; otherwise explain the overlap. For applications, answer the user's circumstances before presenting evidence. For discovery, let the voices approach the bridge from different angles, then show why the underlying passages are relevant.
