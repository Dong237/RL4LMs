Installation
============

Local Installation
------------------

.. code-block:: bash

   git clone https://github.com/allenai/RL4LMs.git
   cd RL4LMs
   pip install -e .



Docker
------

We provide also a Dockerfile for development using docker containers containing all the dependencies.

.. code-block:: bash

docker build . -t rl4lms


Additional dependencies
-----------------------

Optionally, coreNLP libraries are required for certain metric computations (eg. SPICE) which can be downloaded through `cd rl4lms/envs/text_generation/caption_metrics/spice && bash get_stanford_models.sh`
