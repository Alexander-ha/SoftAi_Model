import unittest
from unittest.mock import patch
from PIL import Image
import torch

try:
    from diffusers import AutoPipelineForText2Image
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False


@unittest.skipUnless(DIFFUSERS_AVAILABLE, "diffusers not installed")
class TestTextToImagePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pipe = AutoPipelineForText2Image.from_pretrained(
            "hf-internal-testing/tiny-stable-diffusion-xl-pipe",  # Более совместимая модель
            torch_dtype=torch.float32,
        )
        cls.pipe = cls.pipe.to("cpu")

    def test_pipeline_generates_image(self):
        prompt = "a red apple on a wooden table"
        generator = torch.Generator(device="cpu").manual_seed(42)

        output = self.pipe(prompt, generator=generator, num_inference_steps=1, height=64, width=64)
        image = output.images[0]

        self.assertIsInstance(image, Image.Image)
        self.assertEqual(image.size, (64, 64))  

    def test_different_prompts_produce_different_images(self):
        generator = torch.Generator(device="cpu").manual_seed(100)
        img1 = self.pipe("a cat", generator=generator, num_inference_steps=1, height=64, width=64).images[0]
        img2 = self.pipe("a dog", generator=generator, num_inference_steps=1, height=64, width=64).images[0]

        self.assertNotEqual(img1.tobytes(), img2.tobytes())


if __name__ == "__main__":
    unittest.main()