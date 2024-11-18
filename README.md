# RealTime Trains API Python Module

Maintained by [@anonymous44401](https://github.com/anonymous44401)

Last updated: 18/11/2024 22:34 UTC

### Current version: [V0.0.1 [Alpha]](https://github.com/anonymous44401/realtime-trains-py/releases/tag/v0.0.0-alpha)

## Contents

- [About](https://github.com/anonymous44401/realtime-trains-py/#about)
- [Setup](https://github.com/anonymous44401/realtime-trains-py/#setup)
- [Documentation](https://github.com/anonymous44401/realtime-trains-py/#documentation)
- [Errors](https://github.com/anonymous44401/realtime-trains-py/#errors)

## About

Soon

## Setup

Running the realtime-trains-py package locally on your machine will require you to implement a few things before you can start. You can skip step one (1) if you have installed the package using `pip install realtime-trains-py`.

### Step one (1)

The first step is to create a file called `.env`. You should add this file into the `authentication` folder. This will allow the package to reference your username and password without you having it on display in your code. [I don't have a username or password.](https://github.com/anonymous44401/realtime-trains-py/#i-dont-have-a-username-or-password)

> [!IMPORTANT]
> Keep your username and password private.

Set up your file like this:

```
api_username = "your_username"

api_password = "your_password"
```

Ensure you change the respective fields above to contain your username and password, or the package won't work and you'll receive and error.

### Step two (2)

The second step, is to initialise the package. To do this, you'll need to make a new python file: `your_file.py`. In this file, you'll need to import `realtime_trains_py` and assign `RealtimeTrainsPy()` to a variable of your choosing, like below.

```
from [tbc] import [tbc]

your_var = RealtimeTrainsPy()
```

When you initialise RealtimeTrainsPy(), you can provide between zero (0) and three (3) arguments, like below.

```
your_var = RealtimeTrainsPy(complexity = "", username = "your_username", password = "your_password")
```

> [!IMPORTANT]
> Make sure you provide both your username and password together, or you won't be able to access the API.

Your final step is the try running the program. If you have followed this setup guide correctly, you shouldn't receive any [errors](https://github.com/anonymous44401/realtime-trains-py/#errors). If you receive an error, re-read the setup guide and [report an issue](https://github.com/anonymous44401/realtime-trains-py/issues) with realtime-trains-py on GitHub so that we can check our systems.

### Complexities:

Simple (s)

> Simple mode provides you with access to some data the API has to offer. This mode only allows you to view data fom seven (7) days before the current date and 80 days after the current date. Any data you request from the API will be formatted so you can understand and read it.
>
> This is recommended for users who don't want to see all the nerdy train stuff.

Advanced (a)

> Advanced mode provides you with access to most data the API has to offer. This mode only allows you to view data fom seven (7) days before the current date and 80 days after the current date. Any data you request from the API will be formatted so you can understand and read it.
>
> This is recommended for users who want to see all the nerdy train stuff, but with similar restrictions as simple mode.

Complex (c)

> Complex mode provides you with access to all data the API has to offer. This mode offers no restrictions to what you can access, however it does not format any data for you. Other modes will provide data in a set format, but complex mode will only provide you data as a new .json file.
>
> This mode is recommended for anyone with understanding of json files and who wants to see all the nerdy train stuff.

### I don't have a username or password

To get a username and password, head over to the [api portal](https://api.rtt.io/) and select register. Follow the appropriate steps on the site.
Once logged in, you'll be directed to the API home page. This page shows you your API auth credentials - these are the details you'll use to access the API.
Your username is prefixed with `rttapi_` and your password will be a 40 character hex string. Copy these details and paste them into your code.

> [!IMPORTANT]
> Keep your username and password private.

## Documentation

### get_departures()

Details...

### get_arrivals()

Details...

### get_service()

The `get_service()` method takes one (1) or two (2) positional arguments. These are:

- `service_uid` (a string) - like G54072
- `date` (a string) - like 2024/11/16 (Support for specific times will be added soon)

The `date` argument is optional. I will be defaulted to the current date (UTC) if left blank.

The `get_service()` method returns a list of departures. The amount of data returned will depend on the complexity you specified upon initialising the package. The complexity defaults to “s” (simple) if not specified.

## Errors:

### Service UID not Recognised

> ```
> Service UID not recognised.
> Status code: 404
> ```
>
> This error means that the Service UID you entered doesn't match any service on the server. The Service UID should be a 6-character string. It should start with one (1) letter (not case-sensitive) followed by five (5) integers.. For example G54072 - which is the Service UID for 9J35. The package will return the error shown above if you provide the headcode (9J35 in this case). Due to API limitations, Service UIDs must be provided instead.

### Access Blocked

> ```
> Access blocked: check your credentials.
> Status code: 401 | 403
> ```
>
> This error means that the credentials you provided when you initialised the package were unable to be verified by the API server. If your credentials are correct and you are unable to access the API, you should contact the API support via the [api portal](https://api.rtt.io/). This error is unlikely to be a problem with realtime-trains-py.
> If you have recently registered it may take a while for your details to be verified before you can access the API.
> If this problem persists, visit the [api portal](https://api.rtt.io/) for support. You can also [report an issue](https://github.com/anonymous44401/realtime-trains-py/issues) with realtime-trains-py on GitHub so that we can check our systems.

### Invalid Date

> ```
> Date provided did not meet requirements or fall into the valid date range.
> ```
>
> This error means that a date you provided was not accepted by the system. Your date should be provided in the form dd/mm/yyyy, and not be more than eight (8) days before the current date or more than 80 days after the current date.
> For example, on the 9th January 2025 (09/01/2025), the earliest date that can be requested is the 2nd January 2025 (02/01/2025) and the latest date is the 30th March 2025 (30/03/2025)

> [!TIP]
> Turn on complex mode to bypass this error. Complex mode allows you to access more data.

> [!WARNING]
> Dates requested that are more than two (2) weeks after the current date are unlikely to be representative or accurate of the timetable on that day.

### Missing Details

> ```
> Missing details. Both username and password must be provided. Only one field was provided.
> ```
>
> This error means that you didn't pass in a username and a password when you initialised the package. Make sure you read the [setup guide](https://github.com/anonymous44401/realtime-trains-py/#setup) before running your code.
> If this problem persists and you have correctly followed the setup guide, [report an issue](https://github.com/anonymous44401/realtime-trains-py/issues) with realtime-trains-py on GitHub so that we can check our systems.

### Complexity not Recognised

> ```
> Complexity not recognised. Select a valid type.
> ```
>
> This error means that you didn't select a valid complexity type when you initialised the package. Make sure you read the [setup guide](https://github.com/anonymous44401/realtime-trains-py/#setup) before running your code.
> If this problem persists and you have correctly followed the setup guide, [report an issue](https://github.com/anonymous44401/realtime-trains-py/issues) with realtime-trains-py on GitHub so that we can check our systems.
