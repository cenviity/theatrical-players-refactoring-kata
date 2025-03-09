import math


def statement(invoice: dict, plays: dict) -> str:
    result = f"Statement for {invoice['customer']}\n"

    def usd(amount: float) -> str:
        return f"${amount / 100:0,.2f}"

    def volume_credits_for(performance: dict) -> int:
        result = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == play_for(performance)["type"]:
            result += math.floor(performance["audience"] / 5)
        return result

    def play_for(performance: dict) -> dict:
        return plays[performance["playID"]]

    def amount_for(performance: dict) -> int:
        match play_for(performance)["type"]:
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
                raise ValueError(f"unknown type: {play_for(performance)['type']}")

        return result

    def total_amount() -> int:
        total_amount = 0
        for perf in invoice["performances"]:
            total_amount += amount_for(perf)
        return total_amount

    def total_volume_credits() -> int:
        volume_credits = 0
        for perf in invoice["performances"]:
            volume_credits += volume_credits_for(perf)
        return volume_credits

    for perf in invoice["performances"]:
        # print line for this order
        result += f" {play_for(perf)['name']}: {usd(amount_for(perf))} ({perf['audience']} seats)\n"

    result += f"Amount owed is {usd(total_amount())}\n"
    result += f"You earned {total_volume_credits()} credits\n"
    return result
