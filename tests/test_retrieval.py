from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/explore.py"
spec = importlib.util.spec_from_file_location("podcast_explore", SCRIPT)
explore = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = explore
spec.loader.exec_module(explore)


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = explore.load()

    def test_grounded_question_has_answer_in_nearby_turns(self):
        hits = explore.search(self.rows, "20岁没有资源怎么开始", 4)
        self.assertTrue(any(row["speaker"] == "邵艾伦" and row["time"] == "00:07:58" for row in hits))
        question = next(row for row in hits if row["time"] == "00:07:58")
        index = self.rows.index(next(row for row in self.rows if row["id"] == question["id"]))
        self.assertTrue(any(row["speaker"] == "孙宇晨" for row in self.rows[index + 1:index + 5]))

    def test_comparison_preserves_speaker_separation(self):
        for speaker in ("邵艾伦", "孙宇晨"):
            hits = explore.search(self.rows, "财富自由", 4, speaker)
            self.assertTrue(hits)
            self.assertTrue(all(row["speaker"] == speaker for row in hits))

    def test_discovery_finds_distant_evidence(self):
        a = explore.search(self.rows, "AI 文档 记录", 5)
        b = explore.search(self.rows, "主动健康 财富自由", 5)
        self.assertTrue(a and b)
        self.assertTrue(any(abs(x["order"] - y["order"]) > 20 for x in a for y in b))

    def test_unaddressed_policy_is_not_claimed_by_retrieval(self):
        hits = explore.search(self.rows, "火星殖民政策", 5)
        self.assertFalse(any("火星殖民政策" in row["text"] for row in hits))


if __name__ == "__main__":
    unittest.main()
