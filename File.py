import math

class FileObject:
    def __init__(self, file_manager, file_name, mode):
        self.file_manager = file_manager
        self.file_name = file_name
        self.mode = mode
        self.file_data = file_manager.files[file_name]['data']
        self.file_size = file_manager.files[file_name]['size']
        self.blocks=file_manager.files[file_name]['blocks']

    def _write_data(self, data, pos=None):
        if self.mode == 'r':
            print(f'{self.file_name} is read-only')
            return
        if pos is None:
            pos = self.file_size
        self.file_data = self.file_data[:pos] + data + self.file_data[pos:]
        self.file_size += len(data)
        length= math.ceil(self.file_size / self.file_manager.block_size)
        self.file_manager._free_blocks(self.blocks)
        self.blocks=self.file_manager._allocate_blocks(length)


    def write(self, data):
        self._write_data(data)

    def writelines(self, lines):
        data = ''.join(lines)
        self._write_data(data)

    def read(self, size=-1):
        if self.mode == 'w':
            print(f'{self.file_name} is write-only')
            return None
        if size == -1:
            return self.file_data
        else:
            return self.file_data[:size]

    def readlines(self, size=-1):
        if self.mode == 'w':
            print(f'{self.file_name} is write-only')
            return None
        if size == -1:
            return self.file_data.splitlines()
        else:
            lines = self.file_data.splitlines()
            return [line[:size] for line in lines]

    def close(self):
        self.file_manager.files[self.file_name]['data'] = self.file_data
        self.file_manager.files[self.file_name]['size'] = self.file_size
        self.file_manager.files[self.file_name]['blocks'] = self.blocks