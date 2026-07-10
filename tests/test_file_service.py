from services.file_service import FileService

service = FileService()

print(service.extract_file("sample.pdf"))