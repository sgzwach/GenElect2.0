# GenElect2.0
New and improved GenCyber Elective application for DSU GenCyber

To run:

`python3 run.py`

## Todo - Break these out into further tasks as we go 
- [X] Homepage (with notifications)
- [X] Admin page
- [X] Create User page
- [X] Create elective page
- [X] Create offering page
- [X] Create notification/announcment
- [X] Allow offering to select elective base
- [X] Scheduler page
- [X] Build DB
- [X] Prerequisites and Completed Electives (disabling repeats)
- [X] Remove completions on elective delete
- [X] Allow non-authenticated users to view electives
- [X] Offerings Templates
- [X] Bulk User Import (from text document possibly)
- [X] Create elective field that allows it to be repeated
- [X] Student Elective search box
- [X] Non-registered user list
- [X] Stats Page (possibly featuring: # of registered/unregistered students, # of open seats, full electives, etc)
- [X] Overall Camp Schedule
- [X] Redirect correctly after editing feature or dropping from elective
- [X] Show registered electives when looking at a students information, add schedule button
- [X] Solve same day registered prereq situations (registered but not completed a prereq)
- [X] Allow admins to set a Registration timeline
- [ ] Utilize LDAP for Domain Auth ?
- [X] Create field that allows elective to be taken more than once
- [X] Check current registrations for prereq completions
- [X] Remove registrations with prereq registrations are dropped
- [X] Allow admins and instructors to drop students from classes
- [X] Decide if registrations should be manually or automatically converted to completions (currently manual, see 'Complete' button within allofferings view)
- [X] Fix change password in user update bug
- [X] Add Favicon
- [X] Allow mobile users to add page to homescreen using: mobile-web-app-capable and apple-mobile-web-app-capable
- [ ] Enable mobile app push notificaitons (possibly something for next year)
- [X] Add core courses
- [X] Enable core courses to be registered for by CSV upload
- [X] Allow admins to change a users set of core registrations
- [X] Add roll call for the new core courses
- [X] Order the core courses on each students schedule by core period
- [X] Add link to campus map
- [X] Fix core errors when changing user roles (students to admins primarily)
- [X] Make instructor page so that student helpers know what they can do
- [X] Add difficulty drop-downs for electives and cores
- [X] Add a learning objective for each elective
- [X] Move buttons to create new items to the top of each admin page (so scrolling isn't necessary)
- [X] Hash the stored passwords for all users



To run tests:
From the root directory
- `coverage run --source . --omit tests/* -m "tests.test_basic"`
- `coverage html`

This will generate html reports with code coverage information
Still needs work