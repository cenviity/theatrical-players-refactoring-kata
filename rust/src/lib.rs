use std::cmp::max;

use currency_rs::{Currency, CurrencyOpts};
use serde_json::Value;

pub fn statement(invoice: Value, plays: Value) -> String {
    let mut total_amount = 0;
    let mut volume_credits = 0;
    let mut result = format!("Statement for {}\n", invoice["customer"].as_str().unwrap());

    let play_for =
        |performance: &Value| -> &Value { &plays[performance["playID"].as_str().unwrap()] };

    for perf in invoice["performances"].as_array().unwrap() {
        let this_amount = amount_for(perf, play_for(perf));
        // add volume credits
        volume_credits += max(perf["audience"].as_u64().unwrap() - 30, 0);
        // add extra credit for every ten comedy attendees
        if "comedy" == play_for(perf)["type"].as_str().unwrap() {
            volume_credits += (perf["audience"].as_f64().unwrap() / 5.0).floor() as u64;
        }
        // print line for this order
        result += &format!(
            " {}: {} ({} seats)\n",
            play_for(perf)["name"].as_str().unwrap(),
            usd(this_amount as f64 / 100_f64).format(),
            perf["audience"].as_u64().unwrap()
        );
        total_amount += this_amount;
    }
    result += &format!(
        "Amount owed is {}\n",
        usd(total_amount as f64 / 100_f64).format()
    );
    result += &format!("You earned {} credits\n", volume_credits);
    result
}

fn amount_for(performance: &Value, play: &Value) -> u64 {
    let mut result;
    match play["type"].as_str().unwrap() {
        "tragedy" => {
            result = 40000;
            if performance["audience"].as_u64().unwrap() > 30 {
                result += 1000 * (performance["audience"].as_u64().unwrap() - 30);
            }
        }
        "comedy" => {
            result = 30000;
            if performance["audience"].as_u64().unwrap() > 20 {
                result += 10000 + 500 * (performance["audience"].as_u64().unwrap() - 20);
            }
            result += 300 * performance["audience"].as_u64().unwrap();
        }
        play_type => {
            panic!("unknown type: {}", play_type);
        }
    }
    result
}

fn usd(value: f64) -> Currency {
    let opt = CurrencyOpts::new().set_symbol("$").set_precision(2);
    Currency::new_float(value, Some(opt))
}
