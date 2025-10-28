import torch, platform
print("Python:", platform.python_version())
print("Torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Device count:", torch.cuda.device_count())
    print("GPU 0:", torch.cuda.get_device_name(0))
    a = torch.rand((1024,1024), device="cuda")
    b = torch.mm(a, a)
    print("Matmul OK, tensor device:", b.device)
