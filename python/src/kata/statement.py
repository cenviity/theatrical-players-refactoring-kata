from kata.create_statement_data import create_statement_data


def statement(invoice: dict, plays: dict) -> str:
    return render_plain_text(create_statement_data(invoice, plays))


def render_plain_text(data: dict) -> str:
    result = f"Statement for {data['customer']}\n"

    for perf in data["performances"]:
        result += (
            f" {perf['play'].name}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
        )

    result += f"Amount owed is {usd(data['total_amount'])}\n"
    result += f"You earned {data['total_volume_credits']} credits\n"
    return result


def html_statement(invoice: dict, plays: dict) -> str:
    return render_html(create_statement_data(invoice, plays))


def render_html(data: dict) -> str:
    result = f"<h1>Statement for {data['customer']}</h1>\n"
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n"

    for perf in data["performances"]:
        result += f" <tr><td>{perf['play'].name}</td><td>{perf['audience']}</td>"
        result += f"<td>{usd(perf['amount'])}</td></tr>\n"

    result += "</table>\n"
    result += f"<p>Amount owed is <em>{usd(data['total_amount'])}</em></p>\n"
    result += f"<p>You earned <em>{data['total_volume_credits']}</em> credits</p>\n"
    return result


def usd(amount: float) -> str:
    return f"${amount / 100:0,.2f}"
