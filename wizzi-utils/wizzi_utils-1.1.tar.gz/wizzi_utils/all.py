from wizzi_utils.misc import main_wrapper
from wizzi_utils.open_cv_tools import first_func


def main():
    print('big program output')
    first_func()
    return


if __name__ == '__main__':
    main_wrapper(
        main_function=main,
        cuda_off=True,
        torch_v=True,
        tf_v=False,
        cv2_v=True,
        with_profiler=False
    )
