import cv2

from ipso_phen.ipapi.base.ipt_abstract import IptBase
from ipso_phen.ipapi.base.ip_common import ToolFamily, ensure_odd


from ipso_phen.ipapi.base.ipt_abstract import IptBase


import os
import logging

logger = logging.getLogger(os.path.splitext(__name__)[-1].replace(".", ""))


class IptGaussianFiltering(IptBase):
    def build_params(self):
        self.add_enabled_checkbox()

        self.add_spin_box(
            name="kernel_size",
            desc="Gaussian filter size (odd values only)",
            default_value=3,
            minimum=3,
            maximum=101,
        )

    def process_wrapper(self, **kwargs):
        wrapper = self.init_wrapper(**kwargs)
        if wrapper is None:
            return False

        res = False
        try:
            if self.get_value_of("enabled") == 1:
                kernel_size = ensure_odd(self.get_value_of("kernel_size"))

                self.result = cv2.GaussianBlur(
                    src=wrapper.current_image,
                    ksize=(kernel_size, kernel_size),
                    sigmaX=(kernel_size - 1) / 6,
                    sigmaY=(kernel_size - 1) / 6,
                )

                wrapper.store_image(self.result, "current_image")
                res = True
            else:
                wrapper.store_image(wrapper.current_image, "current_image")
                res = True
        except Exception as e:
            res = False
            logger.error(f"Median Fileter FAILED, exception: {repr(e)}")
        else:
            pass
        finally:
            return res

    @property
    def name(self):
        return "Gaussian filtering"

    @property
    def package(self):
        return "TPMP"

    @property
    def is_wip(self):
        return True

    @property
    def real_time(self):
        return True

    @property
    def result_name(self):
        return "image"

    @property
    def output_kind(self):
        return "image"

    @property
    def use_case(self):
        return ["Mask cleanup", "Pre processing"]

    @property
    def description(self):
        return """'Apply Gaussian filter"""
