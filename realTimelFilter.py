import time
import math


class LowPass:
    def __init__(self, f0, fs, adaptive):
        self.order = 2  # You can change the order if needed
        self.a = [0.0] * self.order
        self.b = [0.0] * (self.order + 1)
        self.omega0 = 6.28318530718 * f0
        self.dt = 1.0 / fs
        self.adapt = adaptive
        self.tn1 = -self.dt
        self.x = [0.0] * (self.order + 1)
        self.y = [0.0] * (self.order + 1)
        self.set_coef()

    def set_coef(self):
        if self.adapt:
            t = time.time()
            self.dt = t - self.tn1
            self.tn1 = t

        alpha = self.omega0 * self.dt
        if self.order == 1:
            self.a[0] = -(alpha - 2.0) / (alpha + 2.0)
            self.b[0] = alpha / (alpha + 2.0)
            self.b[1] = alpha / (alpha + 2.0)
        elif self.order == 2:
            alpha_sq = alpha * alpha
            beta = [1, math.sqrt(2), 1]
            D = alpha_sq * beta[0] + 2 * alpha * beta[1] + 4 * beta[2]
            self.b[0] = alpha_sq / D
            self.b[1] = 2 * self.b[0]
            self.b[2] = self.b[0]
            self.a[0] = -(2 * alpha_sq * beta[0] - 8 * beta[2]) / D
            self.a[1] = -(beta[0] * alpha_sq - 2 * beta[1]
                          * alpha + 4 * beta[2]) / D

    def filt(self, xn):
        if self.adapt:
            self.set_coef()

        self.y[0] = 0
        self.x[0] = xn

        for k in range(self.order):
            self.y[0] += self.a[k] * self.y[k + 1] + self.b[k] * self.x[k]

        self.y[0] += self.b[self.order] * self.x[self.order]

        for k in range(self.order, 0, -1):
            self.y[k] = self.y[k - 1]
            self.x[k] = self.x[k - 1]

        return self.y[0]


# Filter instance
lp = LowPass(3, 1e3, True)

# Replace the following lines with your own sensor reading code
analog_value = 512
xn = (analog_value * 5.0 / 1023.0 - 2.503) / 0.185 * 1000

# Compute the filtered signal
yn = lp.filt(xn)

# Output
print(f"Raw Value: {xn}")
print(f"Filtered Value: {yn}")
