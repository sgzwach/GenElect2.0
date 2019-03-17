# GenElect2.0
New and improved GenCyber Elective application for DSU GenCyber

To run:

`python3 run.py`

## Todo - Break these out into further tasks as we go 
- [X] Homepage (with notifications)
- [X] Admin page
- [X] Create User page
- [X] Create elective page
- [X] Scheduler page
- [X] Build DB
- [X] Prerequisites and Completed Electives
- [ ] Offerings Templates
- [ ] Multiple User Creation (from text document possibly)   



To run tests:
From the root directory
- `coverage run --source . --omit tests/* -m "tests.test_basic"`
- `coverage html`

This will generate html reports with code coverage information
Still needs work