# Overpass

This program displays information about the International Space Station. With the press of a button you can see the current crew and exact position at that moment.

## Features
- Displays ISS position
- Displays the crew on the ISS
- Saves data to a database

## Requirements
- Python 3.10+
- PIP to install packages

## How to run
Start the program and click the "Fetch" button to retrieve information.

## API
The API used is Open Notify. It provides information about the ISS longitude and latitude, as well as the number of crew members, their names and which spacecraft they are assigned to.

## Database
The following is saved on each fetch: longitude, latitude, date and time, and crew count.

## Reflection
I ran into some issues during development. One problem was that the API returned all people currently in space, including the crew on Tiangong. I solved this by filtering to only include crew members on the ISS.

This was one of the more challenging projects I have worked on, but probably the one I am most proud of. It was a great learning experience and it took a while to get the logic to come together properly.
