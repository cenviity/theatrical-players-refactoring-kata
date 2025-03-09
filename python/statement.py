import math


def statement(invoice: dict, plays: dict) -> str:
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    def format_as_dollars(amount: float) -> str:
        return f"${amount:0,.2f}"

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

    for perf in invoice["performances"]:
        this_amount = amount_for(perf)

        # add volume credits
        volume_credits += max(perf["audience"] - 30, 0)

        # add extra credit for every ten comedy attendees
        if "comedy" == play_for(perf)["type"]:
            volume_credits += math.floor(perf["audience"] / 5)

        # print line for this order
        result += f" {play_for(perf)['name']}: {format_as_dollars(this_amount / 100)} ({perf['audience']} seats)\n"
        total_amount += this_amount

    result += f"Amount owed is {format_as_dollars(total_amount / 100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result
