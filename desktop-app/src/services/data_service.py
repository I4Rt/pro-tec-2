from pathlib import Path
import json
import os
from loguru import logger

class DataService:
    
    def __init__(self):
        self.fs_route = Path("/home/i4rt/git/pro-tec-2/tmp_file_system")
        
    def add_report(self, id_, name, last_edit_time):
        os.mkdir(self.fs_route.joinpath(str(id_)))
        with open(self.fs_route.joinpath(str(id_)).joinpath('description.txt'), 'w') as file:
            file.write(
                json.dumps(
                    {
                        'name': name,
                        'description': '',
                        'edit_time': last_edit_time
                    }
                )
            )
        os.mkdir(self.fs_route.joinpath(str(id_)).joinpath('tracks'))
        
    def get_reports_list(self) -> list:
        reports = []
        print(os.listdir(self.fs_route))
        for id_ in os.listdir(self.fs_route):
            try:
                with open(self.fs_route.joinpath(str(id_)).joinpath('description.txt'), 'r') as file:
                    data = json.loads(file.read())
                    reports.append(
                        {
                            "id":id_,
                            "name":data['name'],
                            "description":data['description'],
                            
                            "edit_time":data['edit_time'],
                        }
                    )
            except Exception as e:
                logger.warning(f'get_reports_list: {e}')
        return reports