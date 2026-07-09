def logger(old_function: callable):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        start = datetime.now()
        sleep(3)
        try:
            result = old_function(*args, **kwargs)
        except Exception as e:
           result = e.__class__.__name__
        args_ = ', '.join(repr(el) for el in args) if args else []
        kwargs_ = ', '.join(f'{k} = {repr(v)}'  for k, v in kwargs.items())  if kwargs else {}   
        end = datetime.now()
        time = end - start
        with open('main.log', 'a', encoding='utf-8') as f:
            info = f'дата: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}, {old_function.__name__}, args = {args_}, kwargs = {kwargs_}, result = {result}, время выполнения: {time}\n'
            f.write(info )
        return result

    return new_function


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
