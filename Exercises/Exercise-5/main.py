import psycopg2


def main():
    host = 'postgres'
    database = 'postgres'
    user = 'postgres'
    pas = 'postgres'
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    pass
    #for root, dirs, files in os.walk(target_path):
    #    for file in files:
    #        if file.endswith(".json"):


if __name__ == '__main__':
    main()
