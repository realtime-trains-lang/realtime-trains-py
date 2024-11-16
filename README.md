# RealTime Trains API Python Module

Maintained by [@anonymous44401](https://github.com/anonymous44401)

## Current version: [V0.0.0 [Alpha]](https://github.com/anonymous44401/realtime-trains-py/releases/tag/v0.0.0-alpha)

## Contents

- [About](https://github.com/anonymous44401/realtime-trains-py-v2/#about)
- [Setup](https://github.com/anonymous44401/realtime-trains-py-v2/#setup)
- [Documentation](https://github.com/anonymous44401/realtime-trains-py-v2/#documentation)

## About

Soon

## Setup

Running the realtime-trains-py module locally on your machine will require you to implement a things before you can start.

The first step is to create a file called `.env` in the `authentication` folder. This will allow the package to collect your username and password without you having to enter it each time.
Set up your file like this:

```
api_username = "[your_username]"

api_password = "[your_password]"
```

> [!IMPORTANT]
> Keep your username and password private.

Ensure you change the respective fields above to contain your username and password.

### Don't have a username or password?

To get a username and password, head over to the [api portal](https://api.rtt.io/) and select register. Follow the appropriate steps on the site.
Once logged in, you'll be directed to the API Home Page. This page shows you your API auth credentials - these are the details you'll use to access the API.
Your username is prefixed with `rttapi_` and your password is a 40 character hex string.

> [!IMPORTANT]
> Keep your username and password private.

## Documentation

### get_departures()

Details...

### get_arrivals()

Details...

### get_service()

Details...
