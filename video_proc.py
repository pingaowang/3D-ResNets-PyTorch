import sys
import os
from os.path import abspath, dirname


# Configuration of folders
ucf_version = '01'
root_project = dirname(dirname(abspath(__file__)))
root_ucfTrainTestlist = os.path.join(root_project, "ucfTrainTestlist")
root_raw_data = os.path.join(root_project, "UCF-101")
root_output = os.path.join(root_project, "avi_ucf-101")


def get_train_test_lists(version='01'):
    """
    Using one of the train/test files (01, 02, or 03), get the filename
    breakdowns we'll later use to move everything.
    """
    # Get our files based on version.
    test_file = os.path.join(root_ucfTrainTestlist, 'testlist') + version + '.txt'
    train_file = os.path.join(root_ucfTrainTestlist, 'trainlist') + version + '.txt'

    # Build the test list.
    with open(test_file) as fin:
        test_list = [row.strip() for row in list(fin)]

    # Build the train list. Extra step to remove the class index.
    with open(train_file) as fin:
        train_list = [row.strip() for row in list(fin)]
        train_list = [row.split(' ')[0] for row in train_list]

    # Set the groups in a dictionary.
    file_groups = {
        'train': train_list,
        'test': test_list
    }

    return file_groups


def move_files(file_groups):
    # Do each of our groups.
    for group, videos in file_groups.items():
        # Do each of our videos.
        for video in videos:
            # Get the parts.
            parts = video.split('/')
            classname = parts[0]
            filename = parts[1]

            _src_path = os.path.join(root_raw_data, video)
            _dir_path = os.path.join(root_output, group, classname)

            # Check if this class exists.
            if not os.path.exists(_dir_path):
                print("Creating folder for %s/%s" % (group, classname))
                os.makedirs(_dir_path)

            # Check if we have already moved this file, or at least that it
            # exists to move.
            if not os.path.exists(_src_path):
                print("Can't find %s to move. Skipping." % (_src_path))
                continue

            # Move it.
            dest = os.path.join(_dir_path, filename)
            print("Moving %s to %s" % (filename, dest))
            os.rename(_src_path, dest)

    print("Done.")


def main():
    """
    Go through each of our train/test text files and move the videos
    to the right place.
    """
    # Get the videos in groups so we can move them.
    group_lists = get_train_test_lists(ucf_version)

    # Move the files.
    move_files(group_lists)

if __name__ == '__main__':
    main()
