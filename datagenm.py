import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
from sklearn import preprocessing

fake = Faker()
np.random.seed(42)

MIN_CLICKS = 5
MAX_CLICKS = 150
MIN_KEYS = 0
MAX_KEYS = 800
MIN_TRAVEL = 5.0
MAX_TRAVEL = 600.0
MAX_TABS = 25
BURST_LAMBDA = 1.5
HESITATION_ALPHA = 1
HESITATION_BETA = 3
INACTIVE_PROB = 0.3
MIN_DEADLINE = 1
MAX_DEADLINE = 72
CRITICAL_DEADLINE = 12
PROCRASTINATION_THRESHOLD = 0.7
FEEDBACK_THRESHOLD = 0.25
TIME_SCALE = 300

APP_TYPES = ['chrome', 'work', 'other', 'game', 'social_media']
APP_WEIGHTS = [0.25, 0.15, 0.2, 0.25, 0.15]
HIGH_RISK_APPS = ['game', 'social_media']
WORK_APPS = ['work', 'word', 'powerpoint', 'pdf']
DISTRACTION_APPS = ['chrome', 'other']
FEEDBACK_YES = 0
FEEDBACK_NO = 1

APP_ENCODING = {'work': 0,'chrome': 1,'game': 2,'social_media': 3,'other': 4}


records = []
current_time = datetime.now() - timedelta(days=7)

for _ in range(100):
    clicks = np.random.randint(MIN_CLICKS, MAX_CLICKS)
    keys = np.random.randint(MIN_KEYS, MAX_KEYS)
    travel = np.random.uniform(MIN_TRAVEL, MAX_TRAVEL)
    tabs = np.random.randint(0, MAX_TABS)

    bursts = np.random.poisson(lam=BURST_LAMBDA)
    hesitation = np.random.beta(a=HESITATION_ALPHA, b=HESITATION_BETA)
    inactive = np.random.geometric(p=INACTIVE_PROB)

    app_type = np.random.choice(APP_TYPES, p=APP_WEIGHTS)
    is_distracted = False

    if (app_type in HIGH_RISK_APPS or
            (bursts > 2 and hesitation > PROCRASTINATION_THRESHOLD) or
            tabs > 15):
        is_distracted = True
        keys = int(keys * 0.3)
        clicks = int(clicks * 1.5)

    deadline = np.random.randint(MIN_DEADLINE, MAX_DEADLINE)
    if deadline < CRITICAL_DEADLINE:
        is_distracted = is_distracted or (np.random.random() > PROCRASTINATION_THRESHOLD)

    feedback = FEEDBACK_YES if (is_distracted and np.random.random() > FEEDBACK_THRESHOLD) else FEEDBACK_NO

    current_time += timedelta(seconds=np.random.exponential(scale=TIME_SCALE))


    records.append([clicks, current_time.strftime("%Y-%m-%d %H:%M:%S"), feedback, keys, round(travel, 2), tabs, app_type])

column_names = ['mouse_clicks', 'timestamp', 'feedback_response', 'keys_pressed', 'mouse_travel', 'tabs_changed', 'app_focus_type']

data_frame = pd.DataFrame(records, columns=column_names)
data_frame['app_focus_type']= data_frame['app_focus_type'].map(APP_ENCODING)

data_frame.to_csv('procrastination_data2.csv', index=False)
print('done')
