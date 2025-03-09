import math


def statement(invoice: dict, plays: dict) -> str:
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    def format_as_dollars(amount: float) -> str:
        return f"${amount:0,.2f}"

    def amount_for(perf: dict, play: dict) -> int:
        match play["type"]:
            case "tragedy":
                this_amount = 40000
                if perf["audience"] > 30:
                    this_amount += 1000 * (perf["audience"] - 30)

            case "comedy":
                this_amount = 30000
                if perf["audience"] > 20:
                    this_amount += 10000 + 500 * (perf["audience"] - 20)
                this_amount += 300 * perf["audience"]

            case _:
                raise ValueError(f"unknown type: {play['type']}")

        return this_amount

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = amount_for(perf, play)

        # add volume credits
        volume_credits += max(perf["audience"] - 30, 0)

        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += math.floor(perf["audience"] / 5)

        # print line for this order
        result += f" {play['name']}: {format_as_dollars(this_amount / 100)} ({perf['audience']} seats)\n"
        total_amount += this_amount

    result += f"Amount owed is {format_as_dollars(total_amount / 100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result
