from PIL import Image
from ComfyUI_UltimateSDUpscale.utils import tensor_to_pil, pil_to_tensor
from ComfyUI.comfy_extras.nodes_upscale_model import ImageUpscaleWithModel
from ComfyUI_UltimateSDUpscale.modules import shared

if (not hasattr(Image, 'Resampling')):  # For older versions of Pillow
    Image.Resampling = Image


class Upscaler:

    def _upscale(self, img: Image, scale):
        if scale == 1.0:
            return img
        if (shared.actual_upscaler is None):
            return img.resize((img.width * scale, img.height * scale), Image.Resampling.NEAREST)
        tensor = pil_to_tensor(img)
        image_upscale_node = ImageUpscaleWithModel()
        (upscaled,) = image_upscale_node.upscale(shared.actual_upscaler, tensor)
        return tensor_to_pil(upscaled)

    def upscale(self, img: Image, scale, selected_model: str = None):
        shared.batch = [self._upscale(img, scale) for img in shared.batch]
        return shared.batch[0]


class UpscalerData:
    name = ""
    data_path = ""

    def __init__(self):
        self.scaler = Upscaler()
