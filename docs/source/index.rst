.. RL4LMs documentation master file, created by
   sphinx-quickstart on Thu Apr 20 15:20:57 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to RL4LMs's documentation!
==================================

.. note:: The documentation is currently under active development


RL4LMs provides easily customizable building blocks for training language models, including implementations of **on-policy algorithms**, **reward functions**, **metrics**, **datasets** and **LM based actor-critic policies**

Github Repository: https://github.com/allenai/RL4LMs

Paper Link: https://arxiv.org/abs/2210.01241

Website Link: https://rl4lms.apps.allenai.org/
   
   
Main Characteristics
--------------------

RL4LMs is thoroughly **tested** and **benchmarked** with over **2000 experiments** (GRUE benchmark) on a comprehensive set of: 

- 7 different Natural Language Processing (NLP) Tasks:
    - Summarization
    - Generative Commonsense Reasoning
    - IMDB Sentiment-based Text Continuation
    - Table-to-text generation
    - Abstractive Question Answering
    - Machine Translation
    - Dialogue Generation
- Different types of NLG metrics (20+) which can be used as reward functions:
    - Lexical Metrics (eg: ROUGE, BLEU, SacreBLEU, METEOR)
    - Semantic Metrics (eg: BERTSCORE, BLEURT)
    - Task specific metrics (eg: PARENT, CIDER, SPICE)
    - Scores from pre-trained classifiers (eg: Sentiment scores)
- On-policy algorithms of PPO, A2C, TRPO and novel **NLPO (Natural Language Policy Optimization)**
- Actor-Critic Policies supporting causal LMs (eg. GPT-2/3) and seq2seq LMs (eg. T5, BART)

All of these building blocks can be customizable allowing users to train transformer-based LMs to optimize any arbitrary reward function on any dataset of their choice.
   
.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   
   intro/install
   intro/quickstart
   intro/blocks

.. toctree::
   :maxdepth: 2
   :caption: Module Guide
   
   modules/rl4lms.algorithms
   modules/rl4lms.envs
   modules/rl4lms.core_components
   modules/rl4lms.data_pools
   


Citing RL4LMs
-------------
To cite this project in publications:
   
.. code-block:: bibtex

   @inproceedings{Ramamurthy2022IsRL,
      title={Is Reinforcement Learning (Not) for Natural Language Processing?: Benchmarks, Baselines, and Building Blocks for Natural Language Policy Optimization},
      author={Rajkumar Ramamurthy and Prithviraj Ammanabrolu and Kiant{\'e} Brantley and Jack Hessel and Rafet Sifa and Christian Bauckhage and Hannaneh Hajishirzi and Yejin Choi},
      journal={arXiv preprint arXiv:2210.01241},
      url={https://arxiv.org/abs/2210.01241},
      year={2022}
   }


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
