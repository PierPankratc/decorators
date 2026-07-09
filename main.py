def logger(old_function: callable):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        start = datetime.now()
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




def path_logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            start = datetime.now()
            try:
                result = old_function(*args, **kwargs)
            except Exception as e:
                result = e.__class__.__name__
            args_ = ', '.join(repr(arg) for arg in args) if args else []
            kwargs_ = ', '.join(f'{k} = {repr(v)}' for k, v in kwargs.items()) if kwargs else {}
            end = datetime.now()
            time = end - start
            info = f'дата: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}, {old_function.__name__}, args = {args_}, kwargs = {kwargs_}, result = {result}, время выполнения: {time}\n'
            with open(path,  'a', encoding='utf-8') as f:
                f.write(info)
            return result
        return new_function
    return __logger


class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0
        self.inner_index = 0

    def __iter__(self):
      return self
    
    @logger
    @path_logger('new_log.log')
    def __next__(self):
        if self.outer_index >= len(self.list_of_list):
            raise StopIteration
        
        current_list = self.list_of_list[self.outer_index]
        if self.inner_index >= len(current_list):
            self.outer_index += 1
            self.inner_index = 0
            return self.__next__()
        
        item = current_list[self.inner_index]
        self.inner_index += 1
        
        return item
    
lst = FlatIterator([[1], [8,3, 4], [5]])
lst.__iter__()
lst.__next__()
lst.__next__()

