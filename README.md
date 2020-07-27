# VicRoads_driving_test_appointments
This holds the script written in .py which scrape the vicroads website to find out the latest available appointments in all locations over Victoria and present them in an email

Purpose:
"Temporary visa holders who are already living in Victoria and haven't yet converted their licence(overseas to victorian licence), have six months from 29th October 2019 to do so." - SBS. This sets the final date as April 29, 2020 to convert the licence.

There are 3 tests which overseas licence holder must give in order to convert their licence. They are computer based test followed by Hazard perception and then drivers(practical) test. It is mandatory to have slots booked for all the tests and they are of "first come first serve" basis. As a result, most of the vicroads locations are now completely booked until mid of May 2020(as on 15 March 2020). But few might reschedule their appointment to another available slot in future. This gives the opportunity for the new member to occupy the vacant slot which is left open by the person who rescheduled.

The script is written to scrape the appointments(Next available) in each location of VicRoads office (so as to capture the reschedules) and present them in email.  It is then scheduled from an EC2 instance for every 30 min until my booking is made. 

