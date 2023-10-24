import os
import base64

class FileEncoder:

    def __init__(self, input_directory='./unencoded_file', output_directory='./processed', archive_directory='./unencoded_file/Archive'):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.archive_directory = archive_directory
        # Ensure the processed and archive directories exist
        os.makedirs(self.output_directory, exist_ok=True)
        os.makedirs(self.archive_directory, exist_ok=True)

    def encode_file_to_base64(self, filepath):
        with open(filepath, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)
            return encoded_content.decode('utf-8')

    def process_files(self):
        for filename in os.listdir(self.input_directory):
            # Encode the file and save the encoded content
            if filename == 'Archive':
                continue
            else:
                file_name_without_extension = os.path.splitext(filename)[0]
                input_file_path = os.path.join(self.input_directory, filename)
                output_file_path = os.path.join(self.output_directory, ('Encoded_' + file_name_without_extension + '.txt'))
                encoded_content = self.encode_file_to_base64(input_file_path)
                with open(output_file_path, 'w') as file:
                    file.write(encoded_content)
                destination = f'{self.archive_directory}/{filename}'
                if os.path.exists(destination):
                    # If it exists, remove it
                    os.remove(destination)
                os.rename(input_file_path, destination)
        print(f"Encoded files saved to {self.output_directory}")


# Example usage:

# encoder = FileEncoder()
# encoder.process_files()
