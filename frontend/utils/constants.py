"""Constants for the CrossFit application.

This module defines constants including font families and event metadata
for all CrossFit performance metrics.
"""

FONT_FAMILY = 'Libertinus Sans, sans-serif'

EVENT_MAPPING = {
    'athlete_id': {
        'display_name': 'Athlete ID',
        'better': 'neither',
        'unit': '',
        'description': 'Unique identifier for each athlete',
    },
    'name': {
        'display_name': 'Name',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete name',
    },
    'region': {
        'display_name': 'Region',
        'better': 'neither',
        'unit': '',
        'description': 'Geographic region',
    },
    'team': {
        'display_name': 'Team',
        'better': 'neither',
        'unit': '',
        'description': 'Team affiliation',
    },
    'affiliate': {
        'display_name': 'Affiliate',
        'better': 'neither',
        'unit': '',
        'description': 'CrossFit affiliate gym',
    },
    'gender': {
        'display_name': 'Gender',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete gender',
    },
    'age': {
        'display_name': 'Age',
        'better': 'neither',
        'unit': 'years',
        'description': 'Athlete age',
    },
    'height': {
        'display_name': 'Height',
        'better': 'neither',
        'unit': 'inches',
        'description': 'Athlete height',
    },
    'weight': {
        'display_name': 'Weight',
        'better': 'neither',
        'unit': 'lbs',
        'description': 'Athlete weight',
    },
    'fran': {
        'display_name': 'Fran',
        'better': 'lower',
        'unit': 'seconds',
        'description': 'Time to complete 21-15-9 reps of thrusters and pull-ups',
    },
    'helen': {
        'display_name': 'Helen',
        'better': 'lower',
        'unit': 'seconds',
        'description': 'Time to complete 3 rounds of 400m run, 21 kettlebell swings, 12 pull-ups',
    },
    'grace': {
        'display_name': 'Grace',
        'better': 'lower',
        'unit': 'seconds',
        'description': 'Time to complete 30 clean & jerks at 135/95 lbs',
    },
    'filthy50': {
        'display_name': 'Filthy 50',
        'better': 'lower',
        'unit': 'seconds',
        'description': 'Time to complete 50 reps of each exercise',
    },
    'fgonebad': {
        'display_name': 'Fight Gone Bad',
        'better': 'higher',
        'unit': 'reps',
        'description': 'Total reps across 3 rounds of wall balls, sumo deadlift high pulls, box jumps, push presses, and rowing',
    },
    'run400': {
        'display_name': '400m Run',
        'better': 'lower',
        'unit': 'seconds',
        'description': 'Time to complete 400 meter run',
    },
    'run5k': {
        'display_name': '5K Run',
        'better': 'lower',
        'unit': 'seconds',
        'description': 'Time to complete 5 kilometer run',
    },
    'candj': {
        'display_name': 'Clean & Jerk',
        'better': 'higher',
        'unit': 'lbs',
        'description': 'Maximum weight for clean & jerk',
    },
    'snatch': {
        'display_name': 'Snatch',
        'better': 'higher',
        'unit': 'lbs',
        'description': 'Maximum weight for snatch',
    },
    'deadlift': {
        'display_name': 'Deadlift',
        'better': 'higher',
        'unit': 'lbs',
        'description': 'Maximum weight for deadlift',
    },
    'backsq': {
        'display_name': 'Back Squat',
        'better': 'higher',
        'unit': 'lbs',
        'description': 'Maximum weight for back squat',
    },
    'pullups': {
        'display_name': 'Pull-ups',
        'better': 'higher',
        'unit': 'reps',
        'description': 'Maximum number of pull-ups',
    },
    'eat': {
        'display_name': 'Eating Habits',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete eating habits',
    },
    'train': {
        'display_name': 'Training Style',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete training style',
    },
    'background': {
        'display_name': 'Background',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete background',
    },
    'experience': {
        'display_name': 'Experience',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete experience level',
    },
    'schedule': {
        'display_name': 'Schedule',
        'better': 'neither',
        'unit': '',
        'description': 'Athlete training schedule',
    },
    'howlong': {
        'display_name': 'Experience Duration',
        'better': 'neither',
        'unit': '',
        'description': 'How long athlete has been training',
    },
}
