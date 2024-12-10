import unittest
import os
import tarfile
import time
from io import StringIO
from unittest.mock import patch
from emulator import list_files_in_tar, change_directory, tac_file, run_shell, parse_config

class TestShellCommands(unittest.TestCase):

    def setUp(self):
        # Используем данные из config.xml
        self.config_file = "config.xml"
        self.username, self.computername, self.filesystem = parse_config(self.config_file)
        
        # Создаём тестовый архив для файловой системы
        self.test_tar = "test_virtual_filesystem.tar"
        with tarfile.open(self.test_tar, "w") as tar:
            os.makedirs("test_dir", exist_ok=True)
            with open("test_dir/test_file.txt", "w") as f:
                f.write("line 1\nline 2\nline 3")
            tar.add("test_dir", arcname="test_dir")

        self.filesystem = self.test_tar

    def tearDown(self):
        # Удаляем тестовый архив и директорию
        if os.path.exists(self.test_tar):
            os.remove(self.test_tar)
        if os.path.exists("test_dir"):
            for file in os.listdir("test_dir"):
                os.remove(os.path.join("test_dir", file))
            os.rmdir("test_dir")

    # Тест команды ls
    def test_ls(self):
        expected_files = ['test_dir']
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            files = list_files_in_tar(self.filesystem, '/')
            print("\n".join(files))
            output = mock_stdout.getvalue().strip().splitlines()
            self.assertEqual(output, expected_files)

    def test_ls_empty_directory(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            files = list_files_in_tar(self.filesystem, '/empty_dir')
            print("\n".join(files))
            output = mock_stdout.getvalue().strip().splitlines()
            self.assertEqual(output, [])

    # Тест команды cd
    def test_cd_success(self):
        new_directory = '/test_dir'
        result = change_directory(self.filesystem, '/', 'test_dir')
        self.assertEqual(result, new_directory)

    def test_cd_fail(self):
        current_directory = '/'
        result = change_directory(self.filesystem, current_directory, 'non_existing_dir')
        self.assertEqual(result, current_directory)

    # Тест команды exit
    @patch('builtins.input', return_value='exit')
    def test_exit(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', return_value='exit'):
                run_shell(self.username, self.computername, self.filesystem)
            output = mock_stdout.getvalue()
            self.assertIn("Exiting...", output)

    # Тест команды uptime
    def test_uptime(self):
        start_time = time.time()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            uptime = time.time() - start_time
            print(f"Uptime: {uptime:.2f} seconds")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("Uptime" in output)

    # Тест команды tac
    def test_tac(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            tac_file(self.filesystem, '/test_dir', 'test_file.txt')
            output = mock_stdout.getvalue().strip()
            self.assertTrue(output.startswith('line 3'))  # Проверка, что строки выводятся в обратном порядке

    def test_tac_fail(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            tac_file(self.filesystem, '/test_dir', 'non_existing_file.txt')
            output = mock_stdout.getvalue().strip()
            self.assertIn("File 'non_existing_file.txt' not found.", output)

if __name__ == '__main__':
    unittest.main()
