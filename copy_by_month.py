#!/usr/bin/env python3

import argparse
import exifread
import os
import re
import shutil

def retrieve_year_month(path):
  '''returns a tuple of the year and month of the image file, both in string format;
  None if the file has no EXIF information or some other error has occurred'''
  r_yearmonth = re.compile('(\d{4}):(\d{2}):\d{2} \d{2}:\d{2}:\d{2}')

  try:
    f = open(path, 'rb')
    tags = exifread.process_file(f, details=False, stop_tag='DateTimeOriginal')
    img_datetime = tags['EXIF DateTimeOriginal'].values
    return r_yearmonth.match(img_datetime).groups()
  except Exception as e:
    print(e)
    return None


def organize_image(source, target):
  '''copy and organize images'''
  for dirpath, subdirs, filenames in os.walk(source):
    for filename in filenames:
      source_file = os.path.join(dirpath, filename)
      print(source_file)
      # get metadata, compute target path, and copy
      yearmonth = retrieve_year_month(source_file)
      if yearmonth:
        target_dir = os.path.join(target, yearmonth[0], yearmonth[1])
        if not os.path.exists(target_dir):
          os.makedirs(target_dir)
        shutil.copy2(source_file, target_dir)
      else:
        print('{} was not copied'.format(source_file))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Traverse all images (anything with valid EXIF) under a directory and regroups them by year/month.')
  parser.add_argument('-s', '--source', dest='source', metavar='SOURCE', help='root directory of all source images', required=True)
  parser.add_argument('-t', '--target', dest='target', metavar='TARGET', help='target directory under which images will be copied to and organized', required=True)

  args = parser.parse_args()
  print("Starting to copy images under {source} to {target}, organized by year/month: ".format(source=args.source, target=args.target))

  organize_image(args.source, args.target)

  print("finished.")
