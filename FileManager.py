from File import FileObject

class FileManager:
    def _init_(self):
        self.current_dir = '/'
        self.files = {}
        self.memory_map = []

    def create(self, file_name):
        if file_name in self.files:
            print(f'{file_name} already exists')
            return
        self.files[file_name] = {
            'data': '',
            'size': 0,
            'start': None,
            'blocks': []
        }
        print(f'{file_name} created')

    def delete(self, file_name):
        if file_name not in self.files:
            print(f'{file_name} does not exist')
            return
        for block in self.files[file_name]['blocks']:
            self.memory_map[block] = 0
        del self.files[file_name]
        print(f'{file_name} deleted')

    def mkdir(self, dir_name):
        if dir_name in self.files:
            print(f'{dir_name} already exists')
            return
        self.files[dir_name] = {
            'type': 'dir',
            'contents': {}
        }
        print(f'{dir_name} created')

    def chdir(self, dir_name):
        if dir_name not in self.files or self.files[dir_name]['type'] != 'dir':
            print(f'{dir_name} is not a valid directory')
            return
        self.current_dir = dir_name
        print(f'Changed current directory to {dir_name}')

    def move(self, source_file, target_file):
        if source_file not in self.files:
            print(f'{source_file} does not exist')
            return
        if target_file in self.files:
            print(f'{target_file} already exists')
            return
        self.files[target_file] = self.files[source_file]
        del self.files[source_file]
        print(f'{source_file} moved to {target_file}')

    def open(self, file_name, mode):
        if file_name not in self.files:
            print(f'{file_name} does not exist')
            return None
        if mode not in ['r', 'w', 'a']:
            print(f'{mode} is not a valid mode')
            return None
        return FileObject(self, file_name, mode)

    def show_memory_map(self):
        print(self.memory_map)

    def _find_free_blocks(self, size):
        free_blocks = []
        block_count = len(self.memory_map)
        for i in range(block_count):
            if self.memory_map[i] == 0:
                free_blocks.append(i)
                if len(free_blocks) == size:
                    return free_blocks
            else:
                free_blocks = []
        return None

    def _allocate_blocks(self, size):
        free_blocks = self._find_free_blocks(size)
        if free_blocks is None:
            print(f'Not enough space to allocate {size} blocks')
            return None
        for block in free_blocks:
            self.memory_map[block] = 1
        return free_blocks

    def _free_blocks(self, blocks):
        for block in blocks:
            self.memory_map[block] = 0


