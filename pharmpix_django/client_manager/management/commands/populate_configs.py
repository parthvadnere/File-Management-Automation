# client_manager/management/commands/populate_configs.py
from django.core.management.base import BaseCommand
from client_manager.models import Client, Path, Task, OutputConfig

class Command(BaseCommand):
    help = 'Populate the database with initial client configurations'

    def handle(self, *args, **options):
        # Create Task
        task_5pm, _ = Task.objects.get_or_create(name="5PM-Work", description="5PM Work Task")

        # Define Clients and their configurations
        clients_data = {
            # "ALLIED": {
            #     "paths": [
            #         {"path": "ALLIED/Claims", "file_types": [".txt"], "max_files": 1},
            #         {"path": "ALLIED/Eligibility", "file_types": [".results", ".xlsx"], "max_files": 1}
            #     ],
            #     "output_configs": [
            #         {"path": "ALLIED/Claims", "file_type": "txt", "output_dir": "5PM-Work/Allied/Claims", "filename_template": "Trans_RxClaims_{mmddyyyy}.txt"},
            #         {"path": "ALLIED/Claims", "file_type": "txt", "output_dir": "5PM-Work/RxEOB/Claims/Sapp", "filename_template": "Sapp_Claims_{yyyymmdd}_0004.txt"},
            #         {"path": "ALLIED/Eligibility", "file_type": "results", "output_dir": "5PM-Work/RxEOB/Eligibility", "filename_template": "Sapp_MEM_TRX_{yyyymmdd}_0001.txt"},
            #         {"path": "ALLIED/Eligibility", "file_type": "xlsx", "output_dir": "5PM-Work/Allied/Eligibility", "filename_template": "Trans_Elig_{mmddyyyy}.xlsx"},
            #     ]
            # },
            # "ASR": {
            #     "paths": [
            #         {"path": "ASR/Claims", "file_types": [".txt"], "max_files": 1},
            #         {"path": "ASR/Eligibility", "file_types": [".results", ".xlsx"], "max_files": 1}
            #     ],
            #     "output_configs": [
            #         {"path": "ASR/Claims", "file_type": "txt", "output_dir": "5PM-Work/ASR", "filename_template": "TRX_CLAIMS_{yyyymmdd}.txt"},
            #         {"path": "ASR/Claims", "file_type": "txt", "output_dir": "5PM-Work/RxEOB/Claims/ASR", "filename_template": "ASR_Claims_{yyyymmdd}_0001.txt"},
            #         {"path": "ASR/Eligibility", "file_type": "xlsx", "output_dir": "5PM-Work/ASR", "filename_template": "TRXALBION_PPX_ELIG_{yyyymmdd}_001.xlsx"},
            #         {"path": "ASR/Eligibility", "file_type": "results", "output_dir": "5PM-Work/RxEOB/Eligibility", "filename_template": "TRXALBION_PPX_ELIG_{yyyymmdd}_001.txt"},
            #     ]
            # },
            "BML": {
                "paths": [
                    {"path": "BML/Claims", "file_types": [".txt"], "max_files": 1}
                ],
                "output_configs": [
                    {"path": "BML/Claims", "file_type": "txt", "output_dir": "5PM-Work/RxEOB/Claims/BML", "filename_template": "BML_Claims_{yyyymmdd}_0002.txt"}
                ]
            },
            "UMR": {
                "paths": [
                    {"path": "UMR", "file_types": [".txt"], "max_files": 1},
                    {"path": "UMR/Empire", "file_types": [".txt", ".xls"], "max_files": 1},
                    {"path": "UMR/IOA/Eligibility", "file_types": [".results", ".xlsx"], "max_files": 1},
                    {"path": "UMR/UMR_Exc_OOP", "file_types": [".txt"], "max_files": 1, 
                     "file_pattern": r"trx_UMR_RxEOB__\d{8}\.txt"}
                ],
                "output_configs": [
                    {"path": "UMR", "file_type": "txt", "output_dir": "5PM-Work/UMR-Accum-EFTP-to-SFTP", "filename_template": "PBLXV426_P_TransparentRx_{yyyymmdd}.txt"},
                    {"path": "UMR/Empire", "file_type": "txt", "output_dir": "5PM-Work/RxEOB/Claims/EMP", "filename_template": "EMP_Claims_{yyyymmdd}_0003.txt"},
                    {"path": "UMR/IOA/Eligibility", "file_type": "results", "output_dir": "5PM-Work/RxEOB/Eligibility", "filename_template": "EMP_MEM_TRX_UMR_{yyyymmdd}_0001.txt"},
                    {"path": "UMR/IOA/Eligibility", "file_type": "xlsx", "output_dir": "5PM-Work/UMR/Eligibility", "filename_template": "ErrRpt_P_TransparentRx_IOA_{yyyymmdd}.xlsx"},
                    {"path": "UMR/UMR_Exc_OOP", "file_type": "txt", "output_dir": "5PM-Work/RxEOB/Accum", "filename_template": "EMP_Accum_{yyyymmdd}_0001.txt"}
                ]
            },
            "Lucent Health": {
                "paths": [
                    {"path": "Lucent Health/Claims", "file_types": [".txt"], "max_files": 1}
                ],
                "output_configs": [
                    {"path": "Lucent Health/Claims", "file_type": "txt", "output_dir": "5PM-Work/Lucent_health", "filename_template": "OriginalFilename_{yyyymmdd}.txt"}
                ]
            }
        }

        for client_name, data in clients_data.items():
            client, _ = Client.objects.get_or_create(name=client_name)

            # Create Paths
            for path_data in data["paths"]:
                Path.objects.get_or_create(
                    client=client,
                    path=path_data["path"],
                    file_types=path_data["file_types"],
                    max_files=path_data["max_files"]
                )

            # Create Output Configs
            for output_data in data["output_configs"]:
                path = Path.objects.get(client=client, path=output_data["path"])
                OutputConfig.objects.get_or_create(
                    client=client,
                    path=path,
                    task=task_5pm,
                    file_type=output_data["file_type"],
                    output_dir=output_data["output_dir"],
                    filename_template=output_data["filename_template"]
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with client configurations'))