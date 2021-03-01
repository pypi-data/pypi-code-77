import pandas as pd
from cccalendar import draw_colour_calendar
my_data = pd.Series({
    '2021-01-01': 'event_one',
    '2021-01-07': 'event_two',
    '2021-01-10': 'event_three',
    '2021-01-14': 'event_four',
    '2021-01-20': 'event_one',
    '2021-01-21': 'event_two',
})
draw_colour_calendar(my_data)