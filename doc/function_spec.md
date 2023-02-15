# Background
The purpose of this application is to display alerts from the UW Alert System on a map of U-District, inclusing a heatmap and trends of areas/times.
The current alert system informs users on a mailing list via email. We intend to provide a visualization of these alerts.

# User Profiles
## User 1: UW Student
Wants: Check incidents around their commute to class and back.
Interaction Methods: Use application
Needs: Current location, incident locations
Skills: Know how to navigate a website interface.

## User 2: U-District Resident
Wants: Check incidents around their commute to places in U-District.
Interaction Methods: Use application
Needs: Current location, incident locations
Skills: Know how to navigate a website interface.

## User 3: UW Alerts Staff
Wants: Check that alerts display correct location and information.
Interaction Methods: Admin interface
Needs: Admin previliges and interface
Skills: Know how to send alert through UW Alert System, generally knows U-District location

# Data Sources
## [Seattle GeoData](https://data-seattlecitygis.opendata.arcgis.com/datasets/SeattleCityGIS::seattle-streets-3/explore?location=47.609360%2C-122.325916%2C14.88)

## [UW Alerts Blog](https://emergency.uw.edu/?_gl=1*ztz313*_ga*MzIwNzY5MTg2LjE2NjU4NzU5NjU.*_ga_3T65WK0BM8*MTY3NjMyNTM5Ny4yMS4wLjE2NzYzMjU0MDEuMC4wLjA)

# Use Cases
## Objective: User checks if their usual commute is safe
- User: Where is my location?
- Application: Displays the user's current location on a map
- User: Are there any incidents present on street X?
- Application: There is an incident on street X?
- User: How long ago was the incident?
- Application: The incident happened 4 hours prior.
- User: How dangerous was the incident?
- Application: The alert was for suspiscious behavior.

## Objective: User Verification
- Application: Displays login page
- User: Inserts username and password into the respective fields and submits
- Application: If correct, show application home page
-              If incorrect, display "incorrect user credentials" and display blank login page.
