from pathlib import Path
from knack.log import get_logger
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..common.file_loader import LasParser, LocalFileLoader, FileUtilities
from ..service.record_mapper import LasToRecordMapper
from ..common.configuration import Configuration
from ..wrapper.json_writer import JsonToFile

import re
import os

logger = get_logger(__name__)


def printlas(input_path):
  """
    Print a LAS file header
    :param str input_path: Path and filename of a LAS file or folder containing LAS files
    """

  las_parser = LasParser(LocalFileLoader())
  logger.info(f"LAS path: {input_path}")
  for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
    logger.warning(f"LAS file: {file_path}")
    las_data = las_parser.load_las_file(file_path)
    print(las_data.header)


def convert(input_path: str, wellbore_id: str, config_path: str = None):
  """
    Convert a LAS file to Wellbore and Well Log and write to JSON files.
    :param str input_path: Path and filename of a LAS file or folder containing LAS files
    :param str wellbore_id: The wellbore id
    :param str config_path: Path to the configuration file
  """

  # Check if las version is 3 with multi dataset
  if check_version_3_multi_ds(input_path):
    logger.warning(f"Found LAS file version 3 with multi dataset!")
    return convert_version_3_with_multi_ds(input_path, wellbore_id, config_path)

  config_path = EnvironmentVarHelper.get_config_path(config_path)

  las_parser = LasParser(LocalFileLoader())
  config = Configuration(LocalFileLoader(), config_path)

  logger.info(f"LAS path: {input_path}")
  for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
    logger.warning(f"LAS file: {file_path}")
    las_data = las_parser.load_las_file(file_path)

    mapper = LasToRecordMapper(las_data, config)
    wellbore_record = mapper.map_to_wellbore_record()
    welllog_record = mapper.map_to_well_log_record(wellbore_id)

    path = Path(file_path)
    writer = JsonToFile()

    writer.write(wellbore_record.get_raw_data(), path.with_suffix('.wellbore.json'))
    logger.warning(f"Wellbore record file created: {path.with_suffix('.wellbore.json')}")
    writer.write(welllog_record.get_raw_data(), path.with_suffix('.welllog.json'))
    logger.warning(f"Well log record file created: {path.with_suffix('.welllog.json')}")


def split_files_version_3_with_multi_ds(input_path: str):
  # For header, contains version, well and other general definitions
  head = []
  # For current dataset
  body = []
  # All dataset files
  files = []
  # Current file for current dataset
  cur_file = None
  # Initial flag for done dumping header
  init = False
  with open(input_path, "r") as f:
    for line in f:
      # Initialize
      if not init:
        # Check for first dataset section
        # !Notice: First remove the delimiter section
        if re.search(r"(dlm|comma)", line, re.IGNORECASE):
          pass
        else:
          str_match = re.match(r"~(.*)(_|\s)(parameter|definition)", line, re.IGNORECASE)
          if str_match:
            # Get the current file for current dataset
            filename = str_match.group(1)
            cur_file = f"{os.path.dirname(input_path) or '.'}/{Path(input_path).stem}_{filename}.las"
            files.append(cur_file)
            # Add first dataset parameter section to head
            head.append("~Parameter\n")
            # Initialize done
            init = True
          else:
            head.append(line)
      else:
        # Check for next dataset section
        str_match = re.match(r"~(.*)(_|\s)parameter", line, re.IGNORECASE)
        if str_match:
          # If next dataset section, write the current dataset to file first
          with open(cur_file, "w") as _f:
            _f.writelines(head)
            _f.writelines(body)
          # Then get the next file for next dataset
          filename = str_match.group(1)
          cur_file = f"{os.path.dirname(input_path) or '.'}/{Path(input_path).stem}_{filename}.las"
          files.append(cur_file)
          # Reset the body for current dataset
          body = []
        else:
          # Check for data section
          if "data" in line.lower():
            body.append("~A\n")
          # Check for dataset curves definition section
          elif re.match(r"~(.*)(_|\s)definition", line, re.IGNORECASE):
            body.append("~Curve\n")
          else:
            body.append(line)
  # Write the last dataset section (EOF)
  with open(cur_file, "w") as _f:
    _f.writelines(head)
    _f.writelines(body)

  # Return files for converting
  return files


def remove_split_multi_ds_files(files: list[str]):
  for file in files:
    os.remove(file)


def convert_version_3_with_multi_ds(input_path: str, wellbore_id: str, config_path: str = None):
  # Get the split dataset files
  files = split_files_version_3_with_multi_ds(input_path)

  for file in files:
    input_path = file

    config_path = EnvironmentVarHelper.get_config_path(config_path)

    las_parser = LasParser(LocalFileLoader())
    config = Configuration(LocalFileLoader(), config_path)

    logger.info(f"LAS path: {input_path}")
    for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
      logger.warning(f"LAS file: {file_path}")
      las_data = las_parser.load_las_file(file_path)

      mapper = LasToRecordMapper(las_data, config)
      wellbore_record = mapper.map_to_wellbore_record()
      welllog_record = mapper.map_to_well_log_record(wellbore_id)

      path = Path(file_path)
      writer = JsonToFile()

      writer.write(wellbore_record.get_raw_data(), path.with_suffix('.wellbore.json'))
      logger.warning(f"Wellbore record file created: {path.with_suffix('.wellbore.json')}")
      writer.write(welllog_record.get_raw_data(), path.with_suffix('.welllog.json'))
      logger.warning(f"Well log record file created: {path.with_suffix('.welllog.json')}")

  # Then delete the split dataset files
  remove_split_multi_ds_files(files)


def check_version_3_multi_ds(input_path: str):
  with open(input_path, "r") as f:
    for line in f:
      if re.match(r"^VERS", line):
        if re.search(r"\s*2.0*\s*", line):
          return False
        else:
          break
    for line in f:
      if re.match(r"^~curve", line, re.IGNORECASE):
        return False
    return True
