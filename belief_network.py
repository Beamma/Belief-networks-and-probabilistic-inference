from itertools import product

def joint_prob(network, assign):
    p = 1
    for key in list(network.keys()):
        # Check Parent In Variable
        variable = network[key]

        parents = variable['Parents']
    
        parents_vals = []

        if len(parents) > 0:
            for parent in parents:
                parents_vals.append(assign[parent])

        parents_vals_tup = tuple(parents_vals)
        cpt = variable["CPT"]
        value = cpt[parents_vals_tup]

        if assign[key] == True:
            p = p * value
        
        else:
            p = p * (1 - value)
    
    return p



def query(network, query_var, evidence):

    hidden_vars = network.keys() - evidence.keys() - {query_var}
    assign = dict(evidence)
    ans = [0, 0]
    
    for value in {True, False}:
        probability = 0
        assign[query_var] = value
        for rows in product((True, False), repeat=len(hidden_vars)):

            hidden_assigns = {var: val for var, val in zip(hidden_vars, rows)}
            complete_assign = {**assign, **hidden_assigns}
            probability = probability + joint_prob(network, complete_assign)

        if value == False:
            ans[0] = probability
        else:
            ans[1] = probability

    normal = 0

    for k in ans:
        normal = normal + k

    final_ans = {True: ans[1]/ normal, False: ans[0] / normal}
    return final_ans










def main():
    network = {
    'Burglary': {
        'Parents': [],
        'CPT': {
            (): 0.001
            }},
            
    'Earthquake': {
        'Parents': [],
        'CPT': {
            (): 0.002,
            }},
    'Alarm': {
        'Parents': ['Burglary','Earthquake'],
        'CPT': {
            (True,True): 0.95,
            (True,False): 0.94,
            (False,True): 0.29,
            (False,False): 0.001,
            }},

    'John': {
        'Parents': ['Alarm'],
        'CPT': {
            (True,): 0.9,
            (False,): 0.05,
            }},

    'Mary': {
        'Parents': ['Alarm'],
        'CPT': {
            (True,): 0.7,
            (False,): 0.01,
            }},
    }

    answer = query(network, 'John', {'Mary': True})
    print("Probability of John calling if\n"
        "Mary has called: {:.5f}".format(answer[True]))

    network = {
        'Burglary': {
            'Parents': [],
            'CPT': {
                (): 0.001
                }},
                
        'Earthquake': {
            'Parents': [],
            'CPT': {
                (): 0.002,
                }},
        'Alarm': {
            'Parents': ['Burglary','Earthquake'],
            'CPT': {
                (True,True): 0.95,
                (True,False): 0.94,
                (False,True): 0.29,
                (False,False): 0.001,
                }},

        'John': {
            'Parents': ['Alarm'],
            'CPT': {
                (True,): 0.9,
                (False,): 0.05,
                }},

        'Mary': {
            'Parents': ['Alarm'],
            'CPT': {
                (True,): 0.7,
                (False,): 0.01,
                }},
        }

    answer = query(network, 'Burglary', {'John': True, 'Mary': True})
    print("Probability of a burglary when both\n"
        "John and Mary have called: {:.3f}".format(answer[True]))      
    
    network = {
    'Burglary': {
        'Parents': [],
        'CPT': {
            (): 0.001
            }},
            
    'Earthquake': {
        'Parents': [],
        'CPT': {
            (): 0.002,
            }},
    'Alarm': {
        'Parents': ['Burglary','Earthquake'],
        'CPT': {
            (True,True): 0.95,
            (True,False): 0.94,
            (False,True): 0.29,
            (False,False): 0.001,
            }},

    'John': {
        'Parents': ['Alarm'],
        'CPT': {
            (True,): 0.9,
            (False,): 0.05,
            }},

    'Mary': {
        'Parents': ['Alarm'],
        'CPT': {
            (True,): 0.7,
            (False,): 0.01,
            }},
    }

    p = joint_prob(network, {'John': True, 'Mary': True,
                            'Alarm': True, 'Burglary': False,
                            'Earthquake': False})
    print("{:.8f}".format(p))                     
main()