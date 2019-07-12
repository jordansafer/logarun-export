# Logarun to Strava

## Usage:
1. First, you need to **register an application with the Strava API service.** Go to the [Strava API Management Page](https://www.strava.com/settings/api), and create a new application. Note the Client ID and Client Secret - you will need them later.
2. Clone this project
3. Open Terminal and go to the project folder (use cd)
4. **pip install -r requirements.txt**
5. **python main.py**
6. Enter info (logarun info, date range, Strava ID & Secret)

UI is trashy (you need to click some buttons twice) because PySimpleGUI doesn't work well for Mac.

**Note:**
Strava only allows 600 logs every 15 minutes, so the program will space them out.

## References
Derived from @elliothevel's [logarun exporter](https://github.com/elliothevel/logarun-export) and @barrald's [strava uploader](https://github.com/barrald/strava-uploader)

Uses the Strava v3 API (documented [here](http://strava.github.io/api/)) to upload CSV activities exported from logarun/flotrack.

Borrows liberally from @anthonywu's [Strava API Experiment](https://github.com/anthonywu/strava-api-experiment) and @marthinsen's [Strava Upload](https://github.com/marthinsen/stravaupload) projects. Uses @hozn's [stravalib](https://github.com/hozn/stravalib) to interact with the Strava API. Thanks to all.

XML parsing from https://www.geeksforgeeks.org/xml-parsing-python/
