import os
from argparse import ArgumentParser

import yaml

import sys
sys.path.append("/cluster/home/RL4LMs")

from rl4lms.envs.text_generation.logging_utils import Tracker
from rl4lms.envs.text_generation.training_utils import OnPolicyTrainer


parser = ArgumentParser(description="Fine-tune LM to generate controlled text")
parser.add_argument("--config_path", type=str, help="path to the config file")
parser.add_argument(
    "--project_name", type=str, help="WANDB project name", default="rl4lm_exps"
)
parser.add_argument(
    "--experiment_name",
    type=str,
    help="WANDB experiment name",
    default="rl4lm_experiment",
)
parser.add_argument(
    "--entity_name", type=str, help="WANDB entity name", default=None
)
parser.add_argument(
    "--base_path_to_store_results",
    type=str,
    help="Base path to store experiment results",
    default=os.getcwd(),
)
parser.add_argument(
    "--log_to_wandb", default=True, help="Whether to use wandb logging"
)
args = parser.parse_args()


args.config_path = "/cluster/home/RL4LMs/config_debug.yml"
args.project_name = "rl4lms-debug"
args.experiment_name = "debug-aceso-v1"
args.base_path_to_store_results = "./debug"
args.entity_name = "youxiang"
args.log_to_wandb = True

def main(
    config_path: str,
    project_name: str,
    experiment_name: str,
    base_path_to_store_results: str,
    entity_name: str,
    log_to_wandb: bool,
):
    
    os.environ['TRANSFORMERS_CACHE'] = '/scratch/huggingface'

    # load the config file
    with open(config_path, "r") as fp:
        config = yaml.safe_load(fp)

    # load tracker
    tracker = Tracker(
        base_path_to_store_results,
        config,
        project_name,
        experiment_name,
        entity_name,
        log_to_wandb,
    )

    trainer = OnPolicyTrainer(
        tokenizer_config=config["tokenizer"],
        datapool_config=config["datapool"],
        reward_config=config["reward_fn"],
        env_config=config["env"],
        on_policy_alg_config=config["alg"],
        train_eval_config=config["train_evaluation"],
        tracker=tracker,
        )
    trainer.train_and_eval()

if __name__ == "__main__":

    main(
        args.config_path,
        args.project_name,
        args.experiment_name,
        args.base_path_to_store_results,
        args.entity_name,
        args.log_to_wandb,
    )
