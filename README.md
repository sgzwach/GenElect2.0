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
- [ ] Bulk User Import (from text document possibly)
- [X] Create elective field that allows it to be repeated
- [ ] Student Elective search box (should auto refresh)
- [X] Non-registered user list
- [ ] Stats Page (possibly featuring: # of registered/unregistered students, # of open seats, full electives, etc)
- [ ] Overall Camp Schedule
- [X] Redirect correctly after editing feature or dropping from elective
- [X] Show registered electives when looking at a students information, add schedule button
- [X] Solve same day registered prereq situations (registered but not completed a prereq)
- [X] Allow admins to set a Registration timeline
- [ ] Utilize LDAP for Domain Auth ?
- [X] Create field that allows elective to be taken more than once
- [X] Check current registrations for prereq completions
- [X] Remove registrations with prereq registrations are dropped
- [X] Allow admins and instructors to drop students from classes
- [ ] Decide if registrations should be manually or automatically converted to completions
- [X] Fix change password in user update bug




To run tests:
From the root directory
- `coverage run --source . --omit tests/* -m "tests.test_basic"`
- `coverage html`

This will generate html reports with code coverage information
Still needs work