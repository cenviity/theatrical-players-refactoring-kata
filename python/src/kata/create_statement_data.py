import math

from cattrs import structure
from kata.classes import Play, PlayType


class PerformanceCalculator:
    def __init__(self, performance: dict, play: Play):
        self._performance = performance
        self._play = play

    @property
    def performance(self) -> dict:
        return self._performance

    @property
    def play(self) -> Play:
        return self._play

    @property
    def amount(self) -> int:
        raise ValueError("subclass responsibility")

    @property
    def volume_credits(self) -> int:
        return max(self.performance["audience"] - 30, 0)


class TragedyCalculator(PerformanceCalculator):
    @property
    def amount(self) -> int:
        result = 40_000
        if self.performance["audience"] > 30:
            result += 1000 * (self.performance["audience"] - 30)
        return result


class ComedyCalculator(PerformanceCalculator):
    @property
    def amount(self) -> int:
        if self.performance["audience"] > 20:
            boost_factor = 800
        else:
            boost_factor = 300
        return 30_000 + boost_factor * self.performance["audience"]

    @property
    def volume_credits(self) -> int:
        return super().volume_credits + math.floor(self.performance["audience"] / 5)


def create_statement_data(invoice: dict, plays: dict) -> dict:
    def enrich_performance(performance: dict) -> dict:
        calculator = create_performance_calculator(performance, play_for(performance))

        result = performance.copy()
        result["play"] = calculator.play
        result["amount"] = calculator.amount
        result["volume_credits"] = calculator.volume_credits
        return result

    def create_performance_calculator(
        performance: dict, play: Play
    ) -> PerformanceCalculator:
        match play.type:
            case PlayType.TRAGEDY:
                return TragedyCalculator(performance, play)
            case PlayType.COMEDY:
                return ComedyCalculator(performance, play)
            case _:
                raise ValueError(f"unknown type: {play.type}")

    def play_for(performance: dict) -> Play:
        return structure(plays[performance["playID"]], Play)

    def total_amount(data: dict) -> int:
        return sum(perf["amount"] for perf in data["performances"])

    def total_volume_credits(data: dict) -> int:
        return sum(perf["volume_credits"] for perf in data["performances"])

    result = {
        "customer": invoice["customer"],
        "performances": [enrich_performance(perf) for perf in invoice["performances"]],
    }
    result["total_amount"] = total_amount(result)
    result["total_volume_credits"] = total_volume_credits(result)
    return result
