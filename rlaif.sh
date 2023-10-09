# export CUDA_LAUNCH_BLOCKING=1
# export TRANSFORMERS_CACHE="/scratch/huggingface"
# export WORLD_SIZE=6
# export CUDA_VISIBLE_DEVICES=1,2,3,4,5,6

# torchrun --nproc_per_node=6 --master_port=3469 

python train_rlaif.py \
    --config_path /cluster/home/RL4LMs/config_empathy.yml \
    --project_name "rl4lm-test" \
    --experiment_name "aceso-empadata-lora-v1" \
    --base_path_to_store_results "/cluster/home/RL4LMs/results" \
    --entity_name youxiang \
    --log_to_wandb True \
