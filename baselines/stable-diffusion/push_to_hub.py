from diffusers import DiffusionPipeline

if __name__ == '__main__':
    pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe.push_to_hub("SD-cover-art")