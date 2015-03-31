
## Xavee.net

![alt text](https://s3-ap-northeast-1.amazonaws.com/xavee/static/img/xavee-screenshot.png "Screenshot of the app in action")

[Xavee.net](https://www.xavee.net) is an attempt at automatically curating games on the various mobile app stores.
It is commonly agreed that it is extremely difficult to find good games on these stores,
as stores are profit-oriented and therefore tend to promote only those games that will make them the most money
(i.e. games with so many IAPs that they're practically unplayable).
Xavee's goal is to promote diamonds in the rough by re-ranking games by their quality rather than profitability,
and offer comprehensive filtering tools to browse and find games more efficiently.

It is still an early version of the site, so a lot of needed functionality is not implemented yet.
For now, only the iTunes Appstore is supported (unification with Google Play is planned), and the ranking methods are still unfinished.
The site is available in English and Japanese.

## Rankings

Xavee will offer a suite of different ways to rank games on the stores, which can then be drilled down into
by filtering by country, category, price, whether the game has IAPs or not, and so on.
At this point in time, three rankings are implemented:

* *Worldwide iTunes Rankings*: this is the iTunes top free/paid/grossing ranking browsable and comparable by 13 countries. It is updated once per day.

* *Xavee Rankings*: games ranked with a custom scoring algorithm. At the moment this is a simple Bayesian average 
of the average iTunes rating across 13 countries. Planned additions are analysis of reviews and ratings to detect vote faking
and penalize the scores of these games accordingly, penalties for games that have IAPs on top of being paid, penalties for excessive IAPs, etc.

* *Developer rankings*: currently a Bayesian average of the Xavee scores of a developer's games.

## API
A public API is available for developers to include data from Xavee.net into their applications.
A comprehensive reference document is planned. For now, the API is browsable through the interface provided by the Django REST Framework.
