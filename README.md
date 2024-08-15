# tradingview-interactive-brokers
TradingView Interactive Brokers Integration using Webhooks

## Demo Video:

https://www.youtube.com/watch?v=zsYKfzCNPPU

## Prerequisites

* Requires redis, Python3, and packages installed

```
pip3 install -r requirements.txt
```

## Install Redis

```
brew install redis
brew servies start redis
ps aux | grep redis
```

## Start
Run Flask

```
export FLASK_APP=webapp
export FLASK_ENV=development
flask run
```

Run ngrok for global access
```
ngrok http 5000
ngrok http --domain=<static domain> 5000
```

Run broker deamon
```
python broker.py
```

## References, Tools, and Libraries Used:

* ngrok - https://ngrok.com - provides tunnel to localhost
* Flask - https://flask.palletsprojects.com/ - webapp
* Redis - https://pypi.org/project/redis/ - Redis client for Python
* ib_insync - https://ib-insync.readthedocs.io
* Redis pubsub - https://www.twilio.com/blog/sms-microservice-python-twilio-redis-pub-sub, https://redislabs.com/ebook/part-2-core-concepts/chapter-3-commands-in-redis/3-6-publishsubscribe/
* asyncio snippet - https://stackoverflow.com/questions/54153332/schedule-asyncio-task-to-execute-every-x-seconds
* ib_insyc examples - https://github.com/hackingthemarkets/interactive-brokers-demo/blob/main/order.py
