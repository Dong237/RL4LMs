Custom Building Blocks
======================
RL4LMs provide complete customizability - with respect to adding new tasks/datasets, reward functions, evaluation metric, on-policy algorithms and actor-critic policies.

Adding dataset
--------------
Users can create their own datasets by sub-classing `TextGenPool <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/data_pools/text_generation_pool.py#L15>`_ just by overriding `prepare(cls, split: str, **args) -> 'TextGenPool':` method to return an instance of TextGenPool. An example is shown below:

.. code-block:: python
  from rl4lms.data_pools.text_generation_pool import Sample, TextGenPool

  class MyDataPool(TextGenPool):
    @classmethod
    def prepare(cls, split: str):
        .. 
        samples = []
        for ix, item in enumerate(..):
            sample = Sample(id=f"{split}_{ix}",
                            prompt_or_input_text=item["document"],
                            references=[item["target"]]
                            )
            samples.append(sample)
        pool_instance = cls(samples)
        return pool_instance
        
Adding reward function
----------------------
Custom reward funtions can be implemented easily by sub-classing `RewardFunction <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/envs/text_generation/reward.py#L12>`_ (a callable) which takes observation ($s$), next observation ($s'$), action ($a$), done (indicating whether episode is finished) and meta info (containing other information about textual input). Here, `Observation <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/envs/text_generation/observation.py#L11>`_ is a data class object consisting of generated text (at a particular step), prompt text, context text (at that step), reference text which can be used to compute token-level or sentence level rewards.

.. code-block:: python
  from rl4lms.envs.text_generation.observation import Observation
  from rl4lms.envs.text_generation.reward import RewardFunction


  class MyRewardFunction(RewardFunction):
      def __init__(self, *args) -> None:
          super().__init__()

      def __call__(self, prev_observation: Observation,
                   action: int,
                   current_observation: Observation,
                   done: bool,
                   meta_info: Dict[str, Any] = None) -> float:
          if done:
              reward = ..
              return reward
          return 0

In addition to traditional NLG metrics, for quick prototyping, we provide two synthetic reward functions which trains LMs to `generate numbers <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/envs/text_generation/test_reward.py#L8>`_ in increasing order and `generate dates <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/envs/text_generation/test_reward.py#L54>`_. These can be used to quickly test different algorithms and policies. Corresponding configs can be found here (`numbers <https://github.com/allenai/RL4LMs/tree/main/scripts/training/task_configs/synthetic_generate_increasing_numbers>`_, `dates <https://github.com/allenai/RL4LMs/tree/main/scripts/training/task_configs/synthetic_generate_dates>`_)

Adding custom metrics
---------------------
Users can create their own evaluation metric which then will be used to periodically evaluate the model on validation split of dataset. This can be done by sub-classing `BaseMetric <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/envs/text_generation/metric.py#L20>`_ which takes prompt texts, generated texts, reference texts, meta_infos, current LM model, split name as inputs and returns a dict with metric name as key and value consisting of tuple of sentence-level scores and corpus level scores. An example is as follows:

.. code-block:: python
  from rl4lms.envs.text_generation.metric import BaseMetric

  class MyMetric(BaseMetric):
      def __init__(self) -> None:
          super().__init__()

      def compute(self,
                  prompt_texts: List[str],
                  generated_texts: List[str],
                  reference_texts: List[List[str]],
                  meta_infos: List[Dict[str, Any]] = None,
                  model: PreTrainedModel = None,
                  split_name: str = None):
          metric_dict = {
              "custom_metrics/my_metric": ([0.4, 0.7, 0.9], 0.7)
          }
          return metric_dict


Adding custom on-policy algorithms
----------------------------------
In addition to supported on-policy algorithms (PPO, NLPO, A2C,TRPO), users can implement their own on-policy algorithms with ease by sub-classing stable-baselines3's `OnPolicyAlgorithm <https://github.com/DLR-RM/stable-baselines3/blob/a697401e032dd4fecbbd4162755ddd707df980d3/stable_baselines3/common/on_policy_algorithm.py#L20>`_. Since we provide `wrappers <https://github.com/allenai/RL4LMs/blob/af5a1326578789856ca8550cb5496c9ccc1afdc5/rl4lms/envs/text_generation/alg_wrappers.py#L67>`_ for on-policy algorithms that handles rollouts using LM policies, environment, computing rewards etc, users just need to implement `train()` method with custom loss functions. 

.. code-block:: python
  from stable_baselines3.common.on_policy_algorithm import OnPolicyAlgorithm

  class MyOnPolicyAlgorithm(OnPolicyAlgorithm):
      def __init__(**args):
          super().__init__(**args)

      def train(self) -> None:
          # train for n_epochs epochs
          for epoch in range(self.n_epochs):
              # Do a complete pass on the rollout buffer
              for rollout_data in self.rollout_buffer.get(self.batch_size):
                # compute loss


Adding custom policies
----------------------
We provide LM based actor-critic policy `implementations <https://github.com/allenai/RL4LMs/blob/main/rl4lms/envs/text_generation/policy.py>`_ that wraps causal LM and seq2seq LMs. These can be also extended (for eg: use a different critic architecture) by overriding appropriate methods (eg. `evaluate_actions()`)

Registry
--------
Finally, just register your custom components by adding them to corresponding `registry <https://github.com/allenai/RL4LMs/blob/main/rl4lms/envs/text_generation/registry.py>`_, after which they can be used directly from configs similar to pre-defined components :wave:

Crowdsourcing templates
-----------------------

We have provided the crowdsourcing templates we used on mechanical turk, along with example inputs in `scripts/crowdworking_templates`. You might find these a helpful starting point either for evaluating your own model's generations, or for gathering training data for a learned reward function.

