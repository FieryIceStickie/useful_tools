import numpy as np

def main():
    x = np.linspace(0, 2 * np.pi, 1000, endpoint=False)
    dx = 2 * np.pi / 1000
    fx = (np.sin(x)**2 + 2*np.sin(x) + 2)/((1+np.cos(x)**2) * np.sqrt(3+2*np.sin(x))) 
    result = np.sum(fx) * dx
    print(result, result / (2*np.pi), sep='\n')


if __name__ == '__main__':
    main()
