import unittest
from unittest import mock
from PIL import Image
import torch

try:
    from diffusers import AutoPipelineForImage2Image
    from diffusers.utils import load_image
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False


@unittest.skipUnless(DIFFUSERS_AVAILABLE, "diffusers not installed")
class TestImageToImagePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pipe = AutoPipelineForImage2Image.from_pretrained(
            "hf-internal-testing/tiny-stable-diffusion-pipe",
            torch_dtype=torch.float32,
        )
        cls.pipe = cls.pipe.to("cpu")

        cls.init_image = Image.new("RGB", (64, 64), color=(255, 0, 0))  

    def test_pipeline_generates_image_from_image(self):
        prompt = "a blue square"
        generator = torch.Generator(device="cpu").manual_seed(42)

        output = self.pipe(
            prompt,
            image=self.init_image,
            generator=generator,
            num_inference_steps=1,  
            strength=0.5  
        )
        image = output.images[0]

        self.assertIsInstance(image, Image.Image)
        self.assertEqual(image.size, (64, 64))

    def test_output_differs_from_input(self):
        generator = torch.Generator(device="cpu").manual_seed(100)
        result = self.pipe(
            "a green circle",
            image=self.init_image,
            generator=generator,
            num_inference_steps=1,
            strength=0.8
        ).images[0]

        self.assertNotEqual(result.tobytes(), self.init_image.tobytes())


if __name__ == "__main__":
    unittest.main()
