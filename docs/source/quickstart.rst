Quick Start - Train PPO/NLPO using pre-defined YAML configs
===========================================================

We provide a simple training API that can be invoked via train `script <https://github.com/allenai/RL4LMs/blob/main/scripts/training/train_text_generation.py>`_ that allows to train PPO, NLPO or a supervised model by using a config file (YAML). 

For example, to train T5-base on CNN/DM summarization on PPO using Rouge-1 as reward function, you can run:

.. code-block:: bash

   python scripts/training/train_text_generation.py --config_path scripts/training/task_configs/summarization/t5_ppo.yml


Config files for all tasks can be found `here <https://github.com/allenai/RL4LMs/tree/main/scripts/training/task_configs>`_.

YAML file schema - Configuring building blocks
----------------------------------------------

Config file contains details about hyper-parameter settings for building blocks which are described below:

- **Dataset/Task**: Dataset containing samples with input prompts and reference sentences. Available datasets are found in the class ``DataPoolRegistry`` in `registry <https://github.com/allenai/RL4LMs/blob/main/rl4lms/envs/text_generation/registry.py>`_. (See how to create your own dataset [here](#adding-dataset))

.. code:: yaml

   datapool:
     id: cnn_daily_mail
     args:
       prompt_prefix: "Summarize: "


- **Tokenizer** - A pre-trained tokenizer that is used to (de)tokenize input and output sequences with settings for padding and truncation

.. code:: yaml

   tokenizer:
     model_name: t5-base
     padding_side: left
     truncation_side: left
     pad_token_as_eos_token: False
 
.. todo::
   hyperlink to contents in blocks.rst

- **Reward Function**: Reward function which computes token-level scores at each time step of MDP. Available reward functions can be found in the class ``RewardFunctionRegistry``. (See how to create your own reward function `here <#adding-reward-function>`_)

.. code:: yaml

   reward_fn:
     id: rouge
     args:
       rouge_type: "rouge1"


- **Environment**: Configures a gym-style text generation `environment <https://github.com/allenai/RL4LMs/blob/main/rl4lms/envs/text_generation/env.py>`_ which simulates MDP episodes. Rollouts are generated using train samples from dataset consisting of input and reference texts.
Further, we wrap our env with ``SubProcVecEnv`` from stable-baselines that processes ``n_envs`` episodes in parallel using multi-processing to compute step-wise rewards.  
Further configuration settings include: 

  - ``max_episode_length`` : max length of the episode 
  - ``max_prompt_length`` - maximum length of the input text to consider 
  - ``terminate_on_eos`` - whether to terminate the episode as soon as EOS action is performed 
  - ``prompt_truncation_side`` - truncation side for the prompt text 
  - ``context_start_token`` - id for context token (corresponds to initial token given to decoder in encoder-decoder models)

.. code:: yaml

   env:
     n_envs: 10
     args:
       max_prompt_length: 512
       max_episode_length: 100
       terminate_on_eos: True
       prompt_truncation_side: "right"
       context_start_token: 0

.. todo::
   hyperlink to contents in blocks.rst 

- **On-policy alg**: We provide implementations of 4 on-policy algorithms: PPO, NLPO, A2C and TRPO adapted from `stable-baselines3 <https://github.com/DLR-RM/stable-baselines3>`_ tailored to work with NLP tasks which can be used out-of-the-box with either a causal policy or a seq2seq LM policy. (See how to create your own [on-policy algorithm](#adding-custom-on-policy-algorithms) or [policy](#adding-custom-policies))
  
  - We also provide a supervised `trainer <https://github.com/allenai/RL4LMs/blob/2863116cd5860e4a4106a76486e70bfac25df2ba/rl4lms/envs/text_generation/training_utils.py#L225>`_ for benchmarking purposes. Supervised Warm start models are already uploaded to Huggingface Hub and specified in the respective config files.
  
  - Hyper-parameters for the algorithm can be specified at ``alg/args``. 
  
  - Further, all RL algorithms use adaptive KL controller to keep the LM close to original LM by setting initial KL co-efficient (``alg/kl_div/coeff``) and target KL (``alg/kl_div/target_kl``). 
  
  - We support two types of LM policy: **causal LM policy** (for decoder only models) and **seq2seq LM policy** (for encoder-decoder models). Further for NLPO, we also provide maskable variants of these. Policy implementations can be found `here <https://github.com/allenai/RL4LMs/blob/main/rl4lms/envs/text_generation/policy.py>`_ in and it can be attached to algorithms by specifying ``alg/policy/id`` and ``alg/policy/args``
  

.. code:: yaml

   alg:
     id: ppo
     args: 
       n_steps: 512
       batch_size: 64
       verbose: 1
       learning_rate: 0.000002
       n_epochs: 5
       ent_coef: 0.0
     kl_div:
       coeff: 0.001
       target_kl: 0.2
     policy:
       id: seq2seq_lm_actor_critic_policy
       args:
         model_name: t5-base
         apply_model_parallel: True
         prompt_truncation_side: "right"
         generation_kwargs:
           do_sample: True
           top_k: 50
           min_length: 50
           max_new_tokens: 100    
           

- **Trainer Config**: We provide an `On-policy trainer <https://github.com/allenai/RL4LMs/blob/2863116cd5860e4a4106a76486e70bfac25df2ba/rl4lms/envs/text_generation/training_utils.py#L126>`_ - a feature-complete wrapper that instantiates building blocks from their corresponding configs and provides an outer training loop consisting of *train* and *eval* iterations ``train_evaluation/n_iters``. 

  - Each iteration corresponds to performing updates with ``alg/args/n_steps`` x ``env/n_envs`` of the chosen algorithm. 
  
  - For every ``eval_every`` iters, LM is evaluated on validation split using metrics listed in ``train_evaluation/metrics`` with generation kwargs provided in ``train_evaluation/generation_kwargs`` (this overrides rollout ``alg/policy/generation_kwargs`` for inference purposes only)


.. code:: yaml

   # train and evaluation
   train_evaluation:
     eval_batch_size: 100
     n_iters: 100
     eval_every: 10
     save_every: 1
     metrics:
       - id: meteor
         args: {}
       - id: rouge
       - id: bleu
         args: {}
       - id: bert_score
         args:
           language: en
       - id: diversity
         args: {}
     generation_kwargs: 
       do_sample: True
       top_k: 0
       temperature: 0.7
       min_length: 50
       max_new_tokens: 100
        
