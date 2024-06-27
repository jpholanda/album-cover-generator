from diffusers import StableDiffusionPipeline
from transformers import BertModel, BertTokenizer

if __name__ == "__main__":
    bert_tokenizer = BertTokenizer.from_pretrained('google-bert/bert-base-multilingual-cased')
    bert_model = BertModel.from_pretrained('google-bert/bert-base-multilingual-cased')

    pipe = StableDiffusionPipeline.from_pretrained("OFA-Sys/small-stable-diffusion-v0")

    model = StableDiffusionPipeline(
        tokenizer=bert_tokenizer,
        text_encoder=bert_model,
        vae=pipe.vae,
        unet=pipe.unet,
        scheduler=pipe.scheduler,
        safety_checker=pipe.safety_checker,
        feature_extractor=pipe.feature_extractor,
        image_encoder=pipe.image_encoder
    )
    model.push_to_hub("SDBert-coverart-v0")