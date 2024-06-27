#!/bin/sh

export MODEL_NAME="jpholanda/SD-coverart-v1"
export TRAIN_DIR="dataset/huggingface/all"
export HUB_MODEL_ID="SD-coverart"

accelerate launch baselines/stable-diffusion/train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --train_data_dir=$TRAIN_DIR \
  --resolution=250 \
  --train_batch_size=48 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --mixed_precision="fp16" \
  --num_train_epochs=5 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --checkpoints_total_limit=1 \
  --resume_from_checkpoint=latest \
  --output_dir=${HUB_MODEL_ID} \
  --push_to_hub \
  --hub_model_id=${HUB_MODEL_ID} \
  --report_to=wandb \
  --validation_prompts='Cover art for a disco album titled "My Love", by "Meux Amis"'

# --max_train_steps=1