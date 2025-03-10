import math


def create_statement_data(invoice: dict, plays: dict) -> dict:
    def enrich_performance(performance: dict) -> dict:
        result = performance.copy()
        result["play"] = play_for(result)
        result["amount"] = amount_for(result)
        result["volume_credits"] = volume_credits_for(result)
        return result

    def play_for(performance: dict) -> dict:
        return plays[performance["playID"]]

    def amount_for(performance: dict) -> int:
        match performance["play"]["type"]:
            case "tragedy":
                result = 40_000
                if performance["audience"] > 30:
                    result += 1000 * (performance["audience"] - 30)

            case "comedy":
                result = 30_000
                if performance["audience"] > 20:
                    result += 10_000 + 500 * (performance["audience"] - 20)
                result += 300 * performance["audience"]

            case _:
                raise ValueError(f"unknown type: {performance['play']['type']}")

        return result

    def volume_credits_for(performance: dict) -> int:
        result = 0
        result += max(performance["audience"] - 30, 0)
        if performance["play"]["type"] == "comedy":
            result += math.floor(performance["audience"] / 5)
        return result

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
