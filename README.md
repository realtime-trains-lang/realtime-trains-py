# RealTime Trains API Python Module

Maintained by [@anonymous44401](https://github.com/anonymous44401)

## Current version: [V0.0.0 [Alpha]](https://github.com/anonymous44401/realtime-trains-py/releases/tag/v0.0.0-alpha)

## Contents

- [About](https://github.com/anonymous44401/realtime-trains-py/#about)
- [Setup](https://github.com/anonymous44401/realtime-trains-py/#setup)
- [Documentation](https://github.com/anonymous44401/realtime-trains-py/#documentation)
- [Errors](https://github.com/anonymous44401/realtime-trains-py/#errors)

## About

Soon

## Setup

Running the realtime-trains-py module locally on your machine will require you to implement a things before you can start. You don't need to do this if you have installed in package using `pip install realtime-trains-py`

The first step is to create a file called `.env` in the `authentication` folder. This will allow the package to collect your username and password without you having to enter it each time.
Set up your file like this:

```
api_username = "[your_username]"

api_password = "[your_password]"
```

> [!IMPORTANT]
> Keep your username and password private.

Ensure you change the respective fields above to contain your username and password.

Next, you need to initialise the package. You need to assign `RealtimeTrainsPy()` to a variable of your choosing.

```
your_var = RealtimeTrainsPy()
```

RealtimeTrainsPy() takes zero (0), two (2) or three (3) arguments.

```
your_var = RealtimeTrainsPy(complexity = "", username = "", password = "")
```

> [!IMPORTANT]
> Make sure you provide both your username and password, or you won't be able to access the API.

### Complexities:

Simple

> Simple mode provides you with access to some data the API has to offer.
> Simple mode only allows you to view data fom seven (7) days before the current date and 80 days after the current date. Any data you get from the API will be formatted so you can understand it.  
> This is recommended for users who don't want to see all the nerdy train stuff.

Advanced

> Advanced mode provides you with access to most data the API has to offer.
> This is recommended for users who want to see all the nerdy train stuff, but with the same restrictions as simple mode.

Complex

> Complex mode provides you with access to all data the API has to offer.
> Complex mode offers no restrictions to what you can access, however it does not format any data for you. Other modes will provide data in a set format, but complex mode will only provide you data in json format.

### Don't have a username or password?

To get a username and password, head over to the [api portal](https://api.rtt.io/) and select register. Follow the appropriate steps on the site.
Once logged in, you'll be directed to the API Home Page. This page shows you your API auth credentials - these are the details you'll use to access the API.
Your username is prefixed with `rttapi_` and your password will be a 40 character hex string.

> [!IMPORTANT]
> Keep your username and password private.

## Documentation

### get_departures()

Details...

### get_arrivals()

Details...

### get_service()

The `get_service()` method takes one (1) or two (2) positional arguments. These are:

- `service_uid` -> string eg G54072
- `date` -> specified as a string eg 16/11/2024 (Support for specific times will be added soon)

The `date` argument is optional, and will be defaulted to the current date (UTC) if left blank.

The `get_service()` method returns a list of departures. The amount of data returned will depend on the complexity you specified upon initialising the package. The complexity defaults to “s” (simple) if not specified.

## Errors:

### Service UID not recognised.

> ```
> Service UID not recognised.
> Status code: 404
> ```
>
> This error means that the Service UID you entered doesn't match any service on the server. The Service UID should be a 6-character string. It should start with one (1) letter (not case-sensitive) followed by five (5) integers.. For example G54072 - which is the Service UID for 9J35. The package will return the error shown above if you provide the headcode (9J35 in this case). Due to API limitations, Service UIDs must be provided instead.

### Access blocked.

> ```
> Access blocked: check your credentials.
> Status code: 401 | 403
> ```
>
> This error means that the credentials you provided when you initialised the package were unable to be verified by the API server. If your credentials are correct and you are unable to access the API, you should contact the API support via the [api portal](https://api.rtt.io/). This error is unlikely to be a problem with realtime-trains-py.
> If you have recently registered it may take a while for your details to be verified before you can access the API.
> If this problem persists, visit the [api portal](https://api.rtt.io/) for support. You can also [report an issue](https://github.com/anonymous44401/realtime-trains-py/issues) with realtime-trains-py on GitHub so that our system can be checked.

### Invalid date.

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
