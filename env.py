import gymnasium as gym
from gymnasium import spaces
from gymnasium import ObservationWrapper
import numpy as np
import random

################################################################################################################
################################################################################################################
################################################################################################################

def generate_surgeries(num_surgeries=15, min_duration=30, max_duration=70, day_length=480, seed=None):
    if seed is not None:
        np.random.seed(seed)
    surgeries = []
    while len(surgeries) < num_surgeries:
        duration = np.random.randint(min_duration, max_duration+1)
        latest_arrival = day_length - duration -15
        if latest_arrival < 0:
            continue  # בטעות, אבל לא יקרה בתנאים שלנו
        arrival_time = np.random.randint(0, latest_arrival+1)
        urgency = np.random.choice([1, 2, 3], p=[0.3, 0.3, 0.4])
        surgeries.append({
            'duration': duration,
            'arrival_time': arrival_time,
            'urgency': urgency
        })
    # מיון לפי זמן הגעה
    surgeries.sort(key=lambda x: x['arrival_time'])
    return surgeries
    
################################################################################################################
################################################################################################################
################################################################################################################


class OperatingRoomEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, num_rooms=3, surgeries=None, day_length=480, max_patients_in_obs=8):
        super(OperatingRoomEnv, self).__init__()
        self.num_rooms = num_rooms
        self.day_length = day_length
        self.max_patients_in_obs = max_patients_in_obs

        # מרחב פעולות: 0..num_rooms-1 (חדר), num_rooms = המתן
        #self.action_space = spaces.MultiDiscrete([self.num_rooms + 1, self.max_patients_in_obs])
        self.action_space = spaces.Discrete((self.num_rooms + 1) * self.max_patients_in_obs)

        
        # מרחב תצפית עשיר
        self.observation_space = spaces.Dict({
            'rooms': spaces.MultiDiscrete([self.day_length+1]*self.num_rooms),
            'time': spaces.Discrete(self.day_length+1),
            'num_waiting': spaces.Discrete(self.max_patients_in_obs+1),
            'waiting_times': spaces.MultiDiscrete([self.day_length+1]*self.max_patients_in_obs),
            'urgencies': spaces.MultiDiscrete([4]*self.max_patients_in_obs)
        })
        
    
        self.all_surgeries = sorted(surgeries, key=lambda x: x['arrival_time'])
        self.reset()
        
        # מיון לפי זמן הגעה
        #surgeries.sort(key=lambda x: x['arrival_time'])
        #return surgeries
    
    def reset(self, *, seed=None, options=None, random_patients=False):
        super().reset(seed=seed)  # קובע seed אם צריך (אופציונלי)

        self.time = 0
        self.rooms = [0 for _ in range(self.num_rooms)]
        self.waiting_list = []
        
        if random_patients:
            # מגריל רשימת מטופלים חדשה בכל אפיזודה
            self.all_surgeries = generate_surgeries(
                num_surgeries=18, day_length=self.day_length
            )
        # אחרת – משתמשים ברשימה שהוזנה ב-init
        self.future_patients = self.all_surgeries.copy()
        self.scheduled = []
        self.finished = []
        return self._get_obs() , {}

    def _get_obs(self):
        num_waiting = len(self.waiting_list)
        waiting_times = []
        urgencies = []
        for i in range(self.max_patients_in_obs):
            if i < num_waiting:
                patient = self.waiting_list[i]
                waiting_time = self.time - patient['arrival_time']
                urgency = patient['urgency']
            else:
                waiting_time = 0
                urgency = 0
            waiting_times.append(waiting_time)
            urgencies.append(urgency)
        return {
            'rooms': np.array(self.rooms, dtype=np.int32),
            'time': int(self.time),
            'num_waiting': int(num_waiting),
            'waiting_times': np.array(waiting_times, dtype=np.int32),
            'urgencies': np.array(urgencies, dtype=np.int32)
        }

    def step(self, action):
        reward = 0
        info = {}
        #room_idx, patient_idx = action
        room_idx = action // self.max_patients_in_obs
        patient_idx = action % self.max_patients_in_obs

        self.time += 1
        self.rooms = [max(0, r - 1) for r in self.rooms]
    
        # הוספת מטופלים שהגיעו
        arrived_now = []
        still_future = []
        for s in self.future_patients:
            if s['arrival_time'] <= self.time:
                arrived_now.append(s)
            else:
                still_future.append(s)
        self.future_patients = still_future
        self.waiting_list.extend(arrived_now)
    
        valid_rooms = [i for i, val in enumerate(self.rooms) if val == 0]
    
        # אם אין מטופלים בתור – אין קנס על המתנה, אלא רק 0 נקודות
        if len(self.waiting_list) == 0:
            if room_idx == self.num_rooms:
                reward += 0  # פעולה לגיטימית
            else:
                reward -= 2  # ניסה לשבץ כשאין אף מטופל
    
        # ניסיון שיבוץ
        elif room_idx == self.num_rooms:
            # יש ממתינים אבל הסוכן בחר להמתין – קנס על בזבוז זמן
            reward -= 1
    
        elif (room_idx in valid_rooms and 0 <= patient_idx < len(self.waiting_list)):
            surgery = self.waiting_list.pop(patient_idx)
            waiting_time = self.time - surgery['arrival_time']
    
            # בונוס על שיבוץ
            reward += 60
    
            # (עבור מינימום זמן המתנה ממוצע)
            # קנס פרופורציונלי על זמן המתנה (רק אם חיכה דקה ומעלה)
            if waiting_time >= 2:
                reward -= waiting_time * 0.1

    
            # תגמול/קנס על מקרה דחוף
            if surgery['urgency'] == 3:
                reward += 40  # תגמול לשיבוץ דחוף
                # קנס מוגדל על דחוף שחיכה הרבה (אם waiting_time > 15 דק' לדוג')
                if waiting_time > 15:
                    reward -= (waiting_time - 15) * 0.3
    
            # קנס חזק אם משך הניתוח חורג מיום העבודה
            if self.time + surgery['duration'] > self.day_length:
                overtime = (self.time + surgery['duration']) - self.day_length
                reward -= overtime * 2
    
            self.rooms[room_idx] = surgery['duration']
            self.scheduled.append({**surgery, 'scheduled_time': self.time, 'room': room_idx})
    
        else:
            # פעולה לא חוקית – בחר חדר תפוס/לא קיים, או אינדקס מטופל לא קיים
            reward -= 2
    
        # קנס בכל דקה על ממתינים דחופים – עוזר לעודד טיפול בהם
        for patient in self.waiting_list:
            if patient['urgency'] == 3:
                wt = self.time - patient['arrival_time']
                if patient['urgency'] == 3 and wt >= 2:
                    reward -= wt * 0.05  # קנס קטן לכל דקה שמחכה דחוף (מצטבר)
    
        # תנאי עצירה
        done = (self.time >= self.day_length or
                (len(self.waiting_list) == 0 and len(self.future_patients) == 0 and all(r == 0 for r in self.rooms)))
        if done:
            # קנס חזק לכל מטופל שלא שובץ
            for patient in self.waiting_list:
                base_penalty = 20
                urgency_penalty = 10 if patient['urgency'] == 3 else 0
                reward -= (base_penalty + urgency_penalty)
        terminated = done
        truncated = False  # תוכל לשים True אם תעשה מגבלה מלאכותית על אורך האפיזודה
        #print("info in step:", type(info), info)  # בדיקה לפני return
        return self._get_obs(), reward, terminated, truncated ,info            
        #return self._get_obs(), reward, done, info



    def render(self, mode="human"):
        print(f"Time: {self.time} | Rooms: {self.rooms} | Waiting: {len(self.waiting_list)}")
        for i, patient in enumerate(self.waiting_list[:self.max_patients_in_obs]):
            wait = self.time - patient['arrival_time']
            print(f"  Patient {i+1}: Waiting {wait} min | Urgency: {patient['urgency']}")