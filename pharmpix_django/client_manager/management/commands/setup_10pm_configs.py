# client_manager/management/commands/setup_10pm_configs.py
from django.core.management.base import BaseCommand
from client_manager.models import Client, FileConfig

class Command(BaseCommand):
    help = 'Set up initial 10PM task configurations for clients'

    def handle(self, *args, **kwargs):
        # Allied
        allied, _ = Client.objects.get_or_create(
            name='ALLIED',
            defaults={
                'sftp_host': 'sftp.allied.com',
                'sftp_username': 'allied_user',
                'sftp_password': 'allied_pass',
                'sftp_port': 22,
                'is_active': True,
            }
        )

        FileConfig.objects.get_or_create(
            client=allied,
            file_type='accumulator',
            defaults={
                'remote_path': '/home/AHB/Incoming_Files',
                'file_pattern': 'Trans_Accums_YYYYMMDD.TXT',
                'local_path': '10PM/Sapp/Accum',
                'renamed_pattern': 'TRX_PPX_MOOP_YYYYMMDD_003',
                'is_active': True,
            }
        )
        FileConfig.objects.get_or_create(
            client=allied,
            file_type='eligibility',
            defaults={
                'remote_path': '/home/AHB/Incoming_Files',
                'file_pattern': 'TRANSPARENTRX_YYYYMMDD.TXT',
                'local_path': '10PM/Sapp/Eligibility',
                'renamed_pattern': 'SAPP_PPX_ELIGIBILITY_YYYYMMDD_001',
                'is_active': True,
            }
        )

        # ASR
        asr, _ = Client.objects.get_or_create(
            name='ASR',
            defaults={
                'sftp_host': 'sftp.asr.com',
                'sftp_username': 'asr_user',
                'sftp_password': 'asr_pass',
                'sftp_port': 22,
                'is_active': True,
            }
        )

        FileConfig.objects.get_or_create(
            client=asr,
            file_type='accumulator',
            defaults={
                'remote_path': '/home/ASR/Incoming_Files',
                'file_pattern': 'Accum_ASR_YYYYMMDD.txt',
                'local_path': '10PM/ASR/Accum',
                'renamed_pattern': 'TRXALBION_PPX_ACCUM_YYYYMMDD_001',
                'is_active': True,
            }
        )
        FileConfig.objects.get_or_create(
            client=asr,
            file_type='eligibility',
            defaults={
                'remote_path': '/home/ASR/Incoming_Files',
                'file_pattern': 'Elig_ASR_YYYYMMDD.txt',
                'local_path': '10PM/ASR/Eligibility',
                'renamed_pattern': 'TRXALBION_PPX_ELIG_YYYYMMDD_001',
                'is_active': True,
            }
        )

        # UMR
        umr, _ = Client.objects.get_or_create(
            name='UMR',
            defaults={
                'sftp_host': 'sftp.umr.com',
                'sftp_username': 'umr_user',
                'sftp_password': 'umr_pass',
                'sftp_port': 22,
                'is_active': True,
            }
        )

        FileConfig.objects.get_or_create(
            client=umr,
            file_type='accumulator',
            defaults={
                'remote_path': '/out/transparentrx.com',
                'file_pattern': 'TRANSPARENTRX_ATT_YYYYMMDD_HHMMSS.TXT',
                'local_path': '10PM/UMR/Accum',
                'renamed_pattern': 'YYYYMMDD_ACCUM_UMR',
                'is_active': True,
            }
        )
        FileConfig.objects.get_or_create(
            client=umr,
            file_type='eligibility',
            defaults={
                'remote_path': '/out/transparentrx.com',
                'file_pattern': 'MEM_TRX_UMR_YYYYMMDD_HHMMSS.TXT',
                'local_path': '10PM/UMR/Eligibility',
                'renamed_pattern': 'MEM_TRX_UMR_YYYYMMDD_0001',
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up 10PM task configurations'))