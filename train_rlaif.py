import os
import yaml
from datasets import load_dataset
from argparse import ArgumentParser

import sys
sys.path.append("/cluster/home/RL4LMs")

from rl4lms.envs.text_generation.logging_utils import Tracker
from rl4lms.envs.text_generation.training_utils import OnPolicyTrainer
from rl4lms.envs.text_generation.registry import DataPoolRegistry
from rl4lms.data_pools.text_generation_pool import Sample, TextGenPool
from rl4lms.data_pools.custom_text_generation_pools import CommonGen


class EmpatheticDialoguesDataPool(TextGenPool):
   EOU_TOKEN = "<EOU>"
   @classmethod
   def prepare(cls, split: str, context_size=0):
        split = CommonGen.gen_split_name(split)
        dataset = load_dataset("empathetic_dialogues", split=split)
        dataset = dataset.map(
            lambda x: {'utterance': x['utterance'].replace('_comma_', ',')}
            )
        samples = []
        contexts = []
        for ix, item in enumerate(dataset):
            utterance = item["utterance"]
            if len(contexts) >= context_size:
                context = EmpatheticDialoguesDataPool.EOU_TOKEN.join(contexts[-context_size:]) 
                context += " " + EmpatheticDialoguesDataPool.EOU_TOKEN
                target = utterance + EmpatheticDialoguesDataPool.EOU_TOKEN
                sample = Sample(id=f"{split}_{ix}",
                                prompt_or_input_text=context,
                                references=[target],
                                meta_data={
                                    "context": [item["context"]],
                                    })
                samples.append(sample)
            contexts.append(utterance)
            
        pool_instance = cls(samples)
        return pool_instance


def main(
    config_path: str,
    project_name: str,
    experiment_name: str,
    base_path_to_store_results: str,
    entity_name: str,
    log_to_wandb: bool,
):
    
    # register the datapool
    DataPoolRegistry.add("empathetic_dialogues", EmpatheticDialoguesDataPool)

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

    # instantiate the trainer here
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

if __name__ == '__main__':

    parser = ArgumentParser(description="Fine-tune LM to generate controlled text")
    parser.add_argument(
        "--config_path", 
        type=str, 
        help="path to the config file"
        )
    parser.add_argument(
        "--project_name", 
        type=str, 
        help="WANDB project name", 
        default="rl4lm_exps"
        )
    parser.add_argument(
        "--experiment_name",
        type=str,
        help="WANDB experiment name",
        default="rl4lm_experiment",
        )
    parser.add_argument(
        "--entity_name", 
        type=str, 
        help="WANDB entity name", 
        default=None
        )
    parser.add_argument(
        "--base_path_to_store_results",
        type=str,
        help="Base path to store experiment results",
        default=os.getcwd(),
        )
    parser.add_argument(
        "--log_to_wandb", 
        type=bool, 
        default=True, 
        help="Whether to use wandb logging"
        )
    args = parser.parse_args()

    main(
        args.config_path,
        args.project_name,
        args.experiment_name,
        args.base_path_to_store_results,
        args.entity_name,
        args.log_to_wandb,
    )

