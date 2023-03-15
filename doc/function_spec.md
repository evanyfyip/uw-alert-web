# Background
The purpose of this application is to display alerts from the UW Alert System on a map of U-District, inclusing a heatmap and trends of areas/times.
The current alert system informs users on a mailing list via email. We intend to provide a visualization of these alerts.

# User Profiles
## User 1: UW Student
- Wants: Check incidents around their commute to class and back.
- Interaction Methods: Use application
- Needs: Current location, incident locations
- Skills: Know how to navigate a website interface.

## User 2: UW Alerts Staff
- Wants: Check that alerts display correct location and information.
- Interaction Methods: Admin interface
- Needs: Admin previliges and interface
- Skills: Know how to send alert through UW Alert System, generally knows U-District location

# Data Sources
## [Seattle GeoData](https://data-seattlecitygis.opendata.arcgis.com/datasets/SeattleCityGIS::seattle-streets-3/explore?location=47.609360%2C-122.325916%2C14.88)
Contains geospatial street data for the Seattle area.

## [UW Alerts Blog](https://emergency.uw.edu/?_gl=1*ztz313*_ga*MzIwNzY5MTg2LjE2NjU4NzU5NjU.*_ga_3T65WK0BM8*MTY3NjMyNTM5Ny4yMS4wLjE2NzYzMjU0MDEuMC4wLjA)
A collection of text reports from the UW Alert system. The reports were typed out manually. We will use a text parser to extract necessary information for our application.

# Use Cases
## Objective: User checks if their usual commute is safe
- User: I am walking home late after class, what area(s) should I avoid to stay safe?
- Application: When opening the app, the user can see a map of the U-District area with markers indicating alerts within the past 4 hours.

## Objective: User checks if a recent incident is resolved
- User: There was an alert 2 hours ago. Has the incident resolved?
- Application: Users can click on the markers within the app. A popup will show the alert incident type and the side panel will display text from the UW Alert Blog along with any updates.
