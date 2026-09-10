# Connection to Hill's Equation and Floquet Theory

## Overview
This document explores the deep connection between the operator $A_{\alpha,\beta} = \alpha D + \beta V$ and Hill's equation when the coefficients $\alpha(x)$ and $\beta(x)$ are periodic functions. This relationship reveals how the discriminant $\Delta = \lambda^2 - 4\alpha\beta$ generalizes to the Floquet discriminant, governing band structure and stability/instability regions in periodic systems.

## From Operator to Hill's Equation

Consider the eigenvalue problem for $A_{\alpha,\beta}$ with space-dependent coefficients:
$$
\alpha(x) f'(x) + \beta(x) \int_0^x f(\xi)\,d\xi = \lambda f(x)
$$

Differentiating yields:
$$
\alpha(x) f''(x) + \alpha'(x) f'(x) + \beta(x) f(x) = \lambda f'(x)
$$

Rearranging:
$$
\alpha(x) f''(x) + (\alpha'(x) - \lambda) f'(x) + \beta(x) f(x) = 0
$$

To eliminate the first derivative term, we use the transformation:
$$
f(x) = u(x) \exp\left(-\frac{1}{2} \int \frac{\alpha'(x) - \lambda}{\alpha(x)} dx\right) = u(x) \exp\left(-\frac{1}{2} \ln|\alpha(x)| + \frac{\lambda}{2} \int \frac{dx}{\alpha(x)}\right)
$$
$$
= \frac{u(x)}{\sqrt{|\alpha(x)|}} \exp\left(\frac{\lambda}{2} \int \frac{dx}{\alpha(x)}\right)
$$

For simplicity, assume $\alpha(x) > 0$. Then:
$$
f(x) = \frac{u(x)}{\sqrt{\alpha(x)}} \exp\left(\frac{\lambda}{2} \int \frac{dx}{\alpha(x)}\right)
$$

Substituting into the differential equation and simplifying (detailed calculation omitted), we obtain:
$$
u''(x) + Q(x) u(x) = 0
$$
where
$$
Q(x) = \frac{\beta(x)}{\alpha(x)} - \frac{1}{2} \frac{\alpha''(x)}{\alpha(x)} + \frac{1}{4} \left(\frac{\alpha'(x)}{\alpha(x)}\right)^2 - \frac{\lambda}{2} \frac{\alpha'(x)}{\alpha(x)^2} + \frac{\lambda^2}{4\alpha(x)^2}
$$

When $\alpha(x)$ and $\beta(x)$ are constants, this reduces to:
$$
Q = \frac{\beta}{\alpha} + \frac{\lambda^2}{4\alpha^2}
$$
and the equation becomes $u'' + Q u = 0$, which matches our earlier transformation.

However, for the connection to Hill's equation, it's more insightful to consider the case where we first remove the first derivative term from the original second-order form. Starting from:
$$
\alpha(x) f'' - \lambda f' + \beta(x) f = 0
$$
(obtained by differentiating the eigenvalue equation and assuming $\lambda$ constant for now; we'll address $\lambda(x)$ later)

Divide by $\alpha(x)$:
$$
f'' - \frac{\lambda}{\alpha(x)} f' + \frac{\beta(x)}{\alpha(x)} f = 0
$$

Now apply the transformation $f(x) = u(x) \exp\left(\frac{1}{2} \int \frac{\lambda}{\alpha(x)} dx\right)$ to eliminate the first derivative term:
$$
f' = u' \exp\left(\frac{1}{2} \int \frac{\lambda}{\alpha} dx\right) + \frac{1}{2} \frac{\lambda}{\alpha} u \exp\left(\frac{1}{2} \int \frac{\lambda}{\alpha} dx\right)
$$
$$
f'' = u'' \exp\left(\frac{1}{2} \int \frac{\lambda}{\alpha} dx\right) + \frac{\lambda}{\alpha} u' \exp\left(\frac{1}{2} \int \frac{\lambda}{\alpha} dx\right) + \left[\frac{1}{2} \frac{d}{dx}\left(\frac{\lambda}{\alpha}\right) + \frac{1}{4} \left(\frac{\lambda}{\alpha}\right)^2\right] u \exp\left(\frac{1}{2} \int \frac{\lambda}{\alpha} dx\right)
$$

Substituting into the differential equation and simplifying, the first derivative terms cancel, leaving:
$$
u'' + \left[\frac{\beta(x)}{\alpha(x)} - \frac{1}{2} \frac{d}{dx}\left(\frac{\lambda}{\alpha(x)}\right) - \frac{1}{4} \left(\frac{\lambda}{\alpha(x)}\right)^2\right] u = 0
$$

If $\lambda$ is constant, this becomes:
$$
u'' + \left[\frac{\beta(x)}{\alpha(x)} - \frac{\lambda}{2} \frac{\alpha'(x)}{\alpha(x)^2} - \frac{\lambda^2}{4\alpha(x)^2}\right] u = 0
$$

Now, if we further assume that $\alpha(x)$ is constant (or absorb variations into $\beta$), we get the standard Hill's equation form. However, the most elegant connection appears when we consider the original operator in a symmetric form.

## Alternative Approach: The Symmetric Form

Consider the operator in the form:
$$
A = \alpha D + \beta V
$$
with $D = d/dx$, $V f(x) = \int_0^x f(t) dt$.

The formal adjoint of $D$ is $-D$ (under appropriate boundary conditions), and the adjoint of $V$ is the operator $(V^* f)(x) = \int_x^\infty f(t) dt$ (for suitable decay).

However, a more symmetric approach is to consider the operator on the half-line with appropriate boundary conditions, or to use the causal antiderivative.

For periodic problems, it's often more natural to consider the operator on a circle. Let's reinterpret $V$ as the inverse of $D$ on functions with zero mean.

On the circle $S^1 = \mathbb{R}/L\mathbb{Z}$, let $\mathcal{H}$ be the space of square-integrable functions with zero mean. Then $D: \mathcal{H} \to \mathcal{H}$ is invertible, and we can define $V = D^{-1}$ (the antiderivative with zero mean).

In this setting, $D$ and $V$ satisfy the canonical commutation relation:
$$
[D, V] = I
$$
on $\mathcal{H}$.

Our operator becomes:
$$
A = \alpha D + \beta D^{-1}
$$

This is a remarkable form: a linear combination of an operator and its inverse.

The eigenvalue problem is:
$$
(\alpha D + \beta D^{-1}) f = \lambda f
$$

Multiplying by $D$:
$$
\alpha D^2 f + \beta f = \lambda D f
$$
$$
\alpha D^2 f - \lambda D f + \beta f = 0
$$

Which is exactly our second-order ODE:
$$
\alpha f'' - \lambda f' + \beta f = 0
$$

Now, if we expand $f$ in Fourier series on the circle:
$$
f(x) = \sum_{k \in \mathbb{Z}} \hat{f}_k e^{2\pi i k x / L}
$$
then $D f = \sum_{k} (2\pi i k / L) \hat{f}_k e^{2\pi i k x / L}$ and $D^{-1} f = \sum_{k \neq 0} (L/(2\pi i k)) \hat{f}_k e^{2\pi i k x / L}$ (with appropriate handling of the zero mode).

The eigenvalue problem becomes, for each Fourier mode $k \neq 0$:
$$
\alpha (2\pi i k / L)^2 + \beta (L/(2\pi i k)) = \lambda (2\pi i k / L)
$$
$$
-\alpha (2\pi k / L)^2 - i \beta (L/(2\pi k)) = i \lambda (2\pi k / L)
$$

Multiplying by $i$:
$$
i\alpha (2\pi k / L)^2 + \beta (L/(2\pi k)) = -\lambda (2\pi k / L)
$$

This is complex, suggesting we need to be careful with the interpretation. A better approach is to note that $D$ is skew-adjoint ($D^* = -D$) and $D^{-1}$ is also skew-adjoint on the zero-mean subspace, so $A = \alpha D + \beta D^{-1}$ is skew-adjoint if $\alpha$ and $\beta$ are real. But then eigenvalues would be purely imaginary, which doesn't match our earlier findings.

Let's reconsider: perhaps we should use the anti-causal antiderivative or work on the whole line.

## Connection to Hill's Equation via WKB

A more straightforward connection comes from the WKB approximation. For the equation:
$$
\alpha(x) f'' - \lambda f' + \beta(x) f = 0
$$
we look for solutions of the form $f(x) = \exp\left(\frac{1}{\epsilon} \int S(x) dx\right)$ and expand in powers of $\epsilon$.

The leading order gives the eikonal equation:
$$
\alpha(x) S_0^2 - \lambda S_0 + \beta(x) = 0
$$
which is a quadratic in $S_0$:
$$
S_0 = \frac{\lambda \pm \sqrt{\lambda^2 - 4\alpha(x)\beta(x)}}{2\alpha(x)} = \frac{\lambda \pm \sqrt{\Delta(x)}}{2\alpha(x)}
$$

where $\Delta(x) = \lambda^2 - 4\alpha(x)\beta(x)$ is the local discriminant.

The WKB approximation is valid when $|S_0'| \ll S_0^2$, i.e., when the coefficients vary slowly compared to the wavelength.

The two solutions correspond to:
$$
f_{\pm}(x) \approx \frac{1}{\sqrt[4]{\alpha(x)}} \exp\left(\pm \frac{1}{2} \int \frac{\sqrt{\Delta(x)}}{\alpha(x)} dx\right)
$$
when $\Delta(x) > 0$ (exponential behavior), and oscillatory when $\Delta(x) < 0$.

When $\alpha(x)$ and $\beta(x)$ are periodic with period $L$, $\Delta(x)$ is also periodic. The behavior of solutions over one period is determined by the monodromy matrix, and the Floquet exponent $\mu$ satisfies:
$$
\Delta_F = \text{tr}(M) = 2 \cosh(\mu L)
$$
where $M$ is the monodromy matrix and $\Delta_F$ is the Floquet discriminant.

The stability/instability bands are determined by $|\Delta_F| < 1$ (stable, oscillatory Bloch waves) and $|\Delta_F| > 1$ (unstable, exponential growth).

In the limit of slow variation (WKB), the Floquet discriminant can be approximated by:
$$
\Delta_F \approx 2 \cos\left(\oint \frac{\sqrt{-\Delta(x)}}{2\alpha(x)} dx\right)
$$
when $\Delta(x) < 0$ throughout the period (the oscillatory case), where the integral is over one period.

More generally, the connection is that the zeros of $\Delta(x)$ (where $\Delta(x) = 0$) are turning points where the WKB approximation breaks down, and Airy function matching is needed, leading to the quantization condition for bound states in the case of a potential well.

## Band Structure and Gaps

When $\alpha(x)$ and $\beta(x)$ are periodic, the spectrum of the operator $A = \alpha D + \beta V$ (or equivalently, of the Hill's equation $u'' + Q(x) u = 0$) consists of allowed bands where $\Delta_F \in [-1, 1]$ (stable, oscillatory solutions) and forbidden gaps where $|\Delta_F| > 1$ (exponential solutions).

The width of the bands and gaps depends on the magnitude of the periodic variations in $\alpha(x)$ and $\beta(x)$.

In the limit of small perturbations, we can use perturbation theory. Let:
$$
\alpha(x) = \alpha_0 + \alpha_1(x), \quad \beta(x) = \beta_0 + \beta_1(x)
$$
where $\alpha_1, \beta_1$ are small and periodic with zero mean.

Then to first order, the discriminant $\Delta = \lambda^2 - 4\alpha\beta$ varies as:
$$
\Delta(x) \approx \lambda^2 - 4\alpha_0\beta_0 - 4(\alpha_0\beta_1 + \beta_0\alpha_1)(x)
$$

The corresponding Hill's equation for $u$ will have a periodic potential proportional to $\alpha_0\beta_1 + \beta_0\alpha_1$, leading to band gaps at the Brillouin zone boundaries.

## Special Case: Mathieu Equation

A particularly important special case occurs when the periodic coefficient is a cosine function, leading to Mathieu's equation:
$$
u'' + (a - 2q \cos 2x) u = 0
$$

This can be obtained from our operator by choosing appropriate periodic forms for $\alpha(x)$ and $\beta(x)$. For example, if we set:
$$
\alpha(x) = 1, \quad \beta(x) = \beta_0 + \beta_1 \cos(2x/\lambda_0)
$$
and adjust $\lambda$ appropriately, we can recover Mathieu's equation after suitable transformations.

Mathieu's equation appears in many physical contexts: vibrations in elliptic membranes, wave propagation in periodic media, quantum mechanics in periodic potentials, and stability analysis in dynamical systems.

The characteristic exponents of Mathieu's equation determine stability regions in the $(a,q)$ plane, analogous to how the discriminant $\Delta$ determines behavior in our constant-coefficient case.

## Summary of Connections

1. **Hill's Equation**: When $\alpha(x)$ and $\beta(x)$ are periodic, the eigenvalue problem for $A_{\alpha,\beta}$ reduces to Hill's equation $u'' + Q(x) u = 0$ after eliminating the first derivative term.

2. **Floquet Theory**: The behavior of solutions is governed by the Floquet exponent $\mu$, with stability determined by $|\text{tr}(M)| < 1$ where $M$ is the monodromy matrix over one period.

3. **Band Structure**: The spectrum consists of allowed bands (stable oscillatory solutions) and forbidden gaps (exponential solutions), with band edges determined by periodic or antiperiodic boundary conditions.

4. **Turning Points**: Where the local discriminant $\Delta(x) = \lambda^2 - 4\alpha(x)\beta(x)$ changes sign, we have turning points where WKB approximation fails and Airy matching is needed.

5. **Mathieu Equation**: A special case with cosine potential, relevant for many physical applications.

6. **Connection to Discriminant**: The local discriminant $\Delta(x)$ plays the same role in the periodic case as the constant discriminant does in the constant-coefficient case: it determines the local character of the solution (oscillatory vs. exponential), and its integral over a period relates to the Floquet discriminant.

This connection shows that the discriminant $\Delta = \lambda^2 - 4\alpha\beta$ is not merely a constant in the homogeneous case but generalizes to a local quantity that governs the rich band structure and stability properties of periodic systems, linking our operator to deep topics in differential equations, solid-state physics, and dynamical systems.