# TradingView Bracket Order Webhook

Webhook endpoint for TradingView alerts.

## Getting Started

This project contains a Chalice based webhook that accepts TradingView alerts with a JSON payload. The webhook executes a bracket order taking loss at 2% and profit at 4%.

### Prerequisites

This project requires a Python 3.7 venv and Chalice installed. Create and activate the venv:

```
$ python3 -m venv venv37
$ . venv37/bin/activate
```

Next, you can install the Chalice module in the virtual environment

```
$(venv) python3 -m pip install chalice
```

Finally, clone this repo into your virtual environment

```
$(venv) git clone git@github.com:GoldUniform/tradingview-webhook.git
```

You will also need a TradingView alert setup to use a webhook with the following payload:

```
{
    "open": {{open}},
    "high": {{high}},
    "low": {{low}},
    "close": {{close}},
    "exchange": "{{exchange}}",
    "ticker": "{{ticker}}",
    "volume": {{volume}},
    "time": "{{time}}",
    "timenow": "{{timenow}}",
    "action": "{{strategy.order.action}}"
}
```

### Set up

Enter the virtual environment

```
$ . venv37/bin/activate
$ cd tradingview-webhook
```

Copy the config sample and fill in the values for your TradingView account

```
$ cp config_sample.py config.py
```

## Deployment

```
$(venv) chalice deploy
Creating deployment package.
Creating IAM role: tradingview-webhook
Creating lambda function: tradingview-webhook-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:tradingview-webhook-dev
  - Rest API URL: https://abcd.execute-api.us-west-2.amazonaws.com/api/
```

The deployment will output your public URL, use that URL for your TradingView webhook endpoint.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details