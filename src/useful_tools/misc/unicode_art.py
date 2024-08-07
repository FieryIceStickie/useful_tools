import numpy as np
from typing import Literal
from PIL import Image, ImageFile

type ImgArr = np.ndarray[tuple[int, int, Literal[4]], np.dtype[np.int8]]
type PixelArr = np.ndarray[tuple[int, int], np.dtype[np.bool]]
type TileArr = np.ndarray[tuple[int, int, Literal[3], Literal[2]], np.dtype[np.bool]]
type FlagArr = np.ndarray[tuple[int, int], np.dtype[np.int8]]
type CharArr = np.ndarray[tuple[int, int], np.dtype[np.int32]]


def conv_pixel_flag(flag: int):
    if not (0 <= flag <= 0b111111):
        raise ValueError('Bit flag should only provide six pixels')
    offset = 0x1faff
    exceptions = {
        0: 32,  # Space
        0b10101: 0x258C,  # Left half
        0b101010: 0x2590,  # Right half
        0b111111: 0x2588,  # Full block
    }
    # Left and right halves already exist for 2x2, so they are skipped
    return (
        exceptions[flag]
        if flag in exceptions
        else offset + flag - (flag > 0b10101) - (flag > 0b101010)
    )


def flags_to_chars(flags: FlagArr) -> CharArr:
    flags = np.array(flags, np.int32)
    return np.select(
        # Space, Left half, Right half, Full block
        [flags == 0, flags == 0b10101, flags == 0b101010, flags == 0b111111],
        [32, 0x258C, 0x2590, 0x2588],
        # Left and right halves already exist for 2x2, so they are skipped
        0x1faff + flags - (flags > 0b10101) - (flags > 0b101010)
    )


def tile_pixel_arr(pixel_arr: PixelArr, tile_width: int, tile_height: int) -> TileArr:
    height, width = pixel_arr.shape
    return np.moveaxis(pixel_arr.reshape(
        height // tile_height, 3, tile_height // 3,
        width // tile_width, 2, tile_width // 2,
    ), 3, 1).swapaxes(3, 4)


def gen_unicode_str_from_img(
        img: ImageFile,
        shape: tuple[int, int] | int, *,
        pad: int = 0,
        tolerance: int = 10,
        ratio: float = 0.5
) -> str:
    if isinstance(shape, int):
        shape = shape, shape
    img_arr = np.array(img)
    if pad:
        img_arr = img_arr[pad:-pad, pad:-pad]
    img_arr = img_arr.repeat(2, axis=1)
    pixels = np.sum(img_arr[..., :3], axis=-1) > tolerance
    tiles = tile_pixel_arr(pixels, *shape)
    bits = np.average(tiles, axis=(-1, -2)) >= ratio
    mask = np.arange(6).reshape((3, 2))
    flags = np.bitwise_or.reduce((np.array(bits, dtype=np.int8) << mask), axis=(-1, -2))
    chars = flags_to_chars(flags)
    return np.c_[
        chars,
        np.repeat(np.array([10], dtype=np.int32), chars.shape[0], )
    ].tobytes().decode('utf-32').rstrip('\n')


if __name__ == '__main__':
    img_path = '/Users/stickie/Desktop/Stuff/Images/YouSymbol.png'
    art_str = gen_unicode_str_from_img(Image.open(img_path), 60, pad=200)
    print(art_str)
