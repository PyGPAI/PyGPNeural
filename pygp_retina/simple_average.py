import numpy as np

if False:
    import cv2


def avg_total_color(frame  # type: np.ndarray
                    ):
    # from here: https://stackoverflow.com/a/43112217/782170
    avg = [frame[:,:,i].mean() for i in range(frame.shape[-1])]
    return avg