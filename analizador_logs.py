import re
import argparse
import datetime

def format_logs(file_logs: str) -> list[str]:
    return file_logs.split('\n')

def format_filters(filters: str) -> list[str]:
    return filters.split(',')

def search_pattern(filter: str) -> str:
    """
    This function searches for the pattern to apply to the logs depending on the filter

    :Args:
    filter: str -> filter to apply to the logs

    :Returns:
    str: pattern to apply to the logs

    """
    is_ip: str =r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    is_status_code: str =r'\d{3}'
    is_http_method: str =r'GET|POST|PUT|DELETE'
    is_date: str =r'\d{2}\/\w{3}\/\d{4}'

    if re.search(is_ip, filter):
        return is_ip
    
    elif re.search(is_date, filter):
        return is_date

    elif re.search(is_status_code, filter):
        return r"(?<=\s)[1-5][0-9]{2}(?=\s)"
    
    elif re.search(is_http_method, filter):
        return is_http_method
    
    else:
        return filter
    
def filter_logs(list_logs: list[str], filters: list[str]) -> list[str]:
    """
    This function filters the logs based on the filter provided

    :Args:
    list_logs: list[str] -> list of logs
    filters: list[str] -> filters to apply to the logs

    :Returns:
    list[str]: list of logs that match

    """
    patterns: list[str] = []
    for filter in filters:
        pattern = search_pattern(filter)
        if pattern == filter:
            print("Pattern not found")
            return []
        patterns.append(pattern)
        
    for index,pattern in enumerate(patterns):
        list_logs = [log for log in list_logs if re.search(pattern, log) and re.search(pattern, log).group() == filters[index]]

    if not list_logs:
        print("No logs found")

    return list_logs
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some logs. [Example ejecution:python analizador_logs.py -logfile server_logs.log -filters 200,GET]')
    parser.add_argument('-logfile',required=True, type=str, help='The log file to process')
    parser.add_argument('-filters',required=True ,type=str,
                         help='The filters to apply to the logs (IP[example:8.8.8.8], status code[example:200], HTTP[example:GET] method and date[example:01/Jan/2021])')

    args = parser.parse_args()

    try:
        with open(args.logfile, 'r') as file:
            file_logs: str = file.read()
    except FileNotFoundError:
        print(f"File {args.logfile} not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    start_time = datetime.datetime.now()
    list_logs: list[str] = format_logs(file_logs)
    list_filters: list[str] = format_filters(args.filters)
    logs: list[str] = filter_logs(list_logs,list_filters)

    if logs:
        
        end_time = datetime.datetime.now()
        print(f"Logs found in {end_time - start_time}")
        print(f"Logs found: {len(logs)}")

        show_results = input("Do you want to see the logs? (y/n): ")
        if show_results.lower() == 'y':
            for log in logs:
                print(log)
        export = input("Do you want to export the logs to a file? (y/n): ")
        if export.lower() == 'y':
            file_name = input("Enter the file name to export the logs: ")
            with open(f'{file_name}.txt', 'w') as file:
                for log in logs:
                    file.write(f"{log}\n")
            print("Logs exported successfully")
