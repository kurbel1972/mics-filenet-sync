from asyncio import subprocess
import sys
from src.core.drives_mount.network_drives import NetworkDriveManager
from src.core.history_files.copy_to_history import HistoryCopier
from src.core.filenet.filenet_process import FileNetProcessor
from src.utils.vpn_active import is_vpn_connected
import os
import logging
from src.utils.logging_config import setup_logging
import subprocess

setup_logging()

os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.version_info >= (3, 7):
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')

def main(): 
    # Initialize logging configuration
    logging.info("                                                                                                              ")
    logging.info("                                                                                                              ")
    logging.info("**************************************************************************************************************")
    logging.info("************************************                                      ************************************")
    logging.info("************************************ Main - Starting MICS FileNet Sync... ************************************")
    logging.info("************************************                                      ************************************")
    logging.info("**************************************************************************************************************")
    if is_vpn_connected():
        try:
            # 1st: Mount network drives
            print(" Mounting network drives...")
            logging.info("*********************************** Main - Begin Mounting network drives... **********************************")
            drive_manager = NetworkDriveManager()
            drive_manager.mount_network_drives()
            logging.info("************************************ Main - End Mounting network drives... ***********************************")

            if len(sys.argv) > 1:
                date_input = sys.argv[1]
            else:
                try:
                    date_input = input("Enter the date to search for files (YYYY-MM-DD): ").strip()
                except KeyboardInterrupt:
                    print("\n Operation cancelled by user.")
                    logging.info("*********************************** Main - Operation cancelled by user. ***********************************")
                    return

            # 2st: Copy files in MICS to history
            logging.info(f"************************** Main - Begin Copying files to history for date: {date_input} ************************")
            copier = HistoryCopier(date_input)
            all_files_collected = copier.copy_files_to_history()
            print(f"\n Total files detected for history: {len(all_files_collected)}")
            logging.info(f"*********************************** Main - End Total files detected for history: {len(all_files_collected)} ***********************************")

            # 3rd: Process find files in FileNet and send to recovery des
            logging.info(f"************************** Main - Begin Processing files in FileNet for date: {date_input} **************************")
            processor = FileNetProcessor()
            processor.process_files(all_files_collected, date_input)
            logging.info("*********************************** Main - End Processing files in FileNet ***********************************")
            
            
            try:
                # Execute your main script
                subprocess.run(['python', 'src/core/manage_directories/mantain_directory.py'], check=True)
                print("********************************* Script mantain_directory executed successfully. *********************************")
            except subprocess.CalledProcessError as e:
                print(f"Error executing the script mantain_directory: {e}", file=sys.stderr)
                
        except Exception as e:
            print(f"Error checking VPN connection: {e}", file=sys.stderr)
            logging.error(f"*********************************** Main - Error in main process: {e} ***********************************")
            return False   

if __name__ == "__main__":
    main()