# Yalla

Having lots of bad experiences with bus schedules after moving to Toronto, I create this project to calculate the average delay of YRT buses to go at the right time to catch the bus. Using the real time GTFS data about their vehicle and stop positions, I calculate when does a bus passes each stop every day and compare it with the scheduled time. I intend to do this and over time, I would have enough data to get reliable delay averages.

## Notes

* My understanding is that in GTFS, each trip should be correlated with only one vehicle. However, in some cases, when collecting YRT data, I was finding 2 vehicles for the same trip. In these cases, I just dismiss the vehicles with longer distances since this seems to be a reporting error from YRT.
