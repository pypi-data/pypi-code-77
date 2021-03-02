#!/usr/bin/env python
# coding: utf-8

# https://github.com/jeremiedecock/neural-network-figures.git
import nnfigs.core as nnfig
import matplotlib.pyplot as plt


## EXERCISE 1 #################################################################

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def logistic_regression(s, theta):
    prob_push_right = sigmoid(np.dot(s, np.transpose(theta)))
    return prob_push_right


def draw_action(s, theta):
    prob_push_right = logistic_regression(s, theta)
    r = np.random.rand()
    return 1 if r < prob_push_right else 0


# Generate an episode
def eval_one_episode(theta, max_episode_length=EPISODE_DURATION, render=False):
    s_t = env.reset()

    episode_rewards = []

    for t in range(max_episode_length):

        if render:
            env.render_wrapper.render()

        a_t = draw_action(s_t, theta)
        s_t, r_t, done, info = env.step(a_t)

        episode_rewards.append(r_t)

        if done:
            break

    return sum(episode_rewards)


def eval_multiple_episodes(theta, num_episodes=NUM_EPISODES, max_episode_length=EPISODE_DURATION, render=False):
    
    reward_list = []

    for episode_index in range(num_episodes):
        episode_global_reward = eval_one_episode(theta, max_episode_length, render)
        reward_list.append(episode_global_reward)

        if render:
            print("Test Episode {}: Total Reward = {}".format(episode_index, episode_global_reward))

    return np.mean(reward_list)


def cem_uncorrelated(objective_function, mean_array, var_array,
                     max_iterations=500, sample_size=50, elite_frac=0.2,
                     print_every=10, # success_score=None,
                     hist_dict=None):
    """Cross-entropy method.
        
    Params
    ======
        objective_function (function): the function to maximize
        mean_array (array of floats): the initial proposal distribution (mean)
        var_array (array of floats): the initial proposal distribution (variance)
        max_iterations (int): number of training iterations
        sample_size (int): size of population at each iteration
        elite_frac (float): rate of top performers to use in update with elite_frac ∈ ]0;1]
        print_every (int): how often to print average score
        hist_dict (dict): logs
    """
    assert 0. < elite_frac <= 1.

    n_elite = math.ceil(sample_size * elite_frac)

    for iteration_index in range(0, max_iterations):

        # SAMPLE A NEW POPULATION OF SOLUTIONS (THETA VECTORS) ################

        theta_array = np.random.multivariate_normal(mean=mean_array, cov=np.diag(var_array), size=(sample_size))

        # EVALUATE SAMPLES AND EXTRACT THE BEST ONES ("ELITE") ################

        score_array = np.array([objective_function(theta) for theta in theta_array])

        sorted_indices_array = score_array.argsort()              # Sort from the lower score to the higher one
        elite_indices_array = sorted_indices_array[-n_elite:]     # Here we wants to *maximize* the objective function thus we take the samples that are at the end of the sorted_indices

        elite_theta_array = theta_array[elite_indices_array]

        #df = pd.DataFrame(theta_array)
        #df['elite'] = 0
        #df.iloc[elite_indices_array, -1] = 1
        #print(df)
        #sns.pairplot(df, hue="elite")
        #plt.show()

        # FIT THE NORMAL DISTRIBUTION ON THE ELITE POPULATION #################

        mean_array = elite_theta_array.mean(axis=0)
        var_array = elite_theta_array.var(axis=0)

        # PRINT STATUS ########################################################
        
        if iteration_index % print_every == 0:
            #print("Iteration {}\tScore {}\tMean: {}\tVar: {}".format(iteration_index, objective_function(mean_array), str(mean_array), str(var_array)))
            print("Iteration {}\tScore {}".format(iteration_index, objective_function(mean_array)))
        
        if hist_dict is not None:
            hist_dict[iteration_index] = [objective_function(mean_array)] + mean_array.tolist() + var_array.tolist()

    return mean_array


## EXERCISE 2 #################################################################

###############################################################################
# Parametric Stochastic Policy ################################################
###############################################################################

# Activation functions ########################################################

def identity(x):
    return x

def tanh(x):
    return np.tanh(x)

def relu(x):
    x_and_zeros = np.array([x, np.zeros(x.shape)])
    return np.max(x_and_zeros, axis=0)

# Dense Multi-Layer Neural Network ############################################

class NeuralNetworkPolicy:

    def __init__(self, activation_functions, shape_list):
        self.activation_functions = activation_functions
        self.shape_list = shape_list

    def __call__(self, state, theta):
        weights = unflatten_weights(theta, self.shape_list)

        return feed_forward(inputs=state,
                            weights=weights,
                            activation_functions=self.activation_functions)


def feed_forward(inputs, weights, activation_functions, verbose=False):
    x = inputs.copy()
    for layer_weights, layer_activation_fn in zip(weights, activation_functions):

        y = np.dot(x, layer_weights[1:])
        y += layer_weights[0]
        
        layer_output = layer_activation_fn(y)

        if verbose:
            print("x", x)
            print("bias", layer_weights[0])
            print("W", layer_weights[1:])
            print("y", y)
            print("z", layer_output)

        x = layer_output

    return layer_output


def weights_shape(weights):
    return [weights_array.shape for weights_array in weights]


def flatten_weights(weights):
    """Convert weight parameters to a 1 dimension array (more convenient for optimization algorithms)"""
    nested_list = [weights_2d_array.flatten().tolist() for weights_2d_array in weights]
    flat_list = list(itertools.chain(*nested_list))
    return flat_list


def unflatten_weights(flat_list, shape_list):
    """The reverse function of `flatten_weights`"""
    length_list = [shape[0] * shape[1] for shape in shape_list]

    nested_list = []
    start_index = 0

    for length, shape in zip(length_list, shape_list):
        nested_list.append(np.array(flat_list[start_index:start_index+length]).reshape(shape))
        start_index += length

    return nested_list


###############################################################################
# Objective function ##########################################################
###############################################################################

class ObjectiveFunction:

    def __init__(self, env, policy, ndim, num_episodes=1, max_time_steps=float('inf')):
        self.ndim = ndim
        self.env = env
        self.policy = policy
        self.num_episodes = num_episodes
        self.max_time_steps = max_time_steps

        self.num_evals = 0
        self.hist = []
        self.hist_policy = []

    def eval(self, policy_params, num_episodes=None, render=False):
        """Evaluate a policy"""

        self.num_evals += 1

        if num_episodes is None:
            num_episodes = self.num_episodes

        average_total_rewards = 0

        for i_episode in range(num_episodes):

            total_rewards = 0.
            state = self.env.reset()

            for t in range(self.max_time_steps):
                if render:
                    self.env.render_wrapper.render()

                action = self.policy(state, policy_params)
                state, reward, done, info = self.env.step(action)
                total_rewards += reward
                
                if done:
                    break

            average_total_rewards += float(total_rewards) / num_episodes

            if render:
                print("Test Episode {0}: Total Reward = {1}".format(i_episode, total_rewards))

        # Logs

        if LOG_SCORES:
            self.hist.append({"eval": self.num_evals,
                              "episode": i_episode,
                              "total_rewards": total_rewards})

            if self.num_evals % LOG_RECORD_INTERVAL == 0:
                with open("fobj_hist.json", "w") as fd:
                    json.dump(self.hist, fd)

        if LOG_POLICIES:
            self.hist_policy.append(policy_params.tolist())

            if self.num_evals % LOG_RECORD_INTERVAL == 0:
                with open("fobj_hist_policy.json", "w") as fd:
                    json.dump(self.hist_policy, fd)

        if VERBOSE:
            print("Avg total Reward = {:0.3f}, Theta = {}".format(average_total_rewards, policy_params))

        return average_total_rewards   # Optimizers do minimization by default...

    def __call__(self, policy_params):
        return self.eval(policy_params)