import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fft_analyzer.core.fft import fft_recursive, ifft_recursive, linear_convolution

x = [0, 1, 2, 3]

X = fft_recursive([complex(v) for v in x])
x_back = ifft_recursive(X)

print("Input:", x)
print("FFT:", X)
print("IFFT:", [z.real for z in x_back])

a = [1, 2, 3]
b = [4, 5]
print("Linear convolution:", linear_convolution(a, b))