# RealTime Trains API Python Module

Maintained by [@anonymous44401](https://github.com/anonymous44401)

![PyPI](https://img.shields.io/pypi/v/realtime-trains-py) ![License](https://img.shields.io/github/license/anonymous44401/realtime-trains-py) ![Issues](https://img.shields.io/github/issues/anonymous44401/realtime-trains-py)


### View our [latest release](https://github.com/anonymous44401/realtime-trains-py/releases)

[Documentation](https://github.com/anonymous44401/realtime-trains-py/wiki/Home)

## About this package

**realtime-trains-py** is an open-source python API Wrapper designed to allow you to access data directly from the Realtime Trains API, in a simple and user-friendly way. This package includes 5 different complexity modes that allow you to decide how you want to see the data provided by the API.

This package can be used for anything railway related, whether you're a rail enthusiast or commuter, this package can be used for all your purposes. The package can be used in personal applications or for personal rail data access. 

This package is not affiliated with [Realtime Trains](https://www.realtimetrains.co.uk/).

## What can I do with this package?
This package allows you to access data directly from the Realtime Trains API using one of 5 [complexities](https://github.com/anonymous44401/realtime-trains-py/wiki/Complexity). Each complexity mode gives you access to different data the API offers. 

For the most freedom with the API, you can use **complex** mode. Complex mode lets you access all the data available from the Realtime Trains API. This mode does not format any data for you - it creates new .json files with the data you requested. This mode is recommended for those who have a good understanding of python and managing json files.

For a mix of freedom and flexibility, you can use **advanced** mode. Advanced mode allows you to access most the data available from the Realtime Trains API, but it comes with a time constraint. You can't request data more than 7 days prior to the current date nor 80 days after the current date. 

For the most flexibility, you can use **simple** mode. Simple mode allows you to access lots the data available from the Realtime Trains API, but it comes with a time constraint. You can't request data more than 7 days prior to the current date nor 80 days after the current date. 

Using advanced and simple mode, you can optionally select between prettier or normal mode. Prettier mode gives you your data in a nicely formatted table, while normal mode gives you your data as a list of objects, so you'll need to get the data out of the objects yourself. Don't worry though! If you're confused, we have plenty of [documentation](https://github.com/anonymous44401/realtime-trains-py/wiki/Home) to help you out! 


## Installation Instructions

To install the package, simply run the following command in your terminal:
```
$ pip install realtime-trains-py
``` 
Alternatively, you can clone, fork or download the [repository](https://github.com/anonymous44401/realtime-trains-py) onto your device. 

Once installed, you can import the package. Place the lines below in your file, or you can run them directly in your terminal.
```python
from realtime_trains_py import RealtimeTrainsPy

rtt = RealtimeTrainsPy(username = "your_username", password = "your_password", complexity = "c")
```

Check out the [documentation](https://github.com/anonymous44401/realtime-trains-py/wiki/Home) for more help setting up.

You need an account for the Realtime Trains API to use this package. You can sign up for free at the [API home page](https://api.rtt.io). 


## Examples of this package

The example below will return you up to 15 rows on the departure board for London King's Cross at the time you run the program. 
```python
rtt.get_departures(tiploc = "KNGX", rows = 15)
```

The example below will return you up to 15 rows on the arrivals board for London King's Cross at the time you run the program. 
```python
rtt.get_arrivals(tiploc = "KNGX", rows = 15)
```

More in-depth examples can be found on our [GitHub wiki](https://github.com/anonymous44401/realtime-trains-py/wiki/Home). 


## License

The **realtime-trains-py** API Wrapper uses an MIT License.