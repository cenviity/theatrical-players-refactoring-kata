import math


def statement(invoice: dict, plays: dict) -> str:
    def enrich_performance(performance: dict) -> dict:
        result = performance.copy()
        result["play"] = play_for(result)
        return result

    def play_for(performance: dict) -> dict:
        return plays[performance["playID"]]

    statement_data = {
        "customer": invoice["customer"],
        "performances": [enrich_performance(perf) for perf in invoice["performances"]],
    }
    return render_plain_text(statement_data)


def render_plain_text(data: dict) -> str:
    def usd(amount: float) -> str:
        return f"${amount / 100:0,.2f}"

    def volume_credits_for(performance: dict) -> int:
        result = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == performance["play"]["type"]:
            result += math.floor(performance["audience"] / 5)
        return result

    def amount_for(performance: dict) -> int:
        match performance["play"]["type"]:
            case "tragedy":
                result = 40000
                if performance["audience"] > 30:
                    result += 1000 * (performance["audience"] - 30)

            case "comedy":
                result = 30000
                if performance["audience"] > 20:
                    result += 10000 + 500 * (performance["audience"] - 20)
                result += 300 * performance["audience"]

            case _:
                raise ValueError(f"unknown type: {performance['play']['type']}")

        return result

    def total_amount() -> int:
        result = 0
        for perf in data["performances"]:
            result += amount_for(perf)
        return result

    def total_volume_credits() -> int:
        result = 0
        for perf in data["performances"]:
            result += volume_credits_for(perf)
        return result

    result = f"Statement for {data['customer']}\n"

    for perf in data["performances"]:
        result += f" {perf['play']['name']}: {usd(amount_for(perf))} ({perf['audience']} seats)\n"

    result += f"Amount owed is {usd(total_amount())}\n"
    result += f"You earned {total_volume_credits()} credits\n"
    return result
