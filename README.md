# Realtime Trains API Python Module

Maintained and managed by members of [realtime-trains-lang](https://github.com/realtime-trains-lang).

![PyPI](https://img.shields.io/pypi/v/realtime-trains-py) ![License](https://img.shields.io/github/license/realtime-trains-lang/realtime-trains-py) ![Issues](https://img.shields.io/github/issues/realtime-trains-lang/realtime-trains-py)


### Check out our [release notes.](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Release-Notes)

### Read the [documentation.](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Home)

## About this package

**realtime-trains-py** is an open-source python API Wrapper designed to allow you to access data directly from the Realtime Trains API, in a simple and user-friendly way. This package includes five different [complexity modes](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Complexity) that allow you to customise how you want to see the data provided by the API.

This package can be used for anything railway related, whether you're a rail enthusiast or commuter, this package can be used for all your purposes. The package can be used in **personal** applications or for **personal** rail data access. For **commercial** use, you should contact [Realtime Trains](https://www.realtimetrains.co.uk/). More information can be found on their [API home page](https://api.rtt.io)

This package is not affiliated with [Realtime Trains](https://www.realtimetrains.co.uk/). 

## What can I do with this package?
This package allows you to access data directly from the [Realtime Trains API](https://api.rtt.io) using one of [five complexities](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Complexity). Each complexity mode gives you access to different access to the data the API offers. 

For the most flexibility, you can use **simple** mode, the recommended mode. Simple mode allows you to access a fair amount of the data available from the Realtime Trains API. This mode is recommended for those that want a manageable amount of information while keeping it easy to read. Use `complexity="s"`.

For the most freedom with the API, you can use **complex** mode. Complex mode lets you access all the data available from the Realtime Trains API. This mode does not format any data for you - it creates new `.json` files with the data you requested. This mode is recommended for those who have a good understanding of python and managing json files. Use `complexity="c"`.

For a balance of freedom and flexibility, you can use **advanced** mode. Advanced mode allows you to access most of the data available from the Realtime Trains API. This mode is recommended for those that want to see a bit more information, but like to keep things easy to read. Use `complexity="a"`.

Using advanced and simple mode, you can optionally select between prettier or normal mode. The default, prettier mode, gives you your data in a nicely formatted table, while normal mode gives you your data as a list of objects, so you'll need to get the data out of the objects yourself. To use a normal mode, use `complexity="s.n"` or `complexity="a.n"`. Don't worry though! If you're confused, we have plenty of [documentation](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Home) to help you out.


## Installation Instructions

To install the package, simply run the following command in your terminal:
```
$ pip install realtime-trains-py
``` 
Alternatively, you can clone, fork or download the [repository](https://github.com/realtime-trains-lang/realtime-trains-py) onto your device. 

Once installed, you can import the package. Place the lines below in your file or you can run them directly in your terminal.
```python
from realtime_trains_py import RealtimeTrainsPy

rtt = RealtimeTrainsPy(
    username="<your_username>", 
    password="<your_password>", 
    complexity="<your_choice>"
)
```

Check out our full [setup guide](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Setup) for more help setting up.

You'll need an account for the [Realtime Trains API](https://api.rtt.io) to use this package. You can sign up for free at the [API home page](https://api.rtt.io). 


## Examples

#### Get Live *(New for version 2025.3.0)*
###### The example below will display a live departure board for Ely. 
```python
rtt.get_live(tiploc="ELYY")
```

#### Get Departures
###### The example below will return up to 15 rows on the departure board for London King's Cross at the time you run the program. 
```python
rtt.get_departures(tiploc="KNGX", rows=15)
```

#### Get Arrivals
###### The example below will return up to 15 rows on the arrivals board for London King's Cross at the time you run the program. 
```python
rtt.get_arrivals(tiploc="KNGX", rows=15)
```

#### Get Service
###### The example below will return the service information of G28171 (2H18 0958 London Liverpool Street to Cambridge North) at the time you run the program. 
```python
rtt.get_service(service_uid="G28171")
```

#### Get Station
###### The example below will return up to 30 rows of departures and arrivals for London King's Cross at the time you run the program. 
```python
rtt.get_station(tiploc="KNGX", rows=15)
```

More in-depth examples can be found on our [examples page](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Examples). 


## Licensing 

The **realtime-trains-py** API Wrapper uses an MIT License.

All data is kindly provided by [Realtime Trains](https://www.realtimetrains.co.uk/) through the [Realtime Trains API](https://api.rtt.io).