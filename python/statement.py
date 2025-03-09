import math


def statement(invoice: dict, plays: dict) -> str:
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

    def volume_credits_for(performance: dict) -> int:
        result = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == performance["play"]["type"]:
            result += math.floor(performance["audience"] / 5)
        return result

    def total_amount(data: dict) -> int:
        result = 0
        for perf in data["performances"]:
            result += perf["amount"]
        return result

    def total_volume_credits(data: dict) -> int:
        result = 0
        for perf in data["performances"]:
            result += perf["volume_credits"]
        return result

    statement_data = {
        "customer": invoice["customer"],
        "performances": [enrich_performance(perf) for perf in invoice["performances"]],
    }
    statement_data["total_amount"] = total_amount(statement_data)
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    return render_plain_text(statement_data)


def render_plain_text(data: dict) -> str:
    def usd(amount: float) -> str:
        return f"${amount / 100:0,.2f}"

    result = f"Statement for {data['customer']}\n"

    for perf in data["performances"]:
        result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"

    result += f"Amount owed is {usd(data['total_amount'])}\n"
    result += f"You earned {data['total_volume_credits']} credits\n"
    return result
