from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):
    help = 'Generate a secret key for the project'
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--update-env",
            action="store_true",
            help="Update the SECRET_KEY in the .env file",
        )
        parser.add_argument(
            "--env-file",
            type=str,
            default=".env",
            help="Path to the .env file",
        )
        
    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        
        if options["update_env"]:
            env_path = Path(options["env_file"])
            try:
                if not env_path.exists():
                    env_path.write_text(f"SECRET_KEY={secret_key}\n")
                    self.stdout.write(
                        self.style.SUCCESS(f"File {env_path} created and updated with SECRET_KEY")
                    )
                    return
                lines = env_path.read_text().splitlines()
                updated = False
                for i,line in enumerate(lines):
                    if line.startswith("SECRET_KEY="):
                        lines[i] = f"SECRET_KEY={secret_key}"
                        updated = True
                        break
                if not updated:
                    lines.append(f"SECRET_KEY={secret_key}")
                    
                env_path.write_text("\n".join(lines)+"\n")
                self.stdout.write(
                    self.style.SUCCESS(f"File {env_path} updated with SECRET_KEY")
                )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error updating {env_path}: {e}")
                )
        else:
            self.stdout.write(secret_key)