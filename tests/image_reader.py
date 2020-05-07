import os
import glob
import cv2


class ImageReader:
    
    def __init__(self, image_dir, fname_prefix='sample_', fname_ext='jpg'):
        if not os.path.isdir(image_dir):
            raise Exception(f'Directory "{image_dir}" is not a dir!')

        self._image_dir = image_dir
        self._fname_prefix = fname_prefix
        self._fname_ext = fname_ext

    
    def sample_number(self):
        mask = self._fname_prefix + '*.' + self._fname_ext
        return len(glob.glob(os.path.join(self._image_dir, mask)))


    def _sample_file_name(self, sample_id):
        return self._fname_prefix + str(sample_id).rjust(2, "0") + '.' + self._fname_ext
    

    def _sample_full_file_name(self, sample_id):
        return os.path.join(self._image_dir, self._sample_file_name(sample_id))


    def read_sample(self, sample_id):
        numpy_image = cv2.imread(self._sample_full_file_name(sample_id))
        return numpy_image
