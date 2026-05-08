# 02_data/01_generate_synthetic_data.py
# Google Colab-ready Python script to generate synthetic Bumble-like datasets
# Outputs: users.csv, events.csv, matches.csv, messages.csv, payments.csv, verifications.csv
# Project: driiiportfolio (schema documented separately)

import numpy as np
import pandas as pd
import uuid
import random
from datetime import datetime, timedelta

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Config
N_USERS = 50000
START_DATE = datetime(2026,1,1)
END_DATE = datetime(2026,4,30)
DAYS = (END_DATE - START_DATE).days + 1

# Helper functions
def rand_date(start, days):
    return start + timedelta(days=int(np.random.rand()*days), hours=int(np.random.rand()*24), minutes=int(np.random.rand()*60))

def gen_user_id(i):
    return f"user_{i:06d}"

# 1) Users table
countries = ['US','GB','BR','IN','MX','FR','DE','CA','AU','ES']
genders = ['female','male','nonbinary']
intent_levels = ['casual','intentional','friendship']
premium_prob = 0.08  # baseline paying users
users = []
for i in range(N_USERS):
    uid = gen_user_id(i+1)
    signup = rand_date(START_DATE, DAYS)
    country = np.random.choice(countries, p=[0.25,0.08,0.12,0.15,0.08,0.06,0.06,0.08,0.06,0.06])
    gender = np.random.choice(genders, p=[0.52,0.45,0.03])
    intent = np.random.choice(intent_levels, p=[0.45,0.35,0.20])
    age = int(np.clip(np.random.normal(29,6),18,65))
    # simulate pruning: 21.1% of paying users removed in March (algorithmic prune)
    is_paying = np.random.rand() < premium_prob
    users.append({
        'user_id': uid,
        'signup_ts': signup.isoformat(),
        'country': country,
        'zip_code': str(78749) if country=='US' and np.random.rand()<0.2 else str(random.randint(10000,99999)),
        'gender': gender,
        'age': age,
        'intent_level': intent,
        'is_paying': int(is_paying),
        'initial_right_swipe_rate': round(np.clip(np.random.beta(2,5),0.01,0.9),3)
    })
users_df = pd.DataFrame(users)

# 2) Verifications (selfie-based)
verifications = []
for uid in users_df['user_id']:
    # 5% missing verification attempts, 3% failed
    attempted = np.random.rand() > 0.05
    passed = attempted and (np.random.rand() > 0.03)
    verifications.append({
        'user_id': uid,
        'verification_attempted': int(attempted),
        'verification_passed': int(passed),
        'verification_ts': (rand_date(START_DATE, DAYS).isoformat() if attempted else None)
    })
ver_df = pd.DataFrame(verifications)

# 3) Matches and events (simulate Dates rollout spike in mid-February)
events = []
matches = []
messages = []
payments = []

# Dates rollout: Feb 15 2026 triggers algorithmic earthquake (intent modeling change)
dates_rollout_date = datetime(2026,2,15)

for idx, row in users_df.sample(frac=1.0, random_state=RANDOM_SEED).iterrows():
    uid = row['user_id']
    # number of sessions per user (skewed)
    sessions = max(1, int(np.random.poisson(6) - (0 if row['is_paying'] else 1)))
    last_session = None
    for s in range(sessions):
        ts = rand_date(START_DATE, DAYS)
        event_type = np.random.choice(['session_start','profile_view','swipe','date_suggestion','match','message_sent'], p=[0.15,0.35,0.25,0.05,0.10,0.10])
        events.append({
            'event_id': str(uuid.uuid4()),
            'user_id': uid,
            'event_type': event_type,
            'event_ts': ts.isoformat(),
            'device': np.random.choice(['iOS','Android','Web'], p=[0.55,0.40,0.05]),
            'app_version': f"v{random.randint(1,4)}.{random.randint(0,9)}"
        })
        # create matches and messages with some probability
        if event_type == 'match' or (event_type=='swipe' and np.random.rand()<0.02):
            match_id = str(uuid.uuid4())
            partner_id = gen_user_id(random.randint(1,N_USERS))
            matches.append({
                'match_id': match_id,
                'user_id': uid,
                'partner_id': partner_id,
                'match_ts': ts.isoformat(),
                'match_source': 'dates' if ts >= dates_rollout_date else 'swipe',
                'partner_verified': int(np.random.rand()>0.85)
            })
            # messages after match
            if np.random.rand() < 0.6:
                # message count skewed
                mcount = np.random.poisson(2)
                for m in range(max(1,mcount)):
                    msg_ts = ts + timedelta(minutes=random.randint(1,1440))
                    # message sentiment noise
                    sentiment = np.random.choice(['positive','neutral','negative'], p=[0.6,0.3,0.1])
                    messages.append({
                        'message_id': str(uuid.uuid4()),
                        'match_id': match_id,
                        'sender_id': uid if np.random.rand()>0.5 else partner_id,
                        'text': "lorem ipsum",
                        'sentiment': sentiment,
                        'message_ts': msg_ts.isoformat()
                    })
        # payments: occasional subscription events
        if row['is_paying'] and np.random.rand() < 0.02:
            pay_ts = ts + timedelta(days=random.randint(0,30))
            payments.append({
                'payment_id': str(uuid.uuid4()),
                'user_id': uid,
                'amount': round(np.random.choice([4.99,9.99,19.99,29.99]),2),
                'currency': 'USD',
                'payment_ts': pay_ts.isoformat(),
                'payment_method': np.random.choice(['card','apple_pay','google_pay'])
            })

# Introduce noise: duplicates, missing values, and a pruning event in March
events_df = pd.DataFrame(events)
matches_df = pd.DataFrame(matches)
messages_df = pd.DataFrame(messages)
payments_df = pd.DataFrame(payments)

# Add duplicates
dup_events = events_df.sample(frac=0.01, random_state=RANDOM_SEED)
events_df = pd.concat([events_df, dup_events], ignore_index=True)

# Add missing values
events_df.loc[events_df.sample(frac=0.005, random_state=1).index, 'device'] = None
users_df.loc[users_df.sample(frac=0.01, random_state=2).index, 'age'] = None

# Algorithmic prune: remove 21.1% of paying users with low engagement in March 2026
prune_cutoff = datetime(2026,3,1)
paying_users = users_df[users_df['is_paying']==1].copy()
# low engagement proxy: initial_right_swipe_rate < 0.15 and few sessions
low_engagement = paying_users[paying_users['initial_right_swipe_rate'] < 0.15].sample(frac=0.211, random_state=3)
pruned_user_ids = set(low_engagement['user_id'].tolist())
# mark pruned users in users table (soft delete)
users_df['is_pruned'] = users_df['user_id'].apply(lambda x: int(x in pruned_user_ids))

# Export CSVs
users_df.to_csv('users.csv', index=False)
ver_df.to_csv('verifications.csv', index=False)
events_df.to_csv('events.csv', index=False)
matches_df.to_csv('matches.csv', index=False)
messages_df.to_csv('messages.csv', index=False)
payments_df.to_csv('payments.csv', index=False)

print("Exported: users.csv, verifications.csv, events.csv, matches.csv, messages.csv, payments.csv")