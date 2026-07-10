from services.file_service import FileService

service = FileService()

try:
    result = service.extract_file("sample.txt")
    print(result)
except Exception as e:
    print(type(e).__name__)
    print(e)