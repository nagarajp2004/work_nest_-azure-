let isSignUpMode = false;

function switchMode(mode) {
    isSignUpMode = mode === 'signup';
    const toggle = document.getElementById('authToggle');
    const signupFields = document.querySelectorAll('.signup-fields');
    const forgotPassword = document.getElementById('forgotPassword');
    const submitText = document.getElementById('submitText');
    const subtitle = document.querySelector('.subtitle');

    // Update toggle appearance
    toggle.className = isSignUpMode ? 'auth-toggle signup' : 'auth-toggle';

    // Update active button
    document.querySelectorAll('.auth-toggle button').forEach(btn => btn.classList.remove('active'));
    document.querySelector(isSignUpMode ? '.signup-btn' : '.signin-btn').classList.add('active');

    // Show/hide signup fields
    signupFields.forEach(field => {
        field.classList.toggle('show', isSignUpMode);
    });

    // Show/hide forgot password
    forgotPassword.style.display = isSignUpMode ? 'none' : 'block';

    // Update submit button text
    submitText.textContent = isSignUpMode ? 'Create Account' : 'Sign In';

    // Update subtitle
    subtitle.textContent = isSignUpMode ?
        'Create your account to get started' :
        'Welcome back! Please sign in to your account';

    // Clear form
    document.getElementById('authForm').reset();
    clearAlert();
}

function togglePassword(fieldId = 'password') {
    const field = document.getElementById(fieldId);
    const button = field.nextElementSibling;

    if (field.type === 'password') {
        field.type = 'text';
        button.textContent = '🙈';
    } else {
        field.type = 'password';
        button.textContent = '👁️';
    }
}

function showAlert(message, type = 'error') {
    const container = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;

    container.innerHTML = '';
    container.appendChild(alert);

    // Trigger animation
    setTimeout(() => alert.classList.add('show'), 100);

    // Auto hide after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => container.innerHTML = '', 300);
    }, 5000);
}

function clearAlert() {
    const container = document.getElementById('alertContainer');
    container.innerHTML = '';
}

function setLoading(loading) {
    const btn = document.getElementById('submitBtn');
    const text = document.getElementById('submitText');

    if (loading) {
        btn.classList.add('loading');
        btn.disabled = true;
        text.textContent = isSignUpMode ? 'Creating Account...' : 'Signing In...';
    } else {
        btn.classList.remove('loading');
        btn.disabled = false;
        text.textContent = isSignUpMode ? 'Create Account' : 'Sign In';
    }
}

// Form submission handler
document.getElementById('authForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData);

    // Basic validation
    if (!data.username || !data.password) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    if (isSignUpMode) {
        if (!data.firstName || !data.lastName || !data.email || !data.designation) {
            showAlert('Please fill in all fields for registration', 'error');
            return;
        }

        if (data.password !== data.confirmPassword) {
            showAlert('Passwords do not match', 'error');
            return;
        }

        if (data.password.length < 6) {
            showAlert('Password must be at least 6 characters long', 'error');
            return;
        }
    }

    setLoading(true);
    clearAlert();

    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));

        if (isSignUpMode) {
            // Simulate successful signup
            showAlert('Account created successfully! Please sign in.', 'success');
            setTimeout(() => switchMode('signin'), 2000);
        } else {
            // Simulate successful login
            showAlert('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                // Redirect to main app
                window.location.href = '#dashboard';
            }, 1500);
        }

    } catch (error) {
        showAlert(error.message || 'An error occurred. Please try again.', 'error');
    } finally {
        setLoading(false);
    }
});

// Add input focus effects
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('focus', function () {
        this.parentElement.style.transform = 'translateY(-2px)';
    });

    input.addEventListener('blur', function () {
        this.parentElement.style.transform = 'translateY(0)';
    });
});

// Add some interactive feedback
document.querySelectorAll('.social-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
});
