import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config


def calc_CC(filename, cc_config):
	file = open(filename, 'r')

	results = CCHarvester(filename, cc_config).gobble(file)

	file_cc = 0

	for i in results:
		print (i.complexity)
		file_cc += int(i.complexity)

	avg_cc = file_cc/ len(results)
	print("Total complexity of file: " + str(file_cc))
	print("Average complexity of file: " + str(avg_cc))
	return file_cc

def main():
	path_list = ['C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\client_lib.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\client.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\locking_service.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\file_server.py',
	'C:\\Users\\Joseph\\Documents\\College\\4th Year\\CS4400_IntApps\\File_System_Project\\github_repo\\directory_service.py']


	cc_config = Config(
		exclude='',
		ignore='venv',
		order=SCORE,
		no_assert=True,
		show_closures=False,
		min='A',
		max='F',
	)

	total_cc = 0

	for path in path_list:
		file_cc = calc_CC(path, cc_config)
		total_cc += file_cc
	
	avg_cc = total_cc/ len(path_list)
	print("Total complexity of all file: " + str(total_cc))
	print("Average CC of all files: " + str(avg_cc))


if __name__ == "__main__":
    main()

