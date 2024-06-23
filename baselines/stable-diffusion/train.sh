#!/bin/sh

export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export TRAIN_DIR="dataset/huggingface"
export HUB_MODEL_ID="SD-cover-art"

accelerate launch train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --train_data_dir=$TRAIN_DIR \
  --use_ema \
  --resolution=250 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --mixed_precision="fp16" \
  --max_train_steps=15000 \
  --learning_rate=1e-05 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir=${HUB_MODEL_ID} \
  --push_to_hub \
  --hub_model_id=${HUB_MODEL_ID}