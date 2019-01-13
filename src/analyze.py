import argparse
import driveapi

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
    args = p.parse_args()
    # Setup the Google Drive API. This authenticates the application
    # using the given Google Drive credentials.
    dapi = driveapi.DriveAPI(args.drive_credentials, args.drive_folder_id)
    # Get a list of files in the given drive folder id.
    # TODO: To be replaced with Google Sheets API query that reads these
    # files and generates a new sheets with the analyzed data.
    files = dapi.query_files()
    for idx, ifile in enumerate(files):
        print "{idx}. {name} ({mimeType}), {file_id}".format(
            idx=idx + 1,
            name=ifile["name"],
            mimeType=ifile["mimeType"],
            file_id=ifile["id"])
