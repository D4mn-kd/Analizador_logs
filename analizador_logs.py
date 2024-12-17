import re
import argparse
import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",style='%')

def format_logs(file_logs: str) -> list[str]:
    return file_logs.split('\n')

def format_filters(filters: str) -> list[str]:
    return filters.split(',')

def search_pattern(filter: str) -> list[str]:
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
        return [is_ip,"is_ip"]
    
    elif re.search(is_date, filter):
        return [is_date,"is_date"]

    elif re.search(is_status_code, filter):
        return [r"(?<=\s)[1-5][0-9]{2}(?=\s)", "is_status_code"]
    
    elif re.search(is_http_method, filter):
        return [is_http_method,"is_http_method"]
    
    else:
        raise ValueError(f"Invalid filter: {filter}")

def dic_filters(filters: list[str]) -> dict[str, list[str]]:
    """
    This function creates a dictionary with the filters to apply to the logs

    :Args:
    filters: list[str] -> filters to apply to the logs

    :Returns:
    dict[str, list[str]]: dictionary with the filters to apply to the logs

    """
    filter_dict = {
        "is_ip": [],
        "is_status_code": [],
        "is_http_method": [],
        "is_date": []
    }
    
    for filter in filters:
        type_filter = search_pattern(filter)[1]
        if type_filter in filter_dict:
            filter_dict[type_filter].append(filter)
        else:
            logging.error(f"Invalid filter: {filter}")
            
    return filter_dict

def filter_logs(list_logs: list[str], filters: list[str]) -> list[str]:
    """
    This function filters the logs based on the filter provided

    :Args:
    list_logs: list[str] -> list of logs
    filters: list[str] -> filters to apply to the logs

    :Returns:
    list[str]: list of logs that match

    """
    try:
        patterns: list[list[str]] = [search_pattern(f) for f in filters]
    except ValueError as e:
        logging.error(e)
        return []
    try:
        filters_dic:  dict[str, list[str]]= dic_filters(filters)
    except Exception as e:
        logging.error(e)
        return []
        
    for regex,type_pattern in patterns:
        list_logs = [log for log in list_logs if re.search(regex, log) and re.search(regex, log).group() in filters_dic[type_pattern]]

    if not list_logs:
        print("No logs found")

    return list_logs
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some logs. [Example ejecution:python analizador_logs.py -logfile server_logs.log -filters 200,GET]')
    parser.add_argument('-logfile',required=True, type=str, help='The log file to process')
    parser.add_argument('-filters',required=True ,type=str,
                         help='The filters to apply to the logs (IP[example:8.8.8.8], status code[example:200], HTTP[example:GET] method and date[example:01/Jan/2021])')
    parser.add_argument('-export', type=str, help='Export the logs to a file')
    parser.add_argument('-verbose','-v', action='store_true', help='Print the logs in the console si el número de logs es menor a 100')
    args = parser.parse_args()

    try:
        with open(args.logfile, 'r') as file:
            file_logs: str = file.read()
    except FileNotFoundError:
        logging.error(f"File {args.logfile} not found")
        exit(1)
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        exit(1)

    start_time = datetime.datetime.now()
    list_logs: list[str] = format_logs(file_logs)
    list_filters: list[str] = format_filters(args.filters)
    logs: list[str] = filter_logs(list_logs,list_filters)

    if logs:
        
        end_time = datetime.datetime.now()
        logging.info(f"Logs found in {end_time - start_time}")
        logging.info(f"Logs found: {len(logs)}")
        
        if args.verbose and len(logs) < 100:
            for log in logs:
                print(log)
        
        if args.export:
            with open(f'{args.export}.txt', 'w') as file:
                for log in logs:
                    file.write(f"{log}\n")
            logging.info(f"Logs exported successfully to {args.export}.txt")
