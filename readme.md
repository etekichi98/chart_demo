
# 使い方


株価チャートハイsンサーバを起動する
~~~
$ cd chart_demo
$ docker-compose up -d --build
~~~

次のurlを叩くと、ブラウザに以下のの画面が出る

http://サーバ:5000/list

![chart.png](./chart.png)

個別のチャートのurlは、以下のようなかんじ

http://サーバ:5000/candle?code=1332&term=100&volume=True


