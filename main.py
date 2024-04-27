import ffmpeg
import os
import random
# from tqdm import tqdm

# Créez un dossier "input" et mettez-y vos vidéos
DIR = "input"
OUTPUT = "output"


# ICI, on peut changer les mots clés pour les vidéos
# Ces mots clés seront pris au hasard (5 mots clés par vidéo)
# Ils seront insérés dans le titre, la description et les tags de la vidéo (metadata)
KEYWORDS = [
    "makemoneyonline",
    "sidehustle",
    "makemoney",
    "makemoneyfromhome",
    "makemoneyonlinefree",
    "makemoneyfast",
    "makemoneyonlinefast",
    "hustle",
    "business",
    "entrepreneur",
    "entrepreneurship",
    "entrepreneurlife",
    "entrepreneurmindset",
    "entrepreneurquotes",
]


def get_metadata_dict(video_keywords_str):
    metadata_title = video_keywords_str.replace("_", " ")
    metadata_description = "#" + video_keywords_str.replace("_", " #")
    metadata_keywords = video_keywords_str.replace("_", ",")

    metadata_dict = {
        "metadata:g:0": f"title={metadata_title}",
        "metadata:g:1": f"description={metadata_description}",
        "metadata:g:2": f"keywords={metadata_keywords}",
    }
    return metadata_dict


def get_unique_name_and_metadata(str_effect=""):
    """Generate a unique name for the video

    Args:
        str_effect (str, optional): String to append to the name related to the effect. Defaults to "".

    Returns:
        str: Unique name for the video
    """

    video_keywords = random.sample(KEYWORDS, 5)
    unique_hash = random.randint(10000000, 99999999)
    video_keywords_str = "_".join(video_keywords)
    file_name = f"{unique_hash}_{video_keywords_str}_{str_effect}.mp4"

    metadata_dict = get_metadata_dict(video_keywords_str)

    return file_name, metadata_dict


def get_video_dimensions(path):
    """Get the dimensions of the video

    Args:
        path (str): Path to the video

    Returns:
        tuple: Height, Width dimensions of the video
    """
    probe = ffmpeg.probe(path)
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
    )
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    return width, height


def zoom_video(path, factor_percent=110):
    """Zoom in the video by a factor of factor_percent

    Args:
        path (str): Path to the video
        factor_percent (int, optional): Zoom factor. Defaults to 110.

    Returns:
        bool: True if the video was successfully processed, False otherwise
    """

    factor_str = str(factor_percent)
    video_name, metadata = get_unique_name_and_metadata(f"z_{factor_str}")
    res_file_name = os.path.join(OUTPUT, video_name)
    try:
        width, height = get_video_dimensions(path)
        (
            ffmpeg.input(path)
            .filter("scale", w=width * (factor_percent / 100), h=-1)
            .filter("crop", w=width, h=height)
            .output(
                res_file_name,
                loglevel="quiet",
                map_metadata=-1,
                map="0:a",  # map all audio streams
                **metadata,
            )
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


def flip_video(path):
    print(f"Flipping {path}")
    """Flip the video horizontally

    Args:
        path (str): Path to the video

    Returns:
        bool: True if the video was successfully processed, False otherwise
    """

    # Flip is done after zooming, so we take the original video name and append the effect
    processed_video_name = os.path.basename(path)
    processed_video_effect = processed_video_name.split("_")[-1].split(".")[0]
    video_name, metadata = get_unique_name_and_metadata(f"{processed_video_effect}_f")
    res_file_name = os.path.join(OUTPUT, video_name)
    try:
        (
            ffmpeg.input(path)
            .filter("hflip")
            .output(
                res_file_name,
                loglevel="error",
                map_metadata=-1,
                map="0:a",  # map all audio streams
                **metadata,
            )
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print("Error while flipping video")
        print(e)
        return False


def copy_video(path):
    """Copy the video

    Args:
        path (str): Path to the video

    Returns:
        bool: True if the video was successfully processed, False otherwise
    """

    video_name, metadata = get_unique_name_and_metadata("o")
    res_file_name = os.path.join(OUTPUT, video_name)
    try:
        (
            ffmpeg.input(path)
            .output(
                res_file_name,
                loglevel="quiet",
                map_metadata=-1,
                **metadata,
            )
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print(e.stderr)
        return False


def cleanup():
    """Delete all videos in the output folder"""
    print("Cleaning up output folder...")
    files = os.listdir(OUTPUT)
    for file in files:
        os.remove(os.path.join(OUTPUT, file))


def cleanup_input():
    """Delete all videos in the input folder"""
    print("Cleaning up input folder...")
    files = os.listdir(DIR)
    for file in files:
        os.remove(os.path.join(DIR, file))


def init():
    """Create the output folder if it doesn't exist"""
    if not os.path.exists(OUTPUT):
        os.mkdir(OUTPUT)


def main():
    """Generate duplicate videos with different effects"""
    init()
    cleanup()
    print("Zooming on videos...")
    videos_to_process = os.listdir(DIR)
    for video in tqdm(videos_to_process):
        video_path = os.path.join(DIR, video)
        copy_video(video_path)
        zoom_video(video_path, factor_percent=105)
        zoom_video(video_path, factor_percent=110)

    print("Flipping videos...")
    videos_to_process = os.listdir(OUTPUT)
    for video in tqdm(videos_to_process):
        video_path = os.path.join(OUTPUT, video)
        flip_video(video_path)

    cleanup_input()


if __name__ == "__main__":
    main()
