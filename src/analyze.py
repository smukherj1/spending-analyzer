import argparse
import driveapi
import sheetsapi

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "-dc",
        "--drive_credentials",
        required=True,
        help="Path to the Google Drive credentials.json file.")
    p.add_argument(
        "-sc",
        "--sheets_credentials",
        required=True,
        help="Path to the Google Sheets credentials.json file.")
    p.add_argument(
        "-fid",
        "--drive_folder_id",
        required=True,
        help="Folder ID of the Google Drive Folder to analyze")
    p.add_argument(
        "-of",
        "--output_file",
        required=True,
        help="Name of the output Google Sheets file to generate." +
        "It will be generated in the folder specified by --drive_folder_id")
    p.add_argument(
        "-cd",
        "--cache_directory",
        default="",
        help="OPTIONAL: Directory where cached tokens will be stored")
    args = p.parse_args()
    # Setup the Google Drive API. This authenticates the application
    # using the given Google Drive credentials.
    dapi = driveapi.DriveAPI(args.drive_credentials, args.drive_folder_id,
                             args.cache_directory)
    sapi = sheetsapi.SheetsAPI(args.sheets_credentials, args.cache_directory)
    # Get a list of files in the given drive folder id.
    # TODO: To be replaced with Google Sheets API query that reads these
    # files and generates a new sheets with the analyzed data.
    files = dapi.query_files()
    data = []
    output_file_id = None
    for idx, ifile in enumerate(files):
        if ifile["name"] == args.output_file:
            output_file_id = ifile["id"]
            print "Info: Clearing  {idx}. {name}, {file_id}".format(
                idx=idx + 1, name=ifile["name"], file_id=output_file_id)
            sapi.clear_file(output_file_id)
            continue
        print "Info: Analyzing {idx}. {name}, {file_id}".format(
            idx=idx + 1, name=ifile["name"], file_id=ifile["id"])
        values = sapi.query_doc(ifile["id"])
        data.extend(values)
    if output_file_id is None:
        print "Info: Generating output file: {}".format(args.output_file)
        output_file_id = dapi.create_output_file(args.output_file)["id"]
