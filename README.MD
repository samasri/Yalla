# Yalla

Having lots of bad experiences with buses coming late after moving to Toronto, I create this project to calculate the average delay of YRT buses so that I can go at the right time to catch the bus. Using the real time GTFS data about their vehicle and stop positions, I calculate when does a bus passes each stop every day and compare it with the scheduled time. I intend to do this and over time, I would have enough data to get reliable delay averages.

## Dependency

* An account on leafletjs.com (the map API)

## Getting Started

1. Build the docker image from the Dockerfile: `docker build -t samasri/yalla .`
2. Start the docker container while exposing the `8080` port from docker to `49161` port on the host machine: `docker run -itdp 49161:8080 samasri/yalla`
3. Enter the docker: `docker exec -it [containerID] bash` (containerID is outputted from the `docker run` command)
4. Set up the database:
    1. Start the MySQL instance: `service mysql start`
    2. Set up the right user and create the tables: `mysql -u root < sql/start.sql`
    3. `sql/Stop.sql` and `sql/Delay.sql` can also be imported for a demo of how the website will look like after its populated with data:
        * `mysql -u root yallaDb < sql/Delay.sql`
        * `mysql -u root yallaDb < sql/Stop.sql`
5. Change the token in _static/token.js_ to a valid one.
6. Run the webiste: `cd webApp && npm start`. You can now access the website at `0.0.0.0:49161` from the host machine.

## How to Collect Data

In order for the website to give real data, it has to collect live GTFS data from YRT for a while (few days to a month). This data will be later used to calculate the average delay of buses on a specific route and stop. To collect the GTFS data:

1. Run `./mylib/getDistances.py >> results 2>> results-err`. This script collects data from YRT every 30 seconds and output them to a file.
2. Once enough data is collected, call `./mylib/processData.py results > Delay.sql`. This will process the data and output SQL instructions to populate the database.
3. Finally, run `mysql -u root yallaDb < Delay.sql` to insert the data to the MySQL database.
    * Make sure to delete any `Delay` table that was in the database from previous data collections. To delete the table, run `mysql -u root yallaDb` to enter the MySQL shell, and then run `DROP TABLE Delay;`.
    
## Testing

run ./test/test.py
    
## Screenshots

![image](https://user-images.githubusercontent.com/12204690/74210748-fa665700-4c5a-11ea-9261-b8316dcd3657.png)

![image](https://user-images.githubusercontent.com/12204690/74210808-3dc0c580-4c5b-11ea-9cf4-10158db9bf82.png)

![image](https://user-images.githubusercontent.com/12204690/74210832-54ffb300-4c5b-11ea-8f88-72b8aa56c11d.png)

## Assumptions

* My understanding is that in GTFS, each trip should be correlated with only one vehicle. However, in some cases, when collecting YRT data, I was finding 2 vehicles for the same trip. In these cases, I just dismiss the vehicles with longer distances since this seems to be a reporting error from YRT.
