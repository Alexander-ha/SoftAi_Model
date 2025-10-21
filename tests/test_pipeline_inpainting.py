import unittest
from PIL import Image
import torch

try:
    from diffusers import AutoPipelineForInpainting
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False


@unittest.skipUnless(DIFFUSERS_AVAILABLE, "diffusers doen't install")
class TestInpaintingPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pipe = AutoPipelineForInpainting.from_pretrained(
            "hf-internal-testing/tiny-stable-diffusion-inpainting",
            torch_dtype=torch.float32,
        )
        cls.pipe = cls.pipe.to("cpu")

        cls.init_image = Image.new("RGB", (64, 64), color=(255, 255, 255))  
        cls.mask_image = Image.new("L", (64, 64), color=0)            
        for x in range(20, 44):
            for y in range(20, 44):
                cls.mask_image.putpixel((x, y), 255)

    def test_pipeline_generates_inpainting_result(self):
        prompt = "a red circle"
        generator = torch.Generator(device="cpu").manual_seed(42)

        output = self.pipe(
            prompt,
            image=self.init_image,
            mask_image=self.mask_image,
            generator=generator,
            num_inference_steps=1,  
            strength=0.5
        )
        image = output.images[0]

        self.assertIsInstance(image, Image.Image)
        self.assertEqual(image.size, (64, 64))

    def test_output_differs_from_input(self):
        generator = torch.Generator(device="cpu").manual_seed(99)
        result = self.pipe(
            "a blue star",
            image=self.init_image,
            mask_image=self.mask_image,
            generator=generator,
            num_inference_steps=1,
            strength=0.7
        ).images[0]

        self.assertNotEqual(result.tobytes(), self.init_image.tobytes())


if __name__ == "__main__":
    unittest.main()