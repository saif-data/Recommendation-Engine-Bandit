# Define the Epsilon Greedy Bandit, which focuses on iteratively minimizing the probablity of 
# Exploring in lieu of Exploiting. 

import numpy as np

class EpsilonGreedy(object):
    def __init__(self,n,decay=100): 
        # The decay value determines how quickly, in terms of pageviews, the model will 
        # converge to only showing the 'best' arm. 100 is a good starting point for all-size clients.
        # However, for clients with higher traffic, it would be advisable to raise this value. 
        # More details here: https://docs.google.com/spreadsheets/d/1jYF6ztkiM1MCOLv5bdNV14lQA4dSuqdH4cIADYXfANw/edit?usp=sharing     
        self.pageviews = [0] * n  
        self.conversions = [0.] * n 
        self.decay = decay
        self.n = n
        
    def get_epsilon(self):
        total = np.sum(self.pageviews)
        return float(self.decay) / (total + float(self.decay))
        
    def choose_arm(self):
        #Choose an arm for testing
        epsilon = self.get_epsilon()
        if np.random.random() > epsilon:
            # Exploit (use best arm)
            return np.argmax(self.conversions)
        else:
            # Explore (test all arms)
            return np.random.randint(self.n)
        
    def update(self,arm,reward):
        # Update an arm with the reward value (click = 1; no click = 0)
        self.pageviews[arm] = self.pageviews[arm] + 1
        n = self.pageviews[arm]
        value = self.conversions[arm]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.conversions[arm] = new_value
        
#Integrate the Bandit with the app, to determine the best recommendation algorithm

from flask import Flask, request, render_template, url_for, Response, json
from uuid import uuid4
import numpy as np

app = Flask(__name__)

arms = ["Content1","Content2","Content3","Collaborative"]
eg = EpsilonGreedy(len(arms))
ids = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Choose an arm
        arm = eg.choose_arm()
        arm_name = arms[arm]
        u_id = str(uuid4())
        pred = #This is where the prediction for the arm, though a recommendation algorithm, would go
        ids[u_id] = {
            'arm':arm,
            'arm_name':arm_name
        }
        return Response(json.dumps({'result':pred['result'],
                                    'uid':u_id}),mimetype='application/json')
    elif request.method == 'GET':
        #Render page for user


@app.route('/update', methods=['POST'])
def update_path():
    try:
        u_id,item_num = request.json['id'], int(request.json['item'])
        reward = 1. - (item_num / 9.)
        if reward > 1. or reward < 0.:
            raise Exception()
        reward = reward * reward;
        # will throw exception if id not in ids
        arm_data = ids.pop(u_id)
        arm = arm_data['arm']
        eg.update(arm,reward)
        arm_data['reward'] = reward
        arm_data['arm_name'] = arms[arm]
        res = Response(json.dumps(arm_data),
                        mimetype='application/json')
        return res
    except Exception:
        res = Response(json.dumps({'bad data':"sorry"}),
                        mimetype='application/json')
        return res

@app.route('/state', methods=['GET'])
def get_results():
    state = {}
    state['epsilon'] = eg.get_epsilon()
    state['arms'] = []
    for i in range(len(arms)):
        arm_data = {}
        arm_data['name'] = arms[i]
        arm_data['number'] = i
        arm_data['pageviews'] = eg.pageviews[i]
        arm_data['conversions'] = eg.conversions[i]
        state['arms'].append(arm_data)
    return render_template('state.html',state=state)

if __name__ == '__main__':
    app.run(debug=True)
