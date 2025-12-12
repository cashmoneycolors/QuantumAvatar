import asyncio
import json
import tempfile
from pathlib import Path
import unittest

from CORE_LOGIC import (
    QuantumLogic,
    PayPalLogic,
    persist_results,
    record_transfer,
)


class QuantumLogicDecisionTests(unittest.TestCase):
    def setUp(self):
        self.logic = QuantumLogic()

    def test_decide_action_thresholds(self):
        self.assertEqual(self.logic.decide_action("bullish", 0.85), "BUY_AGGRESSIVE")
        self.assertEqual(self.logic.decide_action("bullish", 0.75), "BUY_MODERATE")
        self.assertEqual(self.logic.decide_action("bearish", 0.9), "SELL_AGGRESSIVE")
        self.assertEqual(self.logic.decide_action("bearish", 0.75), "SELL_MODERATE")
        self.assertEqual(self.logic.decide_action("neutral", 0.99), "HOLD")


class PayPalLogicTests(unittest.TestCase):
    def setUp(self):
        self.logic = PayPalLogic()

    def test_transfer_below_threshold(self):
        result = asyncio.run(self.logic.auto_transfer_logic(self.logic.transfer_threshold - 1))
        self.assertIsNone(result)

    def test_transfer_above_threshold(self):
        amount = self.logic.transfer_threshold + 500
        result = asyncio.run(self.logic.auto_transfer_logic(amount))
        self.assertIsNotNone(result)
        self.assertEqual(result["amount"], amount)
        self.assertEqual(result["recipient"], self.logic.business_email)


class PersistenceHelpersTests(unittest.TestCase):
    def test_persist_results_writes_json(self):
        payload = {"total_profit": 100, "timestamp": "2025-12-12T12:00:00"}
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "results.json"
            persist_results(payload, target)
            loaded = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(loaded, payload)

    def test_record_transfer_appends_history(self):
        transfer = {"amount": 2000, "timestamp": "2025-12-12T12:00:00"}
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "transfers.json"
            record_transfer(transfer, target)
            second = {"amount": 1500, "timestamp": "2025-12-12T12:01:00"}
            record_transfer(second, target)
            history = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["amount"], 2000)
            self.assertEqual(history[1]["amount"], 1500)


if __name__ == "__main__":
    unittest.main()
